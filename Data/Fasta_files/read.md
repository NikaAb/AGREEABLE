
Run pear for merge fastq seq 
$ ./pear -f ***\_L001\_R1\_001.fastq.gz -r ***\_L001\_R2\_001.fastq.gz -o Patient\_x


Run seqtk for convert fastq to fasta and rename the seq

$ ./seqtk seq -a ***.assembled.fastq > ***.fasta
$ ./seqtk seq -C ***.fasta > ***.fasta.tmp
$ ./seqtk rename ***.fasta.tmp S > ***.fa