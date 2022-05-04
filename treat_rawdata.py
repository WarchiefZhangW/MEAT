#!/data/software/conda/bin/python3.7
import os,sys
#********extract path*********#
#print (os.path.abspath('genbank'))
filepaths={}
with open('refseq_dic.txt') as refseqs:
	for line in refseqs:
		filepaths[line.split()[-1]]=''.join((os.path.abspath('refseq'),'/fungi/',line.split()[-1]))
with open('genbank_dic.txt') as genbanks:
	for line in genbanks:
		try:
			have_dic_or_not=filepaths[line.split()[-1]]
		except:
			filepaths[line.split()[-1]]=''.join((os.path.abspath('genbank'),'/fungi/',line.split()[-1]))
#*********get protein sequence********#
o=open('treatment.log','w')
for i,access in enumerate(filepaths):
	Donebool=False
	try:
		done=open(''.join((filepaths[access],'/',access,'.faa')))
		Donebool=True
	expect:
		print('no final protein found')
	if Donebool:
		continue
#	print(i,access,filepaths[access])
	filedirs=os.listdir(filepaths[access])
	proteinname=''
	dnaname=''
	gffname=''
#	print(filedirs)
	for filename in filedirs:
		if len(filename.split('.'))<2:
			continue
		if filename.split('.')[-2]=='faa':
			proteinname=filename
		if filename.split('.')[-2]=='fna':
			if filename.split('.')[-3].split('_')[-2]!='from':
				dnaname=filename
		if filename.split('.')[-2]=='gff':
			gffname=filename
#	print (proteinname,dnaname,gffname)
	if not dnaname:
		print (access)
		del filepaths[access]
		continue
#*************if protein present, just make pfam annotation***************#
	if proteinname:
		os.system("cp -f {0} {1}".format(''.join((filepaths[access],'/',proteinname)),''.join((filepaths[access],'/',access,'_protein.faa.gz'))))
		os.system("cp -f {0} {1}".format(''.join((filepaths[access],'/',dnaname)),''.join((filepaths[access],'/',access,'_genome.fna.gz'))))
		os.system("cp -f {0} {1}".format(''.join((filepaths[access],'/',gffname)),''.join((filepaths[access],'/',access,'_gff.gz'))))
		os.system("gunzip -qdf {}".format(''.join((filepaths[access],'/',access,'_protein.faa.gz'))))
		os.system("gunzip -qdf {}".format(''.join((filepaths[access],'/',access,'_genome.fna.gz'))))
		os.system("gunzip -qdf {}".format(''.join((filepaths[access],'/',access,'_gff.gz'))))
		proteinname,dnaname,gffname=''.join((access,'_protein.faa')),''.join((access,'_genome.fna')),''.join((access,'_gff'))
		
		os.system("mv {0} {1}".format(''.join((filepaths[access],'/',proteinname)),''.join((filepaths[access],'/',access,'.faa'))))
		print (''.join((filepaths[access],'/',dnaname)))
		os.system("fastformat_nt_nospacetittle.py {}".format(''.join((filepaths[access],'/',dnaname))))
		os.system("mv {0} {1}".format(''.join((filepaths[access],'/',access.split('.')[0],'_format.fasta')),''.join((filepaths[access],'/',access,'.fasta'))))
		os.system("mv {0} {1}".format(''.join((filepaths[access],'/',gffname)),''.join((filepaths[access],'/',access,'.gff'))))
#		print(proteinname)		
#		os.system("pfam_scan.pl -fasta {0} -dir /data/database/func_annotation/pfam/ -outfile {1}".format(''.join((filepaths[access],'/',access,'.faa')),''.join((filepaths[access],'/',access,'.pfam'))))
#**************if protein absent, predict protein use genemarki,then do pfam*************#
	if not proteinname:
		print (i,access,filepaths[access])
		os.system("cp -f {0} {1}".format(''.join((filepaths[access],'/',dnaname)),''.join((filepaths[access],'/',access,'_genome.fna.gz'))))
		os.system("gunzip -qdf {}".format(''.join((filepaths[access],'/',access,'_genome.fna.gz'))))			
		proteinname,dnaname,gffname=''.join((access,'_protein.faa')),''.join((access,'_genome.fna')),''.join((access,'_gff'))
		os.system("fastformat_nt_nospacetittle.py {}".format(''.join((filepaths[access],'/',dnaname))))
		os.system("mv {0} {1}".format(''.join((filepaths[access],'/',access.split('.')[0],'_format.fasta')),''.join((filepaths[access],'/',access,'.fasta'))))
		os.system("perl /data/software/Genemark-ES/gmes_linux_64/gmes_petap.pl  --ES --fungus --cores 40 --min_gene_in_predict 120 --sequence {}".format(''.join((filepaths[access],'/',access,'.fasta'))))
		os.system("perl /data/software/Genemark-ES/gmes_linux_64/get_sequence_from_GTF.pl {0} {1}".format('genemark.gtf',''.join((filepaths[access],'/',access,'.fasta'))))
		os.system("mv nuc_seq.fna {}".format(''.join((filepaths[access],'/',access,'.cds'))))
		os.system("mv prot_seq.faa {}".format(''.join((filepaths[access],'/',access,'.faa'))))
		os.system("mv genemark.gtf {}".format(''.join((filepaths[access],'/',access,'.gtf'))))
		os.system("rm -rf info data output run run.cfg gmhmm.mod gmes.log")
#		os.system("pfam_scan.pl -fasta {0} -dir /data/database/func_annotation/pfam/ -outfile {1}".format(''.join((filepaths[access],'/',access,'.faa')),''.join((filepaths[access],'/',access,'.pfam'))))
#	try:
#		protein_seqs=open(''.join((filepaths[gene],'/',gene,)

	
	o.writelines(''.join((str(i),'\t',access,'\t',filepaths[access],'\n')))
o.close()



