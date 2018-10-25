from util import *

invertedIndex, idfs, weights, totalDocs, totalWords = getMeta()

#print(list(idfs.keys())[0])
#print(idfs['respiratory'])
#print(weights['74001']['respiratory'])
#print(getQueryWeight('respiratory respiratory respiratory respiratory fibrosis sick hoibyn', idfs))

#query = input('Insert a query')

#for x in list(idfs.keys())[:50]:
#    print(x, idfs[x])
#query = 'What is the lipid composition of CF respiratory secretions'

#print([x for x in getSim(query, weights, idfs)])

getQuerys(idfs, weights)