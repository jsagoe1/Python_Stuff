# Python MaxHeap

# public functions: push, peek, pop

# private functions: __swap, __floatUp, __bubbleDown

class MaxHeap:
    def __init__(self, items=[]):
        self.heap = [0]
        for i in items:
            self.heap.append(i)
            self.__floatUp(len(self.heap) - 1)
    
    def push(self, data):
        self.heap.append(data)
        self.__floatUp(len(self.heap) - 1)
        
    def peek(self):
        if self.heap[1]:
            return self.heap[1]
        else:
            return False

    def pop(self):
        if len(self.heap) > 2:
            self.__swap(1, len(self.heap) - 1)
            max = self.heap.pop()
            self.__bubbleDown(1)
        elif len(self.heap) == 2:
            max = self.heap.pop()
        else:
            max = False
        return max
            
    def __swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
    def __floatUp(self, index):
        parent = index//2
        if index <= 1:
            return
        elif self.heap[index] > self.heap[parent]:
            self.__swap(index, parent)
            self.__floatUp(parent)

    def __bubbleDown(self, index):
        left = index * 2
        right = index * 2 + 1
        largest = index
        if len(self.heap) > left and self.heap[largest] < self.heap[left]:
            largest = left
        if len(self.heap) > right and self.heap[largest] < self.heap[right]:
            largest = right
        if largest != index:
            self.__swap(index, largest)
            self.__bubbleDown(largest)
        
    def heapSort(self):
        ls = []
        while (len(self.heap) != 1):
            ls.append(self.pop())
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
m = MaxHeap(ls)
m.push(10)

print(str(m.heap[1:len(m.heap)]))
print(str(m.heapSort()))
