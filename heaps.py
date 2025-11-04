# Class File for Heaps
# 0 based heap
class Heap :
    def __init__(self, is_min=True):
        self.data = []
        self.is_min = is_min # if this is true, its a min heap. else it is false
    
    def __len__(self):
        return len(self.data)
    
    def _compare(self, a, b):
        #compare a and b elements in the structure
        return a < b if self.is_min else a > b
    
    def is_empty(self):
        return len(self.data)== 0

    def insert(self, val):
        self.data.append(val)
        self._heapify_up(len(self.data)-1)
        return self.data.append(val)
        #need to bubble it up
    
    def peek (self):
        if self.is_empty():
            raise IndexError("Heap is empty")
        return self.data[0]
    
    def pop(self):
            # replace the root with the smallest (min) or largest element
            # return the top!
            if self.is_empty():
                raise IndexError("Heap is empty")
            ##self.data.remove(top)
            top = self.data[0]
            last = self.data.pop()
            if not self.is_empty():
                self.data[0] = last
                self._heapify_down(len(self.data)-1)
            return top 
            
    
    def _heapify_up(self,index):
        #compare child with current, if diff
        # find the parent first
        parent = (index-1)//2
        while index > 0 and self._compare(self.data[index], self.data[parent]):
            self.data[index], self.data[parent] = self.data[parent], self.data[index]
            index = parent 
            parent  = (index -1) //2 

    
    def _heapify_down(self,index):
        #compare parent with largst ele, swapping when needed
        size = len(self.data)
        while True:
            left = (2* index) +1
            right = (2*index) +2
            smallest = index
            # first we compare with left child
            if left < size and self._compare(self.data[left], self.data[smallest]):
                smallest = left
            if right < size and self._compare(self.data[right], self.data[smallest]):
                smallest = right 
            if smallest == index:
                break

            self.data[index], self.data[smallest] = self.data[smallest], self.data[index]

    def heapify(self, array):
        '''Start from the last non-leaf node (at index n//2 - 1)

        Call heapify_down for each node moving backward to the root

        This is more efficient than inserting one-by-one (O(n) instead of O(n log n))'''
        start = len(array)//2 -1
        if self.is_min:
            for i in reversed(range(start//2)):
                self._heapify_down(i)
        else: 
            for i in reversed(range(start//2)):
                self._heapify_up(i)
     
   
           

