#!/data/software/conda/bin/python3.7
import os,sys
import time
import parasail
from collections import deque
import re
"""
Usage:
./MEAT.py $file.faa(prot) $file.pfam $blast_taget.txt [window=$int(bp)](optional, default=50000) [pfam_domain_similarity=$(float)](optional,default=0.0)
pfam annotations are generated by pfam_scan.pl
#############################################################
#********Mycology Exploring Annotation Tool*****************#
#********************MEAT by ZHANG W************************#
#******zhangww@big.ac.cn    Wechat&TEL:18210123493**********#
#***********Beijing Institute of Genomics, CAS, CN**********#
#***********************************************************#
#############################################################

"""

#********extract path*********#
#print (os.path.abspath('genbank'))
def read_fasta(name):
	t=[]
	with open(name) as rawdata:
		for line in rawdata:
			if line=='' or line=='\n':
				continue
			if line[0]=='>':
				t.append(line.split()[0])
				t.append('')
			if line[0]!='>':
				t[-1]+=line.strip()
	return t
#print(read_fasta('test.faa'))
def get_gene_location(genename,gfflocations,gtflocations):
	chro,start,end='',0,0
	if gtflocations.split('.')[-1]=='gtf':
#		print('GTF')
		with open(gtflocations) as los:
			for lo in los:
				if len(lo.split('\t'))<4:
					continue
				if lo.split('\t')[2]=='CDS':
#					print(lo.split('\t')[-1].split(';')[0].split('"')[-2])
					if lo.split('\t')[-1].split(';')[0].split('"')[-2]==genename:
						chro,start,end=lo.split('\t')[0],min(int(lo.split('\t')[3]),int(lo.split('\t')[4])),max(int(lo.split('\t')[3]),int(lo.split('\t')[4]))
	if gfflocations.split('.')[-1]=='gff':
		with open(gfflocations) as los:
			for lo in los:
				if len(lo.split('\t'))<4:
					continue
				if lo.split('\t')[2]=='CDS':
#					print(lo.split('\t')[-1].split(';')[0].split('XP_')[-1])
					if lo.split('\t')[-1].split(';')[0].split('XP_')[-1]==genename.split('XP_')[-1]:
						chro,start,end=lo.split('\t')[0],min(int(lo.split('\t')[3]),int(lo.split('\t')[4])),max(int(lo.split('\t')[3]),int(lo.split('\t')[4]))
	return chro,start,end
def get_domain_sequence(protein_fasta,proteinID,pfamstart,pfamend):
	for n in range(0,int(len(protein_fasta)/2)):
		if protein_fasta[2*n].split()[0][1:]==proteinID:
			return protein_fasta[2*n+1][pfamstart-1:pfamend]
			break
def get_protein_sequence(protein_fasta,proteinID):
	for n in range(0,int(len(protein_fasta)/2)):
		if protein_fasta[2*n].split()[0][1:]==proteinID:
			return protein_fasta[2*n+1].strip()
			break
def get_gdna_sequence(genome_fasta,chroID,seqstart,seqend):
	for n in range(0,int(len(genome_fasta)/2)):
		if genome_fasta[2*n].split()[0][1:]==chroID:
			return genome_fasta[2*n+1][max([0,seqstart-1]):min([seqend,len(genome_fasta[2*n+1])-2])]
def protein_domain_similarity(sequence1,sequence2):
	aaset=''.join([i for i in list(set(sequence1+sequence2))])
	aamatrix=parasail.matrix_create(aaset,2,-2)
	parasail_result=parasail.sg_trace_scan_16(sequence1,sequence2,5,1,aamatrix)
	parasail_cigar=str(parasail_result.cigar.decode,'utf-8')
	t=[]
	z=''
	for w in parasail_cigar:
		if ord(w)>=ord('0') and ord(w)<=ord('9'):
			z+=w
		else:
			if w=='=':
				t.append(int(z))
				z=''
			else:
				z=''
#	print(parasail_cigar)
	return sum(t)*2/(len(sequence1)+len(sequence2))
	
