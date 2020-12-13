"""
Program for formating the fatsa 
"""

import sys
from optparse import OptionParser

	
# =============================================================================
#                        Read simulated sequences 
# =============================================================================
def readFastaMul(nomFi):
	"""read the fasta file of input sequences"""	
	f=open(nomFi,"r")
	lines=f.readlines()
	f.close()

	seq=""
	nom=""
	lesSeq={}
	for l in lines:
		if l[0] == '>': #attention!!!!!!! there is a space at the beginign of each line 
			if seq != "":
				lesSeq[nom] = seq
			nom=l[1:-1]
			seq=""
		else:
			seq=seq+l[:-1]
	if seq != "":

		lesSeq[nom.rstrip()] = seq.rstrip()
	#print lesSeq.keys()
	return lesSeq
# =============================================================================
#               Rename sequences
# =============================================================================
def rename_seq(dico_seq):
	cluster = {}
	print dico_seq
	count = 1
	for seq in dico_seq.keys(): 
		print seq
		cluster_id = count
		cluster[cluster_id] = seq
		count += 1
	return cluster
# =============================================================================
#               write new fasta file and the correspondance file
# =============================================================================

def write_fasta(cluster_dico, seq_dico, filename):
	fasta_file = open(filename + ".fasta","w")
	corresp_file = open(filename + "_corresp.txt","w")
	for cid in cluster_dico.keys():
		print cluster_dico[cid],"aaaaa"
		header = "S"+str(cid)
		print header
		fasta_file.write(">" + header + "\n")
		fasta_file.write(str(seq_dico[cluster_dico[cid]]) + "\n")
		corresp_file.write(str(header+"\t"+cluster_dico[cid]+"\n"))
	fasta_file.close()
	corresp_file.close()
	return 0

#=============================================================================#
def main():
    usage = "python  Format_fasta.py -f <input fasta> -o <output filename>\n "
    parser = OptionParser(usage)
    parser.add_option("-f", "--input_fasta_File", dest="input_fasta_File",
          help="the unformatted fasta file")
    parser.add_option("-o", "--output_filename", dest="output_filename",
          help="the name of the formatted fasta file and the correspondance file")
    (options, args) = parser.parse_args()
    if len(sys.argv) != 5:
        parser.error("incorrect number of arguments")
    
    input_fasta = options.input_fasta_File
    output_name = options.output_filename
    seq = readFastaMul(input_fasta)
    cluster = rename_seq(seq)
    write_fasta(cluster, seq, output_name)
#=============================================================================#
if __name__ == "__main__":
	main()