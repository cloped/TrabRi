import re
import string 

def getContent(document):
    content = ''

    rn = re.search('RN\s(\d)+', document).group().split()[1]

    au = re.search('AU\s((.)*\n)*TI', document)
    if au:
        au = au.group()[3:-3]
        au = re.sub('\n', '', au)
        au = re.sub('( )+', ' ', au)
        content+= au + ' '

    ti = re.search('TI\s((.)*\n)*SO', document).group()[3:-3]
    ti = re.sub('\n', '', ti)
    ti = re.sub('( )+', ' ', ti)
    content+= ti + ' '

    ab = re.search('(AB)\s((.)*\n)*RF', document)
    if ab:
        ab = ab.group()[3:-3]
        ab = re.sub('\n', '', ab)
        ab = re.sub('( )+', ' ', ab)
        content+= ab + ' '
    
    ex = re.search('(EX)\s((.)*\n)*(\n|RF)', document)
    if ex:
        ex = ex.group()[3:-3]
        ex = re.sub('\n', '', ex)
        ex = re.sub('( )+', ' ', ex)
        content+= ex + ' '

    mj = re.search('MJ\s((.)*\n)*MN', document)
    if mj:
        mj = mj.group()[3:-3]
        mj = re.sub('\n', '', mj)
        mj = re.sub('( )+', ' ', mj)
        content+= mj + ' '

    mn = re.search('MN\s((.)*\n)*(AB|EX)', document)
    if mn:
        mn = mn.group()[3:-3]
        mn = re.sub('\n', '', mn)
        mn = re.sub('( )+', ' ', mn)
        content+= mn + ' '
    
    content = content.lower()
    content = re.sub('['+string.punctuation+']', '', content)
    return rn, content

def adjustRelevance(relevances):
    for index, relevance in enumerate(relevances):
        value = 0
        while relevance > 0:
            value += relevance % 10
            relevance /= 10
        relevances[index] = int(value)
    return relevances

def getQuery(query):
    content = query

    query = re.search('QU\s((.)*\n)*NR', content).group()[3:-3]
    query = re.sub('\n', '', query)
    query = re.sub('( )+', ' ', query)
    query = query.lower()
    query = re.sub('['+string.punctuation+']', '', query)

    relevants = re.search('RD\s((.)*\n)*', content).group()[3:-3]
    relevants = re.sub('\n', '', relevants)
    relevants = re.sub('( )+', ' ', relevants)
    relevants = relevants.split()
    relevants = [ int(x) for x in relevants ]
    relevants = list(zip(relevants[::2],adjustRelevance(relevants[1::2])))

    #for index in range(0,range(len(relevants)),2):
    #    print(index)

    return query, sorted(relevants, key = lambda x: x[1], reverse = True)
    #return query, relevants