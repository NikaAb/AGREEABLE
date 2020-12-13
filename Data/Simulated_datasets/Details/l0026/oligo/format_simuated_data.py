"""
Program to format the IMGT High/v-quest output. The 
"""

import sys
from optparse import OptionParser

# =============================================================================
#               	Read IMGT high/vquest output 
# =============================================================================	

def read_output_file(filename):
	f=open(filename,"r")
	lines=f.readlines()
	f.close()
	return lines

#=============================================================================#

def filterseqclone(lines):
	cluster_dico={}
	for l in range(len(lines)):
		#print lines[l]
		split = lines[l].split("\t")
		cluster = split[1].split("_")
		if str(cluster[1]+"_"+cluster[2]) in cluster_dico.keys():
			cluster_dico[str(cluster[1]+"_"+cluster[2])].append(split[0])
		else:
			cluster_dico[str(cluster[1]+"_"+cluster[2])] = [split[0]] 
	#print cluster_dico
	return cluster_dico

# =============================================================================
#				Write the formatted IMGT/highVquest output 
# =============================================================================	

def sim_format(cluster_dico,formatted_File):
	filetowrite=open(formatted_File,"w")
	compt = 1
	for c in cluster_dico.keys():
		ClusterNum="C"+str(compt)+"\t"
		filetowrite.write(ClusterNum)
		member=cluster_dico[c]
		for m in range(len(member)-1):
			if str(member[m])[0] == "S" :
				filetowrite.write(str(member[m])+" ")
			else :
				filetowrite.write("S"+str(member[m])+" ")
		filetowrite.write("S"+str(member[-1]))
		filetowrite.write("\n")
		compt +=1
	return 0

#=============================================================================#

def main():
    usage = "python  partis_formatter.py -i <simulated coresspondant file> -o <formatted file name>\n "
    parser = OptionParser(usage)
    parser.add_option("-i", "--sim_cor_file", dest="sim_cor_file",
          help="the simulated coresspondant file")
    parser.add_option("-o", "--formatted_file_name", dest="formatted_file_name",
          help="the name for the file to write")
    
    (options, args) = parser.parse_args()
    if len(sys.argv) != 5:
        parser.error("incorrect number of arguments")
    Simulated_clusters = options.sim_cor_file
    formatted_File = options.formatted_file_name
    lines = read_output_file(Simulated_clusters)
    dico_true_cluster=filterseqclone(lines)
    sim_format(dico_true_cluster,formatted_File)
    print ("Done!")

#=============================================================================#

if __name__ == "__main__":
    main()
