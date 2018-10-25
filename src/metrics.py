def map(ranking, relevants):
    acumulator = 0.
    found = 0.
    relevants = [ x[0] for x in relevants]
    #ranking = ranking[:len(relevants)]
    for index, docFound in enumerate(ranking):
        if docFound in relevants:
            found += 1
            acumulator += found/(index + 1)
        
        if index == 2:
            break
    return acumulator/len(ranking)