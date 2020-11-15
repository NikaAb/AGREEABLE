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
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import Counter 
from optparse import OptionParser
from itertools import combinations	


#global variables
intersets = [] 
interMaxTrue = []
interPredTrue = []
truePosSets = []
truePosValues = []

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
def preCompTP(SetTrue, SetPred):
	tp = 0
	for sp in SetPred:
		tp = getTps(sp, SetTrue)
		truePosSets.append(sp)
		truePosValues.append(tp)			
	
#===================================================================================
def totalTP(LS):
	tp = 0
	for s0 in LS:
		tp += nCr2(len(s0))
	return tp

#===================================================================================
def preCompIntersets(SetTrue, SetPred):
	for s in SetPred:
		maxI, maxS, interS = maxIntersect(s, SetTrue)
		if maxI >= 2:
			intersets.append(s)
			interMaxTrue.append(maxS)
			interPredTrue.append(interS)

#===================================================================================
def getTPsPreComp(s):

	if s in truePosSets:
		ind = truePosSets.index(s)
		return truePosValues[ind]
	return 0
	

#===================================================================================
def counter_pairwise(SetTrue, SetPred):
	TP,FN,FP=0,0,0;  isTP = False
	i = 0; j = 0; p = 0; STEP = 100

	Ttp = totalTP(SetTrue)
	#print('Ttp ', Ttp)

	for s in SetPred:		
		#TP += getTps(s, SetTrue)	
		TP += getTPsPreComp(s)	
		if len(s) > 1:
			if s in intersets:
				ind = intersets.index(s)
				maxSTrue = interMaxTrue[ind]
				interS = interPredTrue[ind]
				maxI = len(interS)
				#print ('--', maxI, 'len sp', len(s))
				if maxI >= 2: 
					predDifTrue = s.difference(maxSTrue)
					#print ('Pred -True =', predDifTrue)
					FP += (len(predDifTrue) * len(interS))

	return TP,(Ttp - TP), FP

#===================================================================================
def sortPred(SetPred):
	i = 0; j = 1
	SetPredSorted = []
	array = np.zeros((len(SetPred), 2))
	for s in SetPred:
		array[i][0] = len(s)
		array[i][1] = i	
		i = i + 1	
	arrSorted = np.argsort(array[:, 0])

	i = len(arrSorted)
	while (j <= i):
		SetPredSorted.append(SetPred[arrSorted[i-j]])
		j +=1
	return SetPredSorted

#===================================================================================
def removeSinglentons(setSin):
	SetClean = []
	for s in setSin:
		if len(s) > 1:
			SetClean.append(s)
	return SetClean
#===================================================================================
def updateTrue(SetTrue, predRM):
	SetTrueClean =  []; setUp = []
	for s in SetTrue:
		newS = set()
		for es in s:
			if es not in predRM:
				newS.add(es)
			else:
				predRM.remove(es)
		if newS:
			SetTrueClean.append(newS)
			if s!=newS and s in interMaxTrue:
				ind = interMaxTrue.index(s)
				setUp.append(ind)
	
	if len(setUp) > 0:
		for i in setUp:	
			#print ('precomp intersect')
			sp = intersets[i]	
			maxI, maxS, interS = maxIntersect(sp, SetTrueClean)
			interMaxTrue[i] = maxS; interPredTrue[i] = interS
			if sp in truePosSets:
				ind = truePosSets.index(sp)
				truePosValues[ind] = getTps(sp, SetTrueClean)

	return SetTrueClean
#===================================================================================
def saveSetFile(SetData, fileName):
	f = open(fileName, "w")
	for s in SetData:
		if len(s) > 1:
			f.write(str(len(s)) + '\t' + str(s) + "\n")
	f.close()

#===================================================================================
def counter_pairwise_Iter(SetTrue, SetPred, Total):
	TP,FN,FP = 0, 0, 0; arrayF1 = []; arrayI = []; info = ''
	SetPredSorted = sortPred(SetPred)
	SetPredSorted = removeSinglentons(SetPredSorted)
	SetTrue = removeSinglentons(SetTrue)
	preCompIntersets(SetTrue, SetPred)
	preCompTP(SetTrue, SetPred)
	L = len(SetPredSorted)
	LT = len(SetPredSorted)
	for i in range(L):
		print ('counter_pairwise...',  len(SetTrue), len(SetPredSorted),  len(SetTrue)/len(SetPredSorted))
		TP,FN,FP = counter_pairwise(SetTrue, SetPredSorted)
		nbCluster = len(SetPredSorted)
		if TP > 0:
			print (i, '--', 'TP=',TP, 'FN=',FN, 'FP=',FP)
			pre, rec, f1 = Classiq_mesure(TP,FN,FP)
			print ('Pre=',pre, 'Rec=', rec, 'F1', f1)
			info += str(nbCluster/LT)+ '\t'+ str(f1) + "\n"
			#arrayF1.append(f1);arrayI.append(i)
			#print ('nbCluster= ', nbCluster, 'fscore= ', f1)
		
		predRM = SetPredSorted.pop(0)
		#sys.exit()
		#print ('rm', predRM)
		#print ('updating...')
		SetTrue = updateTrue(SetTrue, predRM)
		#print ('updated')
	return info

	
#===================================================================================
def plot(x, y):
	fig, ax = plt.subplots()
	ax.plot(x, y)

	ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
	ax.grid()

	fig.savefig("test.png")
	plt.show()
#===================================================================================
def Classiq_mesure(TP, FN, FP):
	pre = TP/float(TP+FP)
	rec = TP/float(TP+FN)
	return pre, rec,  round(2*pre*rec/(pre + rec), 2)
	
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
	info = counter_pairwise_Iter(HashTrue, HashPredict, nbPairs)
	print ("save", Predicted_File+'.fscores')
	f = open(Predicted_File+'.fscores', "w")
	f.write(info)
	f.close()	

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
