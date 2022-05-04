#!/data/software/conda/bin/python3.7
from __future__ import division
import os,sys,time
#********extract path*********#
#print (os.path.abspath('genbank'))
filepaths={}
with open('genbank_dic.txt') as genbankseqs:
	for line in genbankseqs:
		filepaths[line.split()[-1]]=''.join((os.path.abspath('genbank'),'/fungi/',line.split()[-1]))
#*********do pfam 15 species per time********#
o=open('pfam_gen_treatment.log','w')
for i,access in enumerate(filepaths):
	pfamdone=False
	print (i,i % 2)
	print(i,access,filepaths[access])
	filedirs=os.listdir(filepaths[access])
	proteinname=''.join((filepaths[access],'/',access,'.faa'))
	pfamname=''.join((filepaths[access],'/',access,'.pfam'))
#*************if protein present, just make pfam annotation***************#
	try:
		proteins=open(proteinname)
	except:
		print('No such protein\n')
		continue
	try:
		pfamanno=open(pfamname)
		print('Pfam exit',pfamname)
		pfamdone=True
	except:
		print('Start doing Pfam',proteinname)
	if pfamdone:
		continue
	os.system("nohup pfam_scan.pl -fasta {0} -dir /data/database/func_annotation/pfam/ -outfile {1} & \n\n\n\n".format(''.join((filepaths[access],'/',access,'.faa')),''.join((filepaths[access],'/',access,'.pfam'))))
	o.writelines(''.join((str(i),'\t',access,'\t',filepaths[access],'\n')))
	if not i % 40 and i:
		while True:
			leavenum=0
			bool=True
			proteinbool=True
			for t,species in enumerate(filepaths):
				proteinbool=True
				if t<=i and t>i-20:
					try:
						protein=open(''.join((filepaths[species],'/',species,'.faa')))
					except:
						proteinbool=False
					try:
						
						pfam_an=open(''.join((filepaths[species],'/',species,'.pfam')))
					except:
						if proteinbool:
							leavenum+=1
				if t>i:
					break
			if not bool:
				print(i,'not finished',time.time())
				time.sleep(20)
			if leavenum<3:
				break

o.close()
