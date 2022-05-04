#!/data/software/conda/bin/python3.7
from __future__ import division
import os,sys,time
#********extract path*********#
#print (os.path.abspath('genbank'))
filepaths={}
with open('refseq_dic.txt') as refseqs:
	for line in refseqs:
		filepaths[line.split()[-1]]=''.join((os.path.abspath('refseq'),'/fungi/',line.split()[-1]))
#*********do pfam 15 species per time********#
o=open('pfam_ref_treatment.log','w')
for i,access in enumerate(filepaths):
	print (i,i % 2)
	print(i,access,filepaths[access])
	filedirs=os.listdir(filepaths[access])
	proteinname=''.join((filepaths[access],'/',access,'.faa'))
#*************if protein present, just make pfam annotation***************#
	try:
		proteins=open(proteinname)
	except:
		print('No such protein\n')
		continue
	os.system("nohup pfam_scan.pl -fasta {0} -dir /data/database/func_annotation/pfam/ -outfile {1} & \n\n\n\n".format(''.join((filepaths[access],'/',access,'.faa')),''.join((filepaths[access],'/',access,'.pfam'))))
	o.writelines(''.join((str(i),'\t',access,'\t',filepaths[access],'\n')))
	if not i % 20 and i:
		while True:
			bool=True
			for t,species in enumerate(filepaths):
				if t<=i and t>i-20:
					try:
						pfam_an=open(''.join((filepaths[species],'/',species,'.pfam')))
					except:
						bool=False
				if t>i:
					break
			if not bool:
				print(i,'not finished',time.time())
				time.sleep(20)
			if bool:
				break

o.close()
