Three files should be prepared for MEAT
1. query_fasta file: using all the proteins seuqences in .fasta format
2. Pfam_annotation file: run pfam_scan.pl for the query_fasta, and remove the results lines for domains that are NOT nessary for the BGC exploration using domain similarity.
3. BLASTP_target file: three columns are 1) protein names in query_fasta file; 2) protein annotations; 3) the protein similarity cutoff. Use \tab to separate.
