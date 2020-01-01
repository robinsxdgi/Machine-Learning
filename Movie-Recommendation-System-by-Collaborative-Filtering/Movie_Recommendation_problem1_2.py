import sys
import csv
import numpy as np
import operator
import time
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def main():
    datafile = 'u.data'
    numOfUsers = 943
    numOfItems = 1682
    # read in csv file into np.arrays X1, X2, Y1, Y2
    csvfile = open(datafile, 'rb')
    dat = csv.reader(csvfile, delimiter='\t')
    #
    #
    # print type(dat)
    itemID = []
    for row in dat:
        itemID.append(int(row[1]))
    print sorted(itemID)
    pairNum = 0
    # You need to find the number of reviews for each movie
    # And put these review numbers into a list
    # If you want to find the number of reviews for each movie
    # You need to count the number of movie item appears
    # I want you to name number of reviews as numReview
    # Name the list as listNumReview
    numReview = 0
    listNumReview = []
    for j in range(1,numOfItems+1):
        if itemID.count(j) > 0:
            numReview = itemID.count(j)
        else:
            numReview = 0
        listNumReview.append(numReview)
    # print 'listNumReview', listNumReview
    # print len(listNumReview)
    # print listNumReview.index(min(listNumReview))
    # lowestList = []
    # for i, ele in enumerate(listNumReview):
    #     if listNumReview[i] == 1:
    #         lowestList.append(i+1)
    # print lowestList


    # Now you need to plot the listNumReview in a descending order
    listNumReviewRev = sorted(listNumReview, reverse=True)
    plt.plot(listNumReviewRev)
    plt.title('Plot of number of reviews for each movie')
    plt.xlabel('Movie number in order by the number of reviews')
    plt.ylabel('Number of review')
    plt.show()

    # totalPair = numOfUsers * (numOfUsers - 1) / 2
    # meanPair = float(pairNum) / totalPair
    # print 'pairNum', pairNum
    # print 'totalPair', totalPair
    # print 'meanPair', meanPair

    # I will let you make an array:
    # pair_left, pair_right, common_number

    # pair_left = []
    # pair_right = []
    # common_number = []
    # for i in range(0, numOfUsers):
    # # for i in range(0, 3):
    #     for j in range(i + 1, numOfUsers):
    #         pair_left.append(i)
    #         pair_right.append(j)
    # print len(pair_left)
    # totalPairNum = len(pair_left)
    # you need to calculate common_number for each pair
    # but you calculate it too slowly
    # so I need you to do some change

    # This time you need to first make a list for each user's movies
    # Then put those lists into a new list
    # So I want you make a list of list
    # The each list represent a user
    # And make it in user number order

    # listOut = []
    # listIn = []
    # print 'First, you need to make a simple lists of lists for 1 min...'
    # for i in range(numOfUsers):
    # # for i in range(3):
    #     listIn = [int(row[1]) for row in Data if int(row[0]) == i + 1]
    #     listOut.append(listIn)
    #     print i
    # print len(listOut)
    #
    # # You need to save this list of list into a file
    # # I think the file name could be "eachUserMovie.txt"
    # writingWord = open('eachUserMovie.txt', 'w')
    # for word in listOut:
    #     # find correct spells for each checked word
    #     writingWord.write("%s\n" % word)
    # writingWord.close()

    # print 'Now you are starting to find the review in common'
    # start = time.time()
    # print 'start',start
    # for k in range(0, totalPairNum):
    # # for k in range(0, 2):
    #     # you need to first find all items reviewed by each pair_left
    #     print pair_left[k]
    #     print pair_right[k]
    #     # listLeft = [int(row[1]) for row in Data if int(row[0]) == pair_left[k]]
    #     # listRight = [int(row[1]) for row in Data if int(row[0]) == pair_right[k]]
    #     common_number.append(len(set(listOut[pair_left[k]]) & set(listOut[pair_right[k]])))

    # end = time.time()
    # print 'end', end
    # print end - start
    # print sum(common_number)/float(totalPairNum)



if __name__ == "__main__":
    main()