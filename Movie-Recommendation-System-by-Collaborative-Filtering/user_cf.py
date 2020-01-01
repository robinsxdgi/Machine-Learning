# -*- coding: utf-8 -*-
# Starter code for uesr-based collaborative filtering
# Complete the function user_based_cf below. Do not change it arguments and return variables. 
# Do not change main() function, 

# How to use terminal for this code:
# python '/Users/Rockwell/PycharmProjects/MLHW4/user_cf.py' '/Users/Rockwell/PycharmProjects/MLHW4/ml-100k/u.data' 4 55 0 3 1

# import modules you need here.
import sys
import csv
import numpy as np
import scipy.stats
import random

def user_based_cf(datafile, userid, movieid, distance, k, iFlag, numOfUsers, numOfItems):
    '''
    build user-based collaborative filter that predicts the rating 
    of a user for a movie.
    This function returns the predicted rating and its actual rating.
    
    Parameters
    ----------
    <datafile> - a fully specified path to a file formatted like the MovieLens100K data file u.data 
    <userid> - a userId in the MovieLens100K data
    <movieid> - a movieID in the MovieLens 100K data set
    <distance> - a Boolean. If set to 0, use Pearson’s correlation as the distance measure. If 1, use Manhattan distance.
    <k> - The number of nearest neighbors to consider
    <iFlag> - A Boolean value. If set to 0 for user-based collaborative filtering, 
    only users that have actual (ie non-0) ratings for the movie are considered in your top K. 
    For user-based, use only movies that have actual ratings by the user in your top K. 
    If set to 1, simply use the top K regardless of whether the top K contain actual or filled-in ratings.
    <numOfUsers> - the number of users in the dataset 
    <numOfItems> - the number of items in the dataset
    (NOTE: use these variables (<numOfUsers>, <numOfItems>) to build user-rating matrix. 
    DO NOT USE any CONSTANT NUMBERS when building user-rating matrix. We already set these variables in the main function for you.
    The size of user-rating matrix in the test case for grading could be different from the given dataset. )

    returns
    -------
    trueRating: <userid>'s actual rating for <movieid>
    predictedRating: <userid>'s rating predicted by collaborative filter for <movieid>


    AUTHOR: Ding Xiang
    '''
    # read datafile
    csvfile = open(datafile, 'rb')
    dat = csv.reader(csvfile, delimiter='\t')
    # store each rating to a correct position in a rating matrix
    # create a matrix
    # The matrix size is number of users by number of movies
    ratingMat = np.zeros((numOfUsers, numOfItems), dtype='int')
    # assign the rating data to the corresponding element of matrix
    for row in dat:
        ratingMat[int(row[0])-1, int(row[1])-1] = int(row[2])
    # No matter which i to choose, i.e no matter use 0 or non-0
    # first calculate each distance between each user to the target user
    # make all the distance to a list, which has numberOfUsers elements
    # but one thing need to differentiate
    # if distance is 0 use Pearson's correlation, if 1 use Manhattan distance
    disList = []
    if distance == 0:
        for i in range(numOfUsers):
            eachDis = scipy.stats.pearsonr(ratingMat[i, :], ratingMat[userid-1, :])[0]
            disList.append(eachDis)
    else:
        for i in range(numOfUsers):
            eachDis = np.sum(np.absolute(ratingMat[i, :] - ratingMat[userid-1, :]))
            disList.append(eachDis)
    # find the K nearest users
    # if i is 0, then only consider the users with non-0 rating for the movie
    # if i is 1, then consider all users no matter non-0 or not
    # One way is first to sort the disList in an ascending order
    # Also save the index of the sorted disList
    # Then check which is the first K users by distinguishing iFlag
    if distance == 0:
        # The larger Pearson's coefficient is, the similar two users will be
        sortDisList = sorted(disList, reverse=True)
        sortIndex = sorted(range(len(disList)), key=lambda l: disList[l], reverse = True)
    else:
        # The smaller Manhattan's distance is, the similar two users will be
        sortDisList = sorted(disList)
        sortIndex = sorted(range(len(disList)), key=lambda l: disList[l])
    # notice that this list also include the distance one to oneself
    # which is usually the first nearest element in the list
    # so we need to take it away
    k_temp = 1
    k_real = 0
    k_rateList = []
    if iFlag == 0:
        while (k_real < k) and (k_temp < numOfUsers):
            # (It's possible that k is larger than non-0 amount of users, in this case, stop after going through all users )
            # check all qualified first k users
            # first of all, remove the user oneself
            # start from the 2nd element
            if ratingMat[sortIndex[k_temp], movieid - 1] == 0:
                k_temp += 1
            else:
                k_rateList.append(ratingMat[sortIndex[k_temp], movieid - 1])
                k_real += 1
                k_temp += 1
    else:
        while k_real < k:
            # just need to remove the user oneself
            # start from the 2nd element
            k_rateList.append(ratingMat[sortIndex[k_temp], movieid - 1])
            k_real += 1
            k_temp += 1
    # Now we get the k nearest users' list reviews to the movie
    # it is saved in k_rateList
    # Next, find out the mode of the top K neighbors
    if k_rateList == []:
        predictedRating = random.randint(1,5)
    else:
        predictedRating = int(scipy.stats.mode(k_rateList)[0])
    trueRating = ratingMat[userid - 1, movieid - 1]
    return trueRating, predictedRating


def main():
    # Some simplified command here for a convenient test
    # datafile = '/Users/Rockwell/PycharmProjects/MLHW4/ml-100k/u.data'
    # userid = 1
    # movieid = 4
    # distance = 1
    # k = 3
    # i = 1

    datafile = sys.argv[1]
    userid = int(sys.argv[2])
    movieid = int(sys.argv[3])
    distance = int(sys.argv[4])
    k = int(sys.argv[5])
    i = int(sys.argv[6])

    # Get the total number of users and items from data file
    csvfile = open(datafile, 'rb')
    dat_temp = csv.reader(csvfile, delimiter='\t')
    userList = []
    itemList = []
    for row in dat_temp:
        userList.append(int(row[0]))
        itemList.append(int(row[1]))
    numOfUsers = max(userList)
    numOfItems = max(itemList)
    
    trueRating, predictedRating = user_based_cf(datafile, userid, movieid, distance, k, i, numOfUsers, numOfItems)
    print 'userID:{} movieID:{} trueRating:{} predictedRating:{} distance:{} K:{} I:{}'\
    .format(userid, movieid, trueRating, predictedRating, distance, k, i)




if __name__ == "__main__":
    main()