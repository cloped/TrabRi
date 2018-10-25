import re
import string 
import math
import operator
from parser import *
from metrics import *

def getMeta():
    #words = invertedIndex.keys()
    invertedIndex = {}
    idfs = {}
    totalDocs = 0
    totalWords = 0
    #docs = weights.keys()
    weights = {}

    cfs = ['cf74', 'cf75', 'cf76', 'cf77', 'cf78', 'cf79']

    print('Creating invertedIndexes')
    for cfc in cfs:
        with open('../data/cfc/' + cfc, 'r') as cf:
            print('Reading and processing file:', cfc)
            data = cf.read()
            data = data.split('\nPN')
            data = [data[0]] + ['PN' + x for x in data[1:]]

        for document in data:
            recordNumber, content = getContent(document)
            totalDocs += 1
            flagedDocWords = []
            weights[recordNumber] = {}

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
                    invertedIndex[word][recordNumber] = 1
                else:
                    if recordNumber not in invertedIndex[word].keys():
                        invertedIndex[word][recordNumber] = 1
                    else:
                        invertedIndex[word][recordNumber] += 1
                totalWords += 1

    print('Calculating idfs.')
    # Calculating IDF
    for word in idfs.keys():
        idfs[word] = math.log10(totalDocs/idfs[word])

    print('Calculating weights.')
    # Calculating Weights
    for word in invertedIndex.keys():
        for doc in invertedIndex[word].keys():
            weights[doc][word] = idfs[word] * invertedIndex[word][doc]

    print('You have a total of:', totalDocs, 'docs.')
    print('You have a total of:', totalWords, 'words.')
    
    return invertedIndex, idfs, weights, totalDocs, totalWords

def countWord(word, query):
    count = 0
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

def getSim(query, idfs, weights):
    query = query.lower()
    query = re.sub('['+string.punctuation+']', '', query)
    queryWeight = getQueryWeight(query, idfs)
    #print(queryWeight)
    ranking = []

    for doc in weights.keys():
        acumulator = 0.
        normDoc = 0.
        normQuery = 0.
        for word in query.split():
            if word in weights[doc].keys():
                acumulator += weights[doc][word] * queryWeight[word]
                normDoc += weights[doc][word] * weights[doc][word]
                normQuery += queryWeight[word] * queryWeight[word]
        

        normDoc = math.sqrt(normDoc)
        normQuery = math.sqrt(normQuery)
        
        if normDoc * normQuery > 0:
            print(acumulator / float(normDoc * normQuery))
            #print(sim)
            ranking.append((doc, acumulator / (normDoc * normQuery)))

    return sorted(ranking, key = lambda x: x[1], reverse = True)[:10]

def getQuerys(idfs, weights):
    with open('../data/cfc/cfquery', 'r') as cf:
        print('Reading and processing query file.')
        data = cf.read()
        data = data.split('\nQN')
        data = [data[0]] + ['QN' + x for x in data[1:]]
        acumulator = 0.
        for query in data:
            query, relevants = getQuery(query)
            ranking = getSim(query, idfs, weights)
            print(query)
            print(ranking)
            #print(relevants)
            #acumulator += map(ranking, relevants)
            break
        #print(acumulator/len(data))
