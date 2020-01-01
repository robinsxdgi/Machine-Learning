#!/usr/bin/env python
# -*- coding: utf-8 -*-
# EECS 349 Machine Learning
# Ding Xiang
from __future__ import division
import numpy as np
import sys
import scipy.stats
import matplotlib.pyplot as plt
from gmm_est import gmm_est


def main():
    """
    This function runs your code for problem 3.

    You can use this code for problem 4, but make sure you do not
    interfere with what you need to do for problem 3.
    """

    # python gmm_classify.py "/Users/Rockwell/PycharmProjects/MLHW6/gmm_test.csv"
    file_path = sys.argv[1]

    # file_path = "/Users/Rockwell/PycharmProjects/MLHW6/gmm_test.csv"
    testDataAll, testData1, testData2 = read_gmm_file(file_path)
    # YOUR CODE FOR PROBLEM 3 GOES HERE
    mu1 = [9.7748859236208396, 29.582587182945414]
    sigmasq1 = [21.922804563227473, 9.7837696129445995]
    wt1 = [0.59765463038641087, 0.40234536961368628]

    mu2 = [-24.822751728696254, -5.0601582832343865, 49.624444719527624]
    sigmasq2 = [7.9473354077562393, 23.322661814350976, 100.02433750441195]
    wt2 = [0.20364945852723454, 0.49884302379593665, 0.29750751767685862]

    # You need to calculate p1 later
    p1 = 1/float(3)

    classlabel = gmm_classify(testDataAll, mu1, sigmasq1, wt1, mu2, sigmasq2, wt2, p1)
    np.set_printoptions(threshold='nan')
    # print testDataAll
    class1_data = [round(testDataAll[i],2) for i in range(len(classlabel)) if classlabel[i] == 1]
    class2_data = [round(testDataAll[i],2) for i in range(len(classlabel)) if classlabel[i] == 2]

    # class1_data is a numpy array containing
    # all of the data points that your gmm classifier
    # predicted will be in class 1.
    print 'Class 1'
    print class1_data

    # class2_data is a numpy array containing
    # all of the data points that your gmm classifier
    # predicted will be in class 2.
    print '\nClass 2'
    print class2_data


def gmm_classify(X, mu1, sigmasq1, wt1, mu2, sigmasq2, wt2, p1):
    """
    Input Parameters:
        - X           : N 1-dimensional data points (a 1-by-N numpy array)
        - mu1         : means of Gaussian components of the 1st class (a 1-by-K1 numpy array)
        - sigmasq1    : variances of Gaussian components of the 1st class (a 1-by-K1 numpy array)
        - wt1         : weights of Gaussian components of the 1st class (a 1-by-K1 numpy array, sums to 1)
        - mu2         : means of Gaussian components of the 2nd class (a 1-by-K2 numpy array)
        - sigmasq2    : variances of Gaussian components of the 2nd class (a 1-by-K2 numpy array)
        - wt2         : weights of Gaussian components of the 2nd class (a 1-by-K2 numpy array, sums to 1)
        - p1          : the prior probability of class 1.

    Returns:
        - class_pred  : a numpy array containing results from the gmm classifier
                        (the results array should be in the same order as the input data points)
    """

    # YOUR CODE FOR PROBLEM 3 HERE
    # You need to compare the possibilities with two different classes of GMMs
    # The one with higher probability assigns the corresponding class to the test data
    # First you need to calculate probability for all data with class1 GMM
    prob1 = np.zeros((1,len(X)))
    for i in range(len(wt1)):
        prob1 += wt1[i] * scipy.stats.norm(mu1[i], np.sqrt(sigmasq1[i])).pdf(X)
    # Then calculate probability for all data with class2 GMM
    prob2 = np.zeros((1, len(X)))
    for i in range(len(wt2)):
        prob2 += wt2[i] * scipy.stats.norm(mu2[i], np.sqrt(sigmasq2[i])).pdf(X)
    # Compare the results prob1 and prob2
    # If prob1 < prob2 then label as Class 2
    # Otherwise, class 1
    class_pred = ((prob1 < prob2) + 1)[0]

    return class_pred


def read_gmm_file(path_to_file):
    """
    Reads either gmm_test.csv or gmm_train.csv
    :param path_to_file: path to .csv file
    :return: two numpy arrays for data with label 1 (X1) and data with label 2 (X2)
    """
    X = [] # Store for all data
    X1 = []
    X2 = []

    data = open(path_to_file).readlines()[1:] # we don't need the first line
    for d in data:
        d = d.split(',')

        X.append(float(d[0]))

        # We know the data is either class 1 or class 2
        if int(d[1]) == 1:
            X1.append(float(d[0]))
        else:
            X2.append(float(d[0]))

    X = np.array(X)
    X1 = np.array(X1)
    X2 = np.array(X2)

    return X, X1, X2

if __name__ == '__main__':
    main()
