"""
You are permitted to write code between Start and End.
Besides, you can write other extra functions or classes outside, 
but don't change the template.
"""


class node:
    def __init__(self, element, next, mark):
        self.element = element
        self.next = next
        self.mark = mark

def newlist(n):
    i = 1
    list = []
    while i <= n:
        list.append(i)
        i += 1
    return list

def HanoiTower(n,from_rod ='A',aux_rod ='B',to_rod ='C'):    
    result_list = []
    # Start writing your code.
        # create linked list
    def move(X, Y):  # pop the head of the linked list X and insert it in to Y
        num = X.element.pop(0)
        Y.element.insert(0, num)
        strs=X.mark, '-->', Y.mark
        result_list.append(strs)
    


    def sequentialMove(num, X):  # move the number to the following column
        if X.next.element == [] or num < X.next.element[0]:
            # get rid of the condition if the head element of X.next is smaller than num
            move(X, X.next)
        elif X.next.next.element == [] or num < X.next.next.element[0]:
            move(X, X.next.next)
        else:
            return None


    def numMove(num, A, B, C):  # grasp the number if it is the head of certain linked list
        if A.element != [] and A.element[0] == num:
            sequentialMove(num, A)
        elif B.element != [] and B.element[0] == num:
            sequentialMove(num, B)
        elif C.element != [] and C.element[0] == num:
            sequentialMove(num, C)
    
    if n % 2 == 0:
        C = node([], None, 'C')
        B = node([], C, 'B')
        A = node(newlist(n), B, 'A')
        C.next = A
    else:
        C = node([], None, 'C')
        A = node(newlist(n), C, 'A')
        B = node([], A, 'B')
        C.next = B
    while True:
        for i in newlist(n):  # move the number from 1 to n in order
            numMove(i, A, B, C)
            
        if A.element == B.element == []:
            break


    return result_list
    # End writing your code.


    


"""
You should store each line your output in result_list defined above.
For example, if the outputs of print() are: 
                A --> C
                A --> B
then please store them in result_list:

strs = "A --> C"
result_list.append(strs)
strs = "A --> B"
result_list.append(strs)

Thus, once you want to print something, please store them in result_list immediately, 
rather than utilizing print() to print it. 
Don't miss the space! For example, don't output:
                A-->C
                A-->B

We will utilize the code similar to the following to check your answer.
"""

if __name__ == '__main__':
    n = 4
    result_list = HanoiTower(n)
    for item in result_list:
        print(item)
