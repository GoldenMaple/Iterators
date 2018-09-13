'''
参考文档
check https://rszalski.github.io/magicmethods/ for more information
https://www.programiz.com/python-programming/iterator
'''

'''
implementing custom container types in Python involves using some of protocols. 

(1) protocol for defining immutable containers
define __len__()
define __getitem__()

(2) protocol for defining mutable containers
define __len__()
define __getitem__()
define __setitem__()
define __delitem__()

(3) protocal for iterable 
define __iter__()

An object is called iterable if the object implementes __iter__()
the function __iter__() returns an iterator
the function obj.__iter__() is automatically called when using iter(obj)

(4) protocal for iterator
a object is called iterator if we:
define __iter__()
define __next__()

obj.__next__() will be called when using next(obj)

(5) how for loop in python is implemented
for element in iterable:
    # do something with element
    
Is actually implemented as

iter_obj = iter(iterable) # create an iterator object from that iterable
while True: # infinite loop
    try:
        element = next(iter_obj) # get the next item
        # do something with element
    except StopIteration:
        break # if StopIteration is raised, break from loop

So internally, the for loop creates an iterator object, iter_obj by calling 
iter() on the iterable.
'''
def Example_PowTwo():
    class PowTwo:
        def __init__(self, max = 0):
            self.max = max
    
        def __iter__(self):
            self.n = 0
            return self
    
        def __next__(self):
            if self.n > self.max:
                raise StopIteration
    
            result = 2 ** self.n
            self.n += 1
            return result
            
    def PowTwoGen(max = 0):
        n = 0
        while n <= max:
            yield 2 ** n
            n += 1
            
    iterator = PowTwo(10)
    for i in iterator:
        print(i)
        
    gen = PowTwoGen(10)
    for i in gen:
        print(i)

def Example_DataPipeLine():
    with open('data.txt') as file:
        lines = (line.strip() for line in file)
        ages = (int(line.split(' ')[1]) for line in lines)
        for age in ages:
            print('age is {}'.format(age))
        

if __name__=='__main__':
    Example_PowTwo()
    Example_DataPipeLine()