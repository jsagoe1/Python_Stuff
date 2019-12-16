class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        
        
class LinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = self.head
        self.length = 0
	
    def append(self, value):
        # Adds new node containing 'data' to the end of the linked list.
        new_node = Node(value)
		self.tail.next = new_node
        self.tail = new_node
        self.length += 1
	
    def insert(self, index, value):
		# Inserts a new node at index 'index' containing data 'data'.
		# Indices begin at 0. If the provided index is greater than or 
		# equal to the length of the linked list the 'data' will be appended.
        if index < 0:
            print("ERROR: index less than 0")
            return
        if index >= self.length:
            self.append(value)
        idx = 0
        prev_node = self.head
        cur_node = self.head.next
		
	    for _ in range(index-1):
		    prev_node = prev_node.next
            cur_node = cur_node.next
			
	    new_node = Node(value)
	    prev_node.next = new_node
	    new_node.next = cur_node
        self.length += 1
		
    def erase(self, index):
        # Deletes the node at index 'index'.
        if index >= self.length or index < 0: # added 'index<0' post-video
            print("ERROR: 'Erase' Index out of range!")
            return
        cur_node = self.head.next
        prev_node = self.head
        
		for _ in range(index-1):
			prev_node = prev_node.next
            cur_node = cur_node.next

		prev_node.next = cur_node.next
		self.length -= 1
		return

    def display(self):
        # Returns the linked list in traditional Python list format. 
        ans = []
        cur_node = self.head
        while cur_node != None:
            if cur_node.value:
                ans.append(cur_node.value)
            cur_node = cur_node.next
        return ans
                  
    def length(self):
        # Returns the length (integer) of the linked list.
        l_len = 0
        cur_node = self.head
        while cur_node.next != None:
            l_len += 1
            cur_node = cur_node.next
	    assert l_len == self.length
        return l_len
    
    def get(self, index):
        # Returns the value of the node at 'index'. 
        if index < 0 or index >= self.length:
            print("ERROR: index out of range")
            return
        idx = 0
        cur_node = self.head.next
        while cur_node != None:
            if idx == index:
                return cur_node.value
            cur_node = cur_node.next
            idx += 1                         
        
    def set(self, index, value):
        # Sets the data at index 'index' equal to 'data'.
	    # Indices begin at 0. If the 'index' is greater than or equal 
	    # to the length of the linked list a warning will be printed 
	    # to the user.
        if index >= self.length or index <0:
            print("EEROR: 'Set' Index out of range!")
            return
        idx = 0
        cur_node = self.head.next
        while cur_node is not None:
            if idx == index:
                cur_node.value = value
                return
            cur_node = cur_node.next
            idx += 1        
        
    	
ls = LinkedList()

vals = [2, 5, 9, 7, 8, 1]

for i in vals:
    ls.append(i)

print(ls.display())
ls.insert(2, 80)
print(ls.display())
ls.set(2, 6)
print(ls.display())
ls.erase(3)
print(ls.display())

'''#########################################################################
[2, 5, 9, 7, 8, 1]
[2, 5, 80, 9, 7, 8, 1]
[2, 5, 6, 9, 7, 8, 1]
[2, 5, 6, 7, 8, 1]
#########################################################################'''
    
