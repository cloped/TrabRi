import re
import string 
import math
from parser import *

def getMeta():
    #words = invertedIndex.keys()
    invertedIndex = {}
    idfs = {}
    totalDocs = 0
    totalWords = 0
    #docs = weights.keys()
    weights = {}

    cfs = ['cf74']

    for cfc in cfs:
        with open('../data/cfc/' + cfc, 'r') as cf:
            print('Reading and processing file:', cfc)
            data = cf.read()
            data = data.split('\nPN')
            data = [data[0]] + ['PN' + x for x in data[1:]]

        for document in data:
            paperNumber, content = getContent(document)
            totalDocs += 1
            flagedDocWords = []
            weights[paperNumber] = {}

            for word in content.split():
                # Setting to use to IDF
                if word not in flagedDocWords:
                    if word not in idfs.keys():
                        idfs[word] = 1
                    else:
                        idfs[word] += 1
                    flagedDocWords.append(word)

                # Inverted index build
                if word not in invertedIndex.keys():
                    invertedIndex[word] = {}
                    invertedIndex[word][paperNumber] = 1
                else:
                    if paperNumber not in invertedIndex[word].keys():
                        invertedIndex[word][paperNumber] = 1
                    else:
                        invertedIndex[word][paperNumber] += 1
                totalWords += 1

    # Calculating IDF
    for word in idfs.keys():
        idfs[word] = math.log10(totalDocs/idfs[word])

    # Calculating Weights
    for word in invertedIndex.keys():
        for doc in invertedIndex[word].keys():
            if idfs[word] * invertedIndex[word][doc] > 0:
                weights[doc][word] = idfs[word] * invertedIndex[word][doc]

    print('You have a total of:', totalDocs, 'docs.')
    print('You have a total of:', totalWords, 'words.')
    return invertedIndex, idfs, weights, totalDocs, totalWords

def countWord(word, query):
    count = 0
    query = query.lower()
    query = re.sub('['+string.punctuation+']', '', query)
    for element in query.split():
        if element == word:
            count += 1
    return count

def getQueryWeight(query, idfs):
    queryWeight = {}
    for word in query.split():
        if word in idfs.keys():
            if countWord(word,query) > 0:
                queryWeight[word] = idfs[word] * countWord(word,query)
    return queryWeight

