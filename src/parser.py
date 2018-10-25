import re
import string 

def getContent(document):
    content = ''

    pn = re.search('PN\s(\d)+', document).group().split()[1]

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
    return pn, content