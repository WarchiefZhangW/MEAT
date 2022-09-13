# ZhangW

Mycology Exploring Annotation Tool (MEAT)

A biosynthesis gene cluster (BGC) finding tool

Once you get a BGC, other similar BGCs can be detected in the query genomes by scanning the conserved protein domains and similar proteins sequences.

e.g. You have a BGC that contain a core gene A and other genes B, C, D, E. To explore the similar BGCs in all the query genomes, you can use MEAT to search the conserved domains in A and B. If C, D, and E have no predicted conserved domains, you can explore the similar proteins using BLASTP. You can define the window size for exploration, such as 15 Kb or larger. In addition, the cutoffs of domain similarity and protein similarity can also be definded accoding to their conservation.




Data preparation:
1. Prepare fungal genome data.#This step can be skipped if you download our Fungal-pro database and decompress it here.

1.1. Download genome files as we discribed in ncbi_genome_download.txt. 

1.2. Choose the genomes and make lists named as refseq_dic.txt and genbank_dic.txt for refseq and genbank, respectively.

1.3. Run ln -s ~/MEAT/fastformat_nt_nospacetittle.py /usr/bin       to link the fastformat_nt_nospacetittle.py function.

1.4. Run ./treat_rawdata.py        to prepare the protein sequences.

1.5. Run ./pfam_annot_genbank.py and ./pfam_annot_refseq.py       to prepare pfam annotation.

1.6. Run ./make_blast_database.py     to prepare BLAST database.



2. (Optional) Download Fungal-pro database: https://github.com/WarchiefZhangW/Fungal-pro and decompress here, then skip step 1.





Then MEAT program is prepared. Example in MEAT/Toy/ can help to test this workflow works or not.


Usage:

./MEAT.py query_sequence.fasta (fasta format file) query_pfam.pfam (pfam_scan results) blast_proteins.txt (target for proteins searched by BLAST) $int (window size) $float (pfam domain similarity cutoff)

Example:

cp ~/MEAT/Toy/* ~/MEAT/

./MEAT.py query_sequence.fasta query_pfam_A.pfam blast_proteins_D.txt 50000 0.3



Query:


1. BLASTP
2. Augustus
3. Pfam_scan
4. parasail in Python
5. ncbi-genome-download