def main(query_protein,pfam_query,blast_query,window,similarity):
	sequence_containing_domains,pfam_annotation,query_annots=[],[],[]#1. get pfam domains and the corresponding genes
	for p in pfam_query:
		if p[0]=='#' or p=='\n':
			continue
		if len(p.split())==1:
			pfam_annotation.append(p.strip())
		if len(p.split())>6:
			query_annots.append(p)
			pfam_annotation.append(p.split()[6])
	pfam_annotation =list(set(pfam_annotation))
	pfam_query=query_annots
	blast_annotation=list(set([annot.split()[1] for annot in blast_query]))#2. get blast genes and the annotations
	blast_index,blast_genes,blast_identity={annot.split()[0]:annot.split()[1] for annot in blast_query},[annot.split()[0] for annot in blast_query],{annot.split()[0]:float(annot.split()[2]) for  annot in blast_query}
	blast_query_sequence=[''.join(('>',protein,'\n',get_protein_sequence(query_protein,protein),'\n')) for protein in blast_genes]
	protein_query_sequence_output=open('{}_for_blast.fasta'.format(sys.argv[3].split('.')[0]),'w')
	protein_query_sequence_output.writelines(blast_query_sequence)
	protein_query_sequence_output.close()	
	filepaths={}#3. scan the genome paths
	with open('refseq_dic.txt') as refseqs:
		for line in refseqs:
			filepaths[line.split()[-1]]=''.join((os.path.abspath('refseq'),'/fungi/',line.split()[-1]))
	with open('genbank_dic.txt') as genbanks:
		for line in genbanks:
			try:
				have_dic_or_not=filepaths[line.split()[-1]]
			except:
				filepaths[line.split()[-1]]=''.join((os.path.abspath('genbank'),'/fungi/',line.split()[-1]))
#*********get file names********#
	for i,access in enumerate(filepaths):
	#	if i>30:
	#		break
#		if i<457:
#			continue
		print(i,access,filepaths[access])
		filedirs=os.listdir(filepaths[access])
		proteinname,dnaname,gffname,gtfname,pfamname='','','','',''
		for filename in filedirs:#4. get the files in the folder
			if filename==access+'.fasta':
				dnaname=filename
			if filename==access+'.faa':
				proteinname=filename
			if filename==access+'.gff':
				gffname=filename
			if filename==access+'.gtf':
				gtfname=filename
			if filename==access+'.pfam':
				pfamname=filename
		print (proteinname,dnaname,gffname,gtfname,pfamname)
		if not pfamname or not dnaname or not (gffname or gtfname) or not proteinname:
			continue
		protein_sequence=read_fasta(''.join((filepaths[access],'/',proteinname)))
		genome_sequence=read_fasta(''.join((filepaths[access],'/',dnaname)))
		gene_al={pfam:[] for pfam in pfam_annotation}#5. *******get pfam sequences
		with open(''.join((filepaths[access],'/',access,'.pfam'))) as all_pfams:
			for pfam_annot in all_pfams:
				if pfam_annot[0]!='#' and pfam_annot!='\n' and pfam_annot.split()[6] in pfam_annotation:
					gene_al[pfam_annot.split()[6]].append((pfam_annot.split()[6],pfam_annot.split()[0],get_gene_location(pfam_annot.split()[0],''.join((filepaths[access],'/',gffname)),''.join((filepaths[access],'/',gtfname))),int(pfam_annot.split()[1]),int(pfam_annot.split()[2])))
#6. ***********get blast sequences
		os.system("blastp -db {0} -query '{1}_for_blast.fasta' -out {1}_blast.out -evalue 0.5 -outfmt 6".format(''.join((filepaths[access],'/protein_blast')),sys.argv[3].split('.')[0]))
		blast_results={blast:[] for blast in blast_annotation}
		with open('{}_blast.out'.format(sys.argv[3].split('.')[0])) as query_sequence_blast_results:
			for blast_result in query_sequence_blast_results:
				if 100*float(blast_result.split()[2])>blast_identity[blast_result.split()[0]]:
					blast_gene_location=(blast_index[blast_result.split()[0]],blast_result.split()[1],get_gene_location(blast_result.split()[1],''.join((filepaths[access],'/',gffname)),''.join((filepaths[access],'/',gtfname))),'Blast','-results')
					if blast_gene_location not in blast_results[blast_index[blast_result.split()[0]]]:
						blast_results[blast_index[blast_result.split()[0]]].append(blast_gene_location)
		gene_array=[]#7. put all the genes together and sort 
		for i,j in enumerate(gene_al):
			for pfam,gene,(chro,start,end),pfamstart,pfamend in gene_al[j]:
				if chro and start:
					gene_array.append((pfam,gene,chro,start,end,pfamstart,pfamend))
		for i,j in enumerate(blast_results):
			for pfam,gene,(chro,start,end),pfamstart,pfamend in blast_results[j]:
				if chro and start:
					gene_array.append((pfam,gene,chro,start,end,pfamstart,pfamend))
		
		gene_array.sort(key=lambda x: x[3])
		gene_array.sort(key=lambda x: x[2])
