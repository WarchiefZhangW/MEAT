# ZhangW
A biosynthesis gene cluster finding tool

Data preparation:
1. Download genome files as we discribed in ncbi_genome_download.txt.
2. Choose the genomes and make lists named as refseq_dic.txt and genbank_dic.txt for refseq and genbank, respectively.
3. 


Usage:

./MEAT.py query_sequence.fasta (fasta format file) query_pfam.pfam (pfam_scan results) blast_proteins.txt (target for proteins searched by BLAST) $int (window size) $float (pfam domain similarity cutoff)

Example:

cp ~/MEAT/Toy/* ~/MEAT/

./MEAT.py query_sequence.fasta query_pfam.pfam blast_proteins.txt 50000 0.3



Query:


1. BLASTP
2. Augustus
3. Pfam_scan
4. parasail in Python
5. ncbi-genome-download

