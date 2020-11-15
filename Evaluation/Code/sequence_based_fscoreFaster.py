"""
This script compares real clusters and predicted clusters content and measure 
precision and recall.

The comparison is based on method explained in method file. 

True cluster's file and predicted cluster's file have the same format:

1	a b
2	c e
3	d

The first column shows the cluster label and the second one represents sequences 
in that cluster, separated by space.
Two columns are seperated by \t.
"""


import sys
import math
from collections import Counter 
from optparse import OptionParser
from itertools import combinations	

SEP = '@'

#===================================================================================
def nCr2(n):
    return (n*(n-1))/2
#===================================================================================
def read_output_file(filename):
	f=open(filename,"r")
	lines=f.readlines()
	f.close()
	return lines

#===================================================================================
def createSet(lines):
	SetsTrue=[]; 
	totalSeq = 0; totalPairs = 0
	for l in lines:
		label=l.split("\t")[0]
		sequences=l.split("\t")[1].rstrip().split(" ")
		#print (sequences)
		totalSeq = totalSeq + len(sequences)
		SetsTrue.append(set(sorted(sequences)))
	#print ('ST', SetsTrue)
	total = nCr2(totalSeq)
		
	return SetsTrue, total
#===================================================================================
def maxIntersect(s, LS):
	maxI = -1; maxS = set()
	for s0 in LS:
		i = s0.intersection(s)
		if len(i) > maxI:
			maxI = len(i)
			maxS = s0
			interS = i
			
	return maxI, maxS, interS
#===================================================================================
def getTps(s, LS):
	tp = 0
	for s0 in LS:
		i = s0.intersection(s)
		if len(i) >= 2:
			tp += nCr2(len(i))			
	return tp
#===================================================================================
def totalTP(LS):
	tp = 0
	for s0 in LS:
		tp += nCr2(len(s0))
	return tp

#===================================================================================
def counter_pairwise(SetTrue,SetPred, Total):
	TP,FN,FP=0,0,0;  isTP = False
	i = 0; j = 0; p = 0; STEP = 100

	Ttp = totalTP(SetTrue)

	#print ("nbSet", len(SetTrue))
	for s in SetPred:
		TP += getTps(s, SetTrue)
		if len(s) > 1:
			maxI, maxS, interS = maxIntersect(s, SetTrue)
			#print ('--', maxI, interS)
			predDifTrue = set()
			if maxI >= 2: 
				predDifTrue = s.difference(maxS)
			#print ('Pred -True =', predDifTrue)
			FP += (len(predDifTrue) * len(interS))

		
	#print ('TP', TP); print ('FP', FP); print ('FN', (Ttp - TP))

	return TP,(Ttp - TP),FP
#===================================================================================
def Classiq_mesure(TP,FN,FP, TN):
	pre = TP/float(TP+FP)
	rec = TP/float(TP+FN)
	print ("TP :", TP)
	print ("FN :", FN)
	print ("FP :",FP)
	print ("TN :",TN)
	print ("Recall : ", rec)
	print ("Precision : ", pre)
	print ("F1-score : ", round(2*pre*rec/(pre + rec),2))
	return 0
#===================================================================================
def precision_recall(Predicted_File,True_file):
	print ("reading Predicted_File")
	predicted_lines=read_output_file(Predicted_File)
	print ("reading True file")
	real_lines=read_output_file(True_file)
	print ("Creating  True Hash")
	HashTrue, nbPairs = createSet(real_lines)
	
	print ("Creating  Pred Hash")
	HashPredict, _ = createSet(predicted_lines)
	#TP,FN,FP=counter(seq_predicted_cluster,HashTrue,HashPredict,label_seq_True)
	print ("Count TP, TF, TN")
	TP,FN,FP = counter_pairwise(HashTrue,HashPredict, nbPairs)
	
	TN = nbPairs - (TP + FN + FP)
	Classiq_mesure(TP,FN,FP, TN) 
	return 0			
#===================================================================================
#			    		Main
#===================================================================================
def main():
    usage = usage = "python sequence_based_fscore.py -p <clustering output> -t <true cluster file> \n"
    parser = OptionParser(usage)
    parser.add_option("-p", "--Predicted_Files_File", dest="Predicted_Files_File",
          help="read clusters from Predicted_File")
    parser.add_option("-t", "--True_clusters_file", dest="True_clusters_file",
          help="read data from True clusters file")
    
    (options, args) = parser.parse_args()
    if len(sys.argv) != 5:
        parser.error("incorrect number of arguments")
    
    Predicted_File = options.Predicted_Files_File
    True_file = options.True_clusters_file
    precision_recall(Predicted_File,True_file)

#===================================================================================
if __name__ == "__main__":
    main()
