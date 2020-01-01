# You've already create the list of each user's movie lists.
# The lists of lists name is "eachUserMovie.txt"
# Now you can draw pictures on this data

import sys
import csv
import numpy as np
import operator
import time
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# First of all
# You need to read the data

def main():
    datafile = 'eachUserMovie.txt'
    numOfUsers = 943
    numOfItems = 1682
    # read in csv file into np.arrays
    csvfile = open(datafile, 'rb')
    dat = csv.reader(csvfile, delimiter='\n')
    #
    #
    Data = []
    listOut = []
    for row in dat:
        # OK, now you know that row[0] is the strings of all movie numbers
        # you need to convert the strings to integers
        # you can use .split
        # make a new listIn for each user
        listIn = []
        row_string = row[0]
        for i in row_string.split(', '):
            i = int(i)
            listIn.append(i)
        listOut.append(listIn)
    # print len(listOut)
    # Great! Now you get the listOut that can be used in the future!

    #I will let you make an array:
    #pair_left, pair_right, common_number

    pair_left = []
    pair_right = []
    common_number = []
    for i in range(0, numOfUsers):
        for j in range(i + 1, numOfUsers):
            pair_left.append(i)
            pair_right.append(j)
    # print len(pair_left)
    totalPairNum = len(pair_left)
    # you need to calculate common_number for each pair

    print 'Now you are starting to find the review in common'
    start = time.time()
    print 'start',start
    for k in range(0, totalPairNum):
        # you need to first find all items reviewed by each pair_left
        print (pair_left[k], pair_right[k])
        common_number.append(len(set(listOut[pair_left[k]]) & set(listOut[pair_right[k]])))

    end = time.time()
    print 'end', end
    print end - start
    print sum(common_number)/float(totalPairNum)

    # Now you need to find the median of common_number
    # But you know that since this is python 2.7
    # so there's no available package to use
    # However, you can sort the list and find the element in the middle
    sortCommon = sorted(common_number)
    median = sortCommon[int(float(len(sortCommon))/2)]
    print 'The median is:', median

    # Now let's plot the histogram
    # The good news is we have histogram function
    num_bins = 3
    n, bins, patches = plt.hist(common_number, num_bins, facecolor='blue', alpha=0.5)
    plt.title('Histogram of number of movies reviewed in common')
    plt.xlabel('Number of movies reviewed in common')
    plt.ylabel('Number of pairs of users')
    plt.show()

    # They ask me to show the reason I choose bin 350
    # So you need to give me what's the largest number of common_number
    print 'largest Common Number:', max(common_number)




if __name__ == "__main__":
    main()