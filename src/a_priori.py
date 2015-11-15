import csv
import collections
import itertools
import argparse
import sys

parser = argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--numeric", help="items are numeric",
                    action="store_true", default=False)
parser.add_argument("support", help="support threshold")
parser.add_argument("-p", "--percentage",
                    action="store_true", default=False,
                    help="treat support threshold as percentage value")
parser.add_argument("filename", help="input filename")
parser.add_argument("-o", "--output", type=str, help="output file")

args = parser.parse_args()

#A-Priori Algorithm first pass
def aPrioriFirstPass(F, s):
    #a counter collection for the frequencies of each item
    counts = collections.Counter()
    #a dictionary with each item and its frequency
    freq = {}
    #for each basket in input file
    for row in F:
        if args.numeric: #the program consider that the items are numeric
            unique_row_items = list(set([int(field) for field in row]))
        else: #the program consider that the items are string
            unique_row_items = set([field.lower().strip() for field in row])
        #for each unique item increase its frequency
        for unique_item in unique_row_items:
            counts[unique_item] = counts[unique_item] + 1
    #for each item whose frequency is bigger than the support's value, put it in frequency dictionary       
    for unique_item in counts:
        if (counts[unique_item]) >= s:
            freq[(unique_item,)] = counts[unique_item]
    return freq

#A-Priori Algorithm k+1 pass
def aPriorPass(F, freqk, k, s):
    #a counter collection for the frequencies of each item
    counts = collections.Counter()
    #a dictionary with each item and its frequency
    freq = {}
    #for each basket in input file
    for row in F:
        if args.numeric: #the program consider that the items are numeric
            unique_row_items = list(set([int(field) for field in row]))
        else: #the program consider that the items are string
            unique_row_items = set([field.lower().strip() for field in row])
        #creation of item's (k+1) combinations
        pairs = itertools.combinations(freqk, k + 1)
        #the initialization of a list with the cadidate items
        candidates = []
        for pair in pairs:
            #the union of pairs
            candidate = tuple(sorted(set((pair[0])) | set((pair[1]))))
            if candidate not in candidates: #each candidate itemset is used only once
                candidates.append(candidate) #the addition of each new candidate item
                if len(candidate) == k + 1: #each itemset has exactly k+1 items
                    if set(candidate).issubset(set(unique_row_items)): #all items belong to basket where we are
                        counts[candidate] = counts[candidate] + 1
    #for each item whose frequency is bigger than the support's value, put it in frequency dictionary
    for unique_item in counts:
        if (counts[unique_item]) >= s:
            freq[(unique_item)] = counts[unique_item]
    return freq
#if the parameter p is given
if args.percentage:
    count = 0 #the counter of the basket's number
    #reading of the csv file
    input_file = open(args.filename, 'r')
    csv_reader = csv.reader(input_file, delimiter=',')
    for row in csv_reader:
        count = count + 1 #increase the counter of the basket's number
    #calculation of the support
    args.support = (int(args.support) / 100)*count
    
#reading of the csv file    
input_file = open(args.filename, 'r')
csv_reader = csv.reader(input_file, delimiter=',')


all_freq = [] #the initialization of a list with all items' frequencies
k = 1 #for the first pass
freqk = aPrioriFirstPass(csv_reader, int(args.support)) #call the method for the first pass
input_file.close()
while len(freqk) is not 0:
    all_freq.append(freqk)
    #reading of the csv file 
    input_file = open(args.filename, 'r')
    csv_reader = csv.reader(input_file, delimiter=',')
    #call the method for the (k+1) pass
    freq = aPriorPass(csv_reader, freqk, k, int(args.support))
    input_file.close()
    freqk = freq
    k = k + 1 #for the (k+1) passes
    
k = False
#for each argument if there is some with value -o then write a csv file
for arg in sys.argv:
    if arg == '-o':
        k = True
        #writing of the results to the csv file
        output_file = open(args.output, 'w')
        csv_writer = csv.writer(output_file, delimiter=';')
        for row in all_freq:
            mlist = []
            unique_key = list(set([field for field in row]))
            for key in sorted(unique_key):
                mlist.append("{0}:{1}".format(key, row[key]))
            csv_writer.writerow(mlist)
        output_file.close()        
if k == False: #printing of the results
    csv_writer = csv.writer(sys.stdout, delimiter=';')
    for row in all_freq:
        mlist = []
        unique_key = list(set([field for field in row]))
        for key in sorted(unique_key):
            mlist.append("{0}:{1}".format(key, row[key]))
        csv_writer.writerow(mlist)
