# Frequent_Itemsets
A_priori algorithm

In several applications (consumer behavior study, biomarker analysis, plagiarism detection, etc) need to find frequent itemsets. 
One way of finding them is the algorithm of Agrawal and Srikant [(Apriori algorithm)](https://en.wikipedia.org/wiki/Apriori_algorithm). 
In this project, we implement this algorithm.
The baskets of objects contained in a CSV file. Each line of this file has the form: item_1, item_2, ..., item_n.

Τhe program runs in the form: python a_priori.py [-n] [-p] [-o OUTPUT] support filename

- The -n parameter is optional. If given parameter-n, the program will consider that the objects are numbers (not strings). Otherwise 
it considers strings.
- The -p parameter is optional. If given parameter -p, the program considers that the minimum support price given by the -s parameter 
is the percentage of baskets that should be an itemset to be significant.
- The -o OUTPUT parameter is optional. If the -o parameter is given the program will save the results to file OUTPUT. Otherwise it displays 
them on the screen.
- Parameter support is mandatory. With this is given the minimum price support will use the algorithm to characterizing frequent itemset.
- The filename parameter is mandatory. With this is given the name of the input file of the program.