#		print(gene_array)
		if not gene_array:
			continue
		genemer=[(gene_array[0])]#define initial windows
		genemer=deque(genemer)
		for gene in gene_array:#8. check if the window fullfil blast and pfam results
			sumpfam,sumblast,boolblast,boolpfam=1,1,{blast:False for blast in blast_annotation},{pfam:False for pfam in pfam_annotation}
			genemer.append((gene))
			while genemer[-1][2]!=genemer[0][2] or max(genemer[-1][3],genemer[-1][4])-min(genemer[0][4],genemer[0][3])>window:
				if len(genemer)==1:
					break
				t=genemer.popleft()
#			print('after remove', genemer)
			for gene in genemer:#8.1. blast check
				boolblast[gene[0]]=True
			for _,i in enumerate(boolblast):
				sumblast*=boolblast[i]
			if not sumblast:
				continue
			for gene in genemer:#8.2. domain check
				boolpfam[gene[0]]=True
			
			for _,i in enumerate(boolpfam):
				sumpfam*=boolpfam[i] 
			if sumpfam:
#				print('Yes domain',genemer)
				simlaritypfam=1
				simpfam={pfam:False for pfam in pfam_annotation}	
				query_informations=deque((line.split()[6],line.split()[0],int(line.split()[1]),int(line.split()[2])) for line in pfam_query)	
				for q in query_informations:
					for r in genemer:
						if q[0]==r[0]:
							if not get_domain_sequence(protein_sequence,r[1],r[5],r[6]):
								continue
				#			print('domainq',get_domain_sequence(query_protein,q[1],q[2],q[3]),'domainr',get_domain_sequence(protein_sequence,r[1],r[5],r[6]))
							print(protein_domain_similarity(get_domain_sequence(query_protein,q[1],q[2],q[3]),get_domain_sequence(protein_sequence,r[1],r[5],r[6])))
							if protein_domain_similarity(get_domain_sequence(query_protein,q[1],q[2],q[3]),get_domain_sequence(protein_sequence,r[1],r[5],r[6]))>similarity:
								simpfam[q[0]]=True
				for _,i in enumerate(simpfam):
					simlaritypfam*=simpfam[i]
				if simlaritypfam:
					print('All domain and genes present and similarities are OK',genemer)
					identified_sequence=get_gdna_sequence(genome_sequence,genemer[0][2],genemer[0][3]-int(window),genemer[-1][4]+int(window))
					sequence_containing_domains.append((dnaname,identified_sequence,list(genemer)))
	return sequence_containing_domains
									





	
				

if __name__ =='__main__':
	window=50000
	similarity=0.0
	try:
		window=int(sys.argv[4])
		similarity=float(sys.argv[4])
	except:
		print('Use default w=50000')
	try:
		similarity=float(sys.argv[5])
	except:
		a=0
	if similarity>1:
		similarity=0.0
	print('Use similarity=',similarity,';\tUse window=',window)
	query_sequences=''
	try:
		pfam_query=open(sys.argv[2]).readlines()
	except:
		print('Usage:  ./MEAT.py $file.faa(prot) $file.pfam $blast_taget.txt [window=$int(bp)](optional, default=50000) [pfam_domain_similarity=$(float)](optional,default=0.0)\ne.g.: ./MEAT.py query_sequence.fasta query_pfam.pfam blast_proteins.txt 50000 0.3')
		sys.exit()
	query_sequence=read_fasta(sys.argv[1])
	try:
		blast_query=open(sys.argv[3]).readlines()
	except:
		print('Usage:  ./MEAT.py $file.faa(prot) $file.pfam $blast_taget.txt [window=$int(bp)](optional, default=50000) [pfam_domain_similarity=$(float)](optional,default=0.0)')
		sys.exit()
	sequence_containing_domains=main(query_sequence,pfam_query,blast_query,window,similarity)
	outputfile=open('meat_result{}.fasta'.format(time.time()),'w')
	for s in sequence_containing_domains:
		if len(s[1])>window*10:
			continue
#		print(s[2])
		annotation=''
		for (domain,gene,chro,start,end,pfamstart,pfamend) in s[2]:
				 annotation+='{0}:{1}-{2}|{3}:{4}-{5}//'.format(gene,start-s[2][0][3]+int(window),end-s[2][0][3]+int(window),domain,pfamstart,pfamend)	
		outputfile.writelines('>{0} {1}\n{2}\n'.format(s[0],annotation,s[1]))
	os.system("mv {0}_for_blast.fasta bak/{0}_for_blast{1}.fasta".format(sys.argv[3].split('.')[0],str(time.time())))
	os.system("mv {0}_blast.out bak/{0}_blast{1}.out".format(sys.argv[3].split('.')[0],str(time.time())))
