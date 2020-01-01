#!/usr/bin/env python
# -*- coding: utf-8 -*-
# EECS 349 Machine Learning
# Ding Xiang
from __future__ import division
import numpy as np
import sys
import scipy.stats
import math
import matplotlib.pyplot as plt


def main():
    """
    This function runs your code for problem 2.

    You can also use this to test your code for problem 1,
    but make sure that you do not leave anything in here that will interfere
    with problem 2. Especially make sure that gmm_est does not output anything
    extraneous, as problem 2 has a very specific expected output.
    """
    file_path = sys.argv[1]
    # file_path = "/Users/Rockwell/PycharmProjects/MLHW6/gmm_train.csv"
    # python /Users/Rockwell/PycharmProjects/MLHW6/gmm_est.py /Users/Rockwell/PycharmProjects/MLHW6/gmm_train.csv

    # YOUR CODE FOR PROBLEM 2 GOES HERE
    trainData1, trainData2 = read_gmm_file(file_path)

    # Now you have the training data
    # You can now start doing GMM for each class
    # For Class 1, it uses K=2, mu_init=[10,30], sigmasq_init=[25, 11], wt_init=[0.6, 0.4]
    mu_init1 = [10, 30]
    sigmasq_init1 = [25, 11]
    wt_init1 = [0.6, 0.4]
    its1 = 20
    mu_results1, sigma2_results1, w_results1, L1 = gmm_est(trainData1, mu_init1, sigmasq_init1, wt_init1, its1)
    plt.figure(1)
    plt.plot(L1, '-o')
    plt.ticklabel_format(useOffset=False)
    plt.title("Plot of Log-likelihood in First 20 Iterations for Class 1")
    plt.savefig("likelihood_class1.png")

    # For Class 2, it uses K=3, mu_init=[-25,-5,50], sigmasq_init=[11,25,64], wt_init=[0.3, 0.4, 0.3]
    mu_init2 = [-25, -5, 50]
    sigmasq_init2 = [11, 25, 64]
    wt_init2 = [0.3, 0.4, 0.3]
    its2 = 20
    mu_results2, sigma2_results2, w_results2, L2 = gmm_est(trainData2, mu_init2, sigmasq_init2, wt_init2, its2)
    plt.figure(2)
    plt.plot(L2, 'r-o')
    plt.ticklabel_format(useOffset=False)
    plt.title("Plot of Log-likelihood in First 20 Iterations for Class 2")
    plt.savefig("likelihood_class2.png")

    # mu_results1, sigma2_results1, w_results1 are all numpy arrays
    # with learned parameters from Class 1
    print 'Class 1'
    print 'mu =', mu_results1, '\nsigma^2 =', sigma2_results1, '\nw =', w_results1

    # mu_results2, sigma2_results2, w_results2 are all numpy arrays
    # with learned parameters from Class 2
    print '\nClass 2'
    print 'mu =', mu_results2, '\nsigma^2 =', sigma2_results2, '\nw =', w_results2


def gmm_est(X, mu_init, sigmasq_init, wt_init, its):
    """
    Input Parameters:
      - X             : N 1-dimensional data points (a 1-by-N numpy array)
      - mu_init       : initial means of K Gaussian components (a 1-by-K numpy array)
      - sigmasq_init  : initial  variances of K Gaussian components (a 1-by-K numpy array)
      - wt_init       : initial weights of k Gaussian components (a 1-by-K numpy array that sums to 1)
      - its           : number of iterations for the EM algorithm

    Returns:
      - mu            : means of Gaussian components (a 1-by-K numpy array)
      - sigmasq       : variances of Gaussian components (a 1-by-K numpy array)
      - wt            : weights of Gaussian components (a 1-by-K numpy array, sums to 1)
      - L             : log likelihood
    """

    # YOUR CODE FOR PROBLEM 1 HERE
    # You just need to find out best mu, sigmasq, wt by the iteration formulation
    # Then you can calculate L by that log formulation

    # Ok, first, Expectation Step:
    # You need to know what is K, N
    K = len(mu_init)
    N = len(X)
    # You need to create a matrix (K by N) for gamma_jn
    # to update its value in each iteration
    gamma_jn = np.zeros((K, N))
    # You also need to create array for mu, sigmasq, wt
    # to update from initialization
    mu = mu_init
    sigmasq = sigmasq_init
    wt = wt_init
    # Don't forget Gamma_j that will also be updated in the process
    Gamma_j = np.zeros((1, K))
    # L is used for store the log-likelihood values iterations for problem2
    L = []
    # Start iterations
    for it in range(its):
        # Now you start to calculate each element of gamma_jn
        for j in range(K):
            for n in range(N):
                gamma_jn[j, n] = (wt[j] * scipy.stats.norm(mu[j], np.sqrt(sigmasq[j])).pdf(X[n])) / (sum([wt[k] * scipy.stats.norm(mu[k], np.sqrt(sigmasq[k])).pdf(X[n]) for k in range(K)]))
            # Now you need calculate Gamma_j
            Gamma_j[0, j] = sum(gamma_jn[j, :])
            # Now you can update all the parameters
            wt[j] = Gamma_j[0, j] / float(N)
            sigmasq[j] = (sum([gamma_jn[j, i] * pow((X[i] - mu[j]),2) for i in range(N)])) / float(Gamma_j[0, j])
            mu[j] = (sum([gamma_jn[j, i] * X[i] for i in range(N)])) / float(Gamma_j[0, j])
        # Calculate the log likelihood
        L_each = 0
        for i in range(N):
            L_each += math.log(sum([wt[j] * scipy.stats.norm(mu[j], np.sqrt(sigmasq[j])).pdf(X[i]) for j in range(K)]))
        L.append(L_each)
        # print it
    # print 'the L is:', L_list
    return mu, sigmasq, wt, L


def read_gmm_file(path_to_file):
    """
    Reads either gmm_test.csv or gmm_train.csv
    :param path_to_file: path to .csv file
    :return: two numpy arrays for data with label 1 (X1) and data with label 2 (X2)
    """
    X1 = []
    X2 = []

    data = open(path_to_file).readlines()[1:] # we don't need the first line
    for d in data:
        d = d.split(',')

        # We know the data is either class 1 or class 2
        if int(d[1]) == 1:
            X1.append(float(d[0]))
        else:
            X2.append(float(d[0]))

    X1 = np.array(X1)
    X2 = np.array(X2)

    return X1, X2

if __name__ == '__main__':
    main()
