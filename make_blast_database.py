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
	except:
		continue
	os.system("makeblastdb -in {0} -out {1}/protein_blast -dbtype prot".format(''.join((filepaths[access],'/',access,'.faa')),filepaths[access]))
