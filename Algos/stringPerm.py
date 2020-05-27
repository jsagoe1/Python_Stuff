def perm1(s):
    lst = list(s)
    def findPerms(lst):  
        if len(lst) == 0:
            return []
        elif len(lst) == 1:
            return [lst]
        else:
            l = []
            for i in range(len(lst)):
                left = lst[i]
                right = lst[:i] + lst[i+1:]
                
                for p in findPerms(right):
                    l.append([left] + p)            
            return l        
    perms = findPerms(lst)
    return ["".join(word) for word in perms]
     
## perm2 uses yield instead of a list so uses almost no 
## memory at all
def perm2(s):
    lst = list(s)
    def findPerms(lst):  
        if len(lst) == 0:
            yield []
        elif len(lst) == 1:
            yield lst
        else:
            for i in range(len(lst)):
                left = lst[i]
                right = lst[:i] + lst[i+1:]
                
                for p in findPerms(right):
                    yield [left]+p            
    perms = ["".join(word) for word in findPerms(lst)]  
    return perms        

        
s = "abcd"
print(perm1(s))
print(perm2(s))
