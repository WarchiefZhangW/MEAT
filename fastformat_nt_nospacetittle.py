#!/data/software/conda/envs/tensorenviron/bin/python
print ('a')
import os,sys
seqs=open(sys.argv[1]).readlines()
filepath=os.path.abspath(sys.argv[1])

filename=sys.argv[1].split('/')[-1]
filepath=filepath[:0-len(filename)]
out=''
spename=''
try:
	spename=sys.argv[2]
	print ('Using species name:',spename)
except:
	print ('No species name')
for seq in seqs:
	if not seq:
		continue
	if seq[0]=='>' and out!='':
		if spename:
#			print (spename)
			out+='\n'+'>'+spename+'_'+seq[1:].split()[0]+'\n'
			continue
		if not spename:
			out+='\n'+seq.split()[0]+'\n'
			continue
	if out=='':
		if spename:
			out+='>'+spename+'_'+seq[1:].split()[0]+'\n'
			continue
		if not spename:
			out+=seq.split()[0]+'\n'
			continue
	out+=seq.strip()
output=open(''.join((filepath,filename.split('.')[0],'_format.fasta')),'w')
output.writelines(out)
output.close()
seqs=open(''.join((filepath,filename.split('.')[0],'_format.fasta'))).readlines()
out2=''
for n in range(0,int(len(seqs)/2)):
	out2+=seqs[2*n][:-1]+'\t'+str(len(seqs[2*n+1]))+'\n'
output2=open(''.join((filepath,filename.split('.')[0],'_info.txt')),'w')
output2.writelines(out2)
output2.close()
