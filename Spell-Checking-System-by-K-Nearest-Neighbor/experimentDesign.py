# EECS 349 Machine Learning, Spell Checking System 3.2
# Ding Xiang
# October,1,2017
#########################
# python spellcheck.py '/Users/Rockwell/PycharmProjects/MLHW2/3esl.txt' 3esl.txt
# python spellcheck.py '/Users/Rockwell/PycharmProjects/MLHW2/wrongwords.txt' 3esl.txt
# python spellcheck.py '/Users/Rockwell/PycharmProjects/MLHW2/wikipediatypoclean.txt' 3esl.txt
# python spellcheck.py '/Users/Rockwell/PycharmProjects/MLHW2/wikicompact.txt' 3esl.txt

import numpy
import sys
import csv
import re
import time
import random

def find_closest_word(string1, dictionary, deletion_cost, insertion_cost, substitution_cost): # dictionary is a list of strings consists of correct words
    closestWord = dictionary[0]
    closestDistance = levenshtein_distance(string1, dictionary[0], deletion_cost, insertion_cost, substitution_cost)
    for i in range(len(dictionary)):
        # Before we get into calculation of levenshtein distance
        # We could add a length checking step, to filter out the words that doesn't have prerequisite being candidates
        if abs(len(dictionary[i])-len(string1)) < closestDistance:
            if closestDistance > levenshtein_distance(string1, dictionary[i], deletion_cost, insertion_cost, substitution_cost): # We first consider the case that three costs equal to 1, if the new word has closer distance to the word, then we replace the closest word by this new one.
                closestWord = dictionary[i]
                closestDistance = levenshtein_distance(string1, dictionary[i], deletion_cost, insertion_cost, substitution_cost)
    return closestWord

# Levenshtein_distance function
def levenshtein_distance(string1, string2, deletion_cost, insertion_cost, substitution_cost):
    M = numpy.zeros((len(string1) + 1, len(string2) + 1)) # M has (m+1) by (n+1) values
    for i in range(len(string1) + 1):
        M[i][0] = i * deletion_cost # Distance of any 1st string to an empty 2nd string
    for j in range(len(string2) + 1):
        M[0][j] = j * insertion_cost # Distance of any 2nd string to an empty 1st string
    for j in range(1, len(string2) + 1):
        for i in range(1, len(string1) + 1):
            if string1[i-1] == string2[j-1]:
                M[i][j] = M[i-1][j-1] # No operation cost, because they match
            else:
                M[i][j] = min(M[i-1][j]+deletion_cost, M[i][j-1]+insertion_cost, M[i-1][j-1]+substitution_cost)
    return M[len(string1), len(string2)] # Return distance

# Define measure error function
def measure_error(typos, trueWords, dictionaryWords, deletion_cost, insertion_cost, substitution_cost):
    errorNumber = 0
    for index, word in enumerate(typos):
        if find_closest_word(word, dictionaryWords, deletion_cost, insertion_cost, substitution_cost) != trueWords[index]: # If the true word doesn't match the closest word then add 1 to error number
            errorNumber += 1
    errorRate = float(errorNumber) / float(len(typos)) # Calculate the error rate
    return errorRate

def main():

    wordCheckedAndTrue = open('wikipediatypoclean.txt') # Input the file to be spell-checked
    checkedAndTrueWords = csv.reader(wordCheckedAndTrue)
    listCheckedAndTrueWords = []
    for eachCheckedAndTrueWord in checkedAndTrueWords:
        listCheckedAndTrueWords.append(eachCheckedAndTrueWord)
    random.shuffle(listCheckedAndTrueWords)
    subCheckedAndTrueWords = listCheckedAndTrueWords[0:10]

    wordDictionary = open('3esl.txt') # Input the dictionary word list
    dictionaryWords = csv.reader(wordDictionary)

    # Create a list of words in dictionary
    dictionaryWordList = []
    for row in dictionaryWords:
        # We just pick the list with first letter 'a', 'b' or 'c'
        if row[0][0] == 'a' or row[0][0] == 'b' or row[0][0] == 'c':
           dictionaryWordList.append(row[0])

    # Create a wrong word list and a true word list
    # Here we use part of the 'wikipediatypoclean.txt' as input file
    # Note: Except for 'tab'(\t) and 'return'(\r), there's no other special characters in this file
    wrongWordList = []
    trueWordList = []
    for row in subCheckedAndTrueWords:
        eachSubCheckedAndTrueWord = re.split('\t',row[0])
        wrongWordList.append(eachSubCheckedAndTrueWord[0])
        trueWordList.append(eachSubCheckedAndTrueWord[1])

    # Calculate the error rate of spell check
    # Initialization for the shortest running time
    start = time.time()
    errorRate = measure_error(wrongWordList, trueWordList, dictionaryWordList, 1, 1, 1)
    leastRunningTime = time.time() - start
    leastTimeCostCombination = [1, 1, 1]
    print 'Please wait, the error rate is calculating in different cost combinations...'
    for deletion_cost in [1, 2, 4]:
        for insertion_cost in [1, 2, 4]:
            for substitution_cost in [1, 2, 4]:
                # Start time
                start = time.time()
                errorRate = measure_error(wrongWordList, trueWordList, dictionaryWordList, deletion_cost, insertion_cost, substitution_cost)
                # Count the total spelling check time
                print 'In cost combination', deletion_cost, insertion_cost, substitution_cost, 'The total time is:', time.time() - start, 'The error rate is:', float(errorRate)
                if time.time() - start < leastRunningTime:
                    leastRunningTime = time.time() - start
                    leastTimeCostCombination = [deletion_cost, insertion_cost, substitution_cost]
    print 'The least running time is', leastRunningTime, 'where the best cost combination is:', leastTimeCostCombination
if __name__ == '__main__':
    main()
