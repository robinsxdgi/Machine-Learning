# EECS 349 Machine Learning, Spell Checking System 2
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

def find_closest_word(string1, dictionary): # dictionary is a list of strings consists of correct words
    closestWord = dictionary[0]
    closestDistance = levenshtein_distance(string1, dictionary[0], 1, 1, 1)
    for i in range(len(dictionary)):
        if closestDistance > levenshtein_distance(string1, dictionary[i], 1, 1, 1): # We first consider the case that three costs equal to 1, if the new word has closer distance to the word, then we replace the closest word by this new one.
            closestWord = dictionary[i]
            closestDistance = levenshtein_distance(string1, dictionary[i], 1, 1, 1)
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

def main():
    wordChecked = open(sys.argv[1]) # Input the file to be spell-checked
    wordDictionary = open(sys.argv[2]) # Input the dictionary word list
    dictionaryWords = csv.reader(wordDictionary)

    # Create a list of words in dictionary
    dictionaryWordList = []
    for row in dictionaryWords:
        dictionaryWordList.append(row[0])
    # print(dictionaryWordList)

    # For spell-checked words, treat all special characters (e.g. blanks, commas, tabs, etc.) as word delimiters
    wrongWordList = []
    for row in wordChecked:
        wrongWords = re.split('\t|\s|\n|`|-|=|~|!|@|#|\$|%|\^|&|\*|\(|\)|_|\+|\[|]|;|,|\.|/|\\\\|\'|\{|}|\]|:|"|>|\?|\||<',row)
        for words in wrongWords:
            if words != '':
                wrongWordList.append(words) # Get every contiguous sequence of alphanumeric characters in the input file as a word.

    # Create a correct words list for those spell-checked words
    writingWord = open('corrected.txt', 'w')
    for word in wrongWordList:
        # find correct spells for each checked word
        correctSpell = find_closest_word(word, dictionaryWordList)
        writingWord.write(correctSpell + '\n')
    writingWord.close()

if __name__ == '__main__':
    main()
