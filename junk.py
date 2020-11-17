from itertools import permutations

r = list(range(9))

def block(b):
    blocks = {(x//3, y//3) for (x,y) in b}
    return len(blocks) < 9

def kingsMove(t):
    for x,y in t:
        for h in (-1,0,1):
            for v in (-1,0,1):
                if h==v==0:
                    continue
                if (x+h,y+v) in t:
                    return True
    return False
    
def knightsMove(t):
    for x,y in t:
        for h in (-1,1,-2,2):
            for v in (3-abs(h), abs(h)-3):
                if (x+h,y+v) in t:
                    return True
    return False

def orthogonal(s,t):
    for x,y in s:
        for h,v in ((1,0),(-1,0),(0,-1),(0,1)):
            if (x+h, y+v) in t:
                return True
    return False

def orderedSolutions(soln):
    for p in permutations(soln):
        if not any(orthogonal(soln[p[k]], soln[p[k+1]]) for k in range(8)):
            yield {k:soln[p[k]] for k in range(9)}
    
def printSolution(soln):
    array = { }
    for s in range(9):
        for x,y in soln[s]:
            array[x,y] = s+1
    for x in range(9):
        for y in range(9):
            print(array[x,y], end=' ')
        print()
    print()
    
transversals = []
for p in permutations(r):
    t = list(zip(p,r))
    if block(t):
        continue
    if kingsMove(t):
        continue
    if knightsMove(t):
        continue
    transversals.append(frozenset(t))

# find tansversal tilings by backtrack
possible = { }
solutions = [ ]
possible[0] = transversals.copy()
used = { }
soln = { }
level = 0
for t in transversals:
    used[0] = t
    soln[0] = t
    level = 1
    possible[1] = {t for t in possible[0] if not(t & used[0])} 
    while level > 0:
        while possible[level]:
            t = soln[level] = possible[level].pop()
            used[level] = used[level-1] | t
            if level == 8:
                solutions.append(soln.copy())
                #printSolution(soln)
                continue
            else:
                level += 1
                possible[level]= {t for t in possible[level-1] if not (t & soln[level-1])} 
        level -= 1

# Now apply the orthogonally adjacent rule to each tiling
solved = [ ]
for soln in solutions:
    for s in orderedSolutions(soln):
        printSolution(s)
        solved.append(s)