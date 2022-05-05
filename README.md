# ZhangW


A biosynthesis gene cluster (BGC) finding tool

Once you get a BGC, other similar BGCs can be detected in the query genomes by scanning the conserved protein domains and similar proteins sequences.

e.g. You have a BGC that contain a core gene A and other genes B, C, D, E. To explore the similar BGCs in all the query genomes, you can use MEAT to search the conserved domains in A and B. If C, D, and E have no predicted conserved domains, you can explore the similar proteins using BLASTP. You can define the window size for exploration, such as 15 Kb or larger. In addition, the cutoffs of domain similarity and protein similarity can also be definded accoding to their conservation.




Data preparation:
1. Download genome files as we discribed in ncbi_genome_download.txt.
3. Choose the genomes and make lists named as refseq_dic.txt and genbank_dic.txt for refseq and genbank, respectively.
4. Run ln -s ~/MEAT/fastformat_nt_nospacetittle.py /usr/bin       to link the fastformat_nt_nospacetittle.py function.
5. Run ./treat_rawdata.py        to prepare the protein sequences.
6. Run ./pfam_annot_genbank.py and ./pfam_annot_refseq.py       to prepare pfam annotation
7. Run ./make_blast_database.py     to prepare BLAST database

Then MEAT program is prepared. Example in Toy can help to test this workflow works or not.


Usage:

./MEAT.py query_sequence.fasta (fasta format file) query_pfam.pfam (pfam_scan results) blast_proteins.txt (target for proteins searched by BLAST) $int (window size) $float (pfam domain similarity cutoff)

Example:

cp ~/MEAT/Toy/* ~/MEAT/

./MEAT.py query_sequence.fasta query_pfam.pfam blast_proteins_D.txt 50000 0.3



Query:


1. BLASTP
2. Augustus
3. Pfam_scan
4. parasail in Python
5. ncbi-genome-download

