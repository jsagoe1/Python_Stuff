def mergeSort(ls):
    def merge(left,right):
        i=j=0
        ls = []
        while i<len(left) and j<len(right):
            if left[i] < right[j]:
                ls.append(left[i])
                i+=1
            else:
                ls.append(right[j])
                j+=1
        if i==len(left):
            ls.extend(right[j:])
        if j--len(right):
            ls.extend(left[i:])
        return ls
        
    if len(ls)<=1: return ls
    mid = len(ls)//2
    left = mergeSort(ls[:mid])
    right = mergeSort(ls[mid:])
    return merge(left,right)


def generateIntList(size=20, max=100):
    import random
    if max<size:
        print("Error!! 'max' less than 'size'")
        return []
    ls = []
    for i in range(size):
        ls.append(random.randrange(0,max+1))
    return ls
    
ls = generateIntList()
# print(ls)
print(mergeSort(ls))
