def shellsort(ls):
    gaps = []
    h = 1
    while h<len(ls):
        gaps.insert(0,h)
        h = (3*h) + 1
        
    for gap in gaps:
        for i in range(gap,len(ls),gap):
            key = ls[i]
            for j in range(i-gap,-1,-gap):
                if key < ls[j]:
                    ls[j],ls[j+gap] = ls[j+gap],ls[j]
    return ls
               
def generateIntList(size = 20, max = 100):
    if size>max:
        print("ArgumentError in function 'generateIntList':'size' larger than 'max'")
        return []
    import random
    ls = []
    while len(ls) != size:
        num = (random.randrange(0,max+1))
        if num not in ls:
            ls.append(num)
    return ls


ls = generateIntList()
print("list:",ls)
print("sorted list:",shellsort(ls))
