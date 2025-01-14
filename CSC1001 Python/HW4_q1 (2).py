"""
You are permitted to write code between Start and End.
Besides, you can write other extra functions or classes outside, 
but don't change the template.
"""


class Node:
    def __init__(self, element, pointer):
        self.element = element
        self.pointer = pointer


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert(self, data): #insert at the tail
        # Start writing your code.
        node = Node(data, None)
        if self.size > 0:
            self.tail.pointer = node
        else:
            self.head = node
        self.tail = node
        self.size += 1
    
    def dequeue(self):    #Use linkedqueue
        if self.size == 0:
            return None
        else:
            answer = self.head.element
            self.head = self.head.pointer
            self.size -= 1
            if self.size == 0:
                self.tail = None
            return answer
    
    def enqueue(self,e):
        node=Node(e,None)
        if self.size == 0:
            self.head=node
        else:
            self.tail.pointer=node
        self.tail=node
        self.size+=1
    


# End writing your code.

def quick_sort(node): #Get the first reference of the first node
    # Start writing your code.
    q=QuickSort(node) #get the sorted linked list in ascending order. 
    return q.head     
    # End writing your code.

def QuickSort(node): #Get sorted linked list
    if node==None:
        return SinglyLinkedList()
    elif node.pointer==None:
        t=SinglyLinkedList()
        t.enqueue(node.element)
        return t
    key=node.pointer
    keyterm=node.element
    l1=SinglyLinkedList()
    l2=SinglyLinkedList()
    while key!=None:
        if key.element<keyterm:
            l1.enqueue(key.element)
        else:
            l2.enqueue(key.element)
            node=node.pointer
        key=key.pointer
    l1=QuickSort(l1.head) 
    l2=QuickSort(l2.head) 
    l1.enqueue(keyterm)
    while(l2.size>0):
        t=l2.dequeue()
        l1.enqueue(t)
    return l1    
    
# We will utilize the code similar to the following to check your answer.
if __name__ == '__main__':
    test_list = SinglyLinkedList()
    nums = [4,2,3,1,0,5]  # An example.
    for num in nums:
        test_list.insert(num)

    first_node = test_list.head  # Get the first node of the linked list.
    p = quick_sort(first_node)
    while p.pointer != None:
        print(p.element)
        p = p.pointer
    print(p.element)
    
