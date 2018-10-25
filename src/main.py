from util import *

invertedIndex, idfs, weights, totalDocs, totalWords = getMeta()

print(list(idfs.keys())[0])
print(idfs['respiratory'])
print(weights['74001']['respiratory'])
print(getQueryWeight('respiratory respiratory respiratory respiratory fibrosis sick hoibyn', idfs))