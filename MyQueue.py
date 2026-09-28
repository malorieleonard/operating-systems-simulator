'''
Implements a FIFO Queue, a Priority Queue, and a Sorted Queue

Author: Clayton S. Ferner
Date: 4/15/2022

Classes:
    FIFOQueue
    PriorityQueue
    SortedQueue
    QueueIterator
'''

from LinkedList import LinkedList,LinkedListIterator

class FIFOQueue:
    '''
    Implements a FIFO Queue

    Functions:
        __init__(self)
        enqueue(self, any type)
        dequeue(self) -> any type
        peek(self) -> any type
        find(any type) -> any type
        index(self, any type) -> int
        remove(self, any type)
        __len__(self) -> int
        isEmpty(self) -> boolean
        __str__(self) -> string
        newIterator -> QueueIterator

    '''
    def __init__(self):
        '''
        Constructor - initializes the queue to be empty

        Parameters:
            None

        Returns:
            None
        '''
    def enqueue(self, x):
        '''
        Enqueues the value x at the end of the line.

        Parameters:
            x: any value

        Returns:
            None
        '''
    def dequeue(self):
        '''
        Removes and returns the value at the front

        Parameters:
            None

        Returns:
            the value: any type
        '''
    def peek(self):
        '''
        Returns (BUT DOES NOT REMOVE) the value at the front

        Parameters:
            None

        Returns:
            the value: any type
        '''
    def find(self, x):
        '''
        Finds the first occurrence of x in the queue.  It is assumed that
        the equals operator (==) can be applied to the values in the queue.

        Parameters:
            x: any value

        Returns:
            that payload that matches or None if the value is not found: any type
        '''
    def index(self, x):
        '''
        Finds the first occurrence of x in the list and returns its index.
        It is assumed that the equals operator (==) can be applied to the
        values in the list. The value at the front is at index 0.

        Parameters:
            x: any value

        Returns:
            the index of the first payload that matches or -1 if
            the value cannot be found: int
        '''
    def remove(self, x):
        '''
        Removes the first occurrence of the value from the list
        It is assumed that the equals operator (==) can be applied to the
        values in the list. If the value is not found, nothing is removed.
        Parameters:
            x: any type
        Returns:
            None
        '''
    def __len__(self):
        '''
        returns the size of the queue.  This overloads the len() operator,
        so you can do len(myQueue).

        Parameters:
            None

        Returns:
            length: int
        '''
    def isEmpty(self):
        '''
        Checks to see if the queue is empty

        Parameters:
            None

        Returns:
            boolean
        '''
    def __str__(self):
        '''
        Returns a string of the values in the queue. This overloads the str()
        operator so that you can do things like print(myQueue). It is
        assumed that each value in the list also can be converted to a string
        by using str(value).

        Parameters:
            None

        Returns:
            string
        '''
    def newIterator(self):
        '''
        Creates a new iterator for this queue.
        Parameters:
            None
        Returns:
            QueueIterator
        '''

class PriorityQueue(FIFOQueue):
    '''
    Implements a Priority Queue.  It does so by maintaining a sorted list.
    This is not the most efficient way to do a priority list, because
    each Insertion Sort is O(N), but it is convenient.

    This Priority Queue extends the FIFOQueue, so it inherits ALL of the
    operations of a FIFO Queue.  The only difference is the enqueue uses
    insertionSort() instead of append().  That ensures that the smallest
    value (the highest priority) is at the front and the first one to be
    dequeued. The insertionSort() assumes that values inserted into the
    queue have a function called getKey() that returns a comparable
    value.  This function will use the "<=" operator on the keys to
    put the values in sorted (ascending) order. You can put the values
    in descending order by reversing the key values.

    Functions:
        enqueue(any type)
    '''

    def enqueue(self, x):
        '''
        Enqueues the value x. Since this uses insertionSort(), it requires that
        the value enqueue must have a getKey() function to return an comparable
        value which the less than or equal to operator (<=) can be applied.
        Parameters:
            x: any value
        Returns:
            None
        '''

class SortedQueue(PriorityQueue):
    '''
    Implements a Sorted Queue.
    This Sorted Queue extends the PriorityQueue(and FIFOQueue), so it
    inherits ALL of the operations of a FIFO Queue.  This is basically
    a priority queue. The same thing applies with respect to the user
    of insertionSort().  The values will be inserted in ascending order.
    The insertionSort() assumes that values inserted into the
    queue have a function called getKey() that returns a comparable
    value.  This function will use the "<=" operator on the keys to
    put the values in sorted (ascending) order. You can put the values
    in descending order by reversing the key values.

    Functions:
        enqueue(any type)
    '''


class QueueIterator(LinkedListIterator):
    '''
    Implements an Iterator for a Linked List

    Functions:
        __init__(self, linkedlist)

    Functions inherited from the LinkedListIterator class:
        setCurrentFront(self)
        setCurrentBack(self)
        advance(self)
        retreat(self)
        getCurrentValue(self) -> any type
        isPastEnd(self) -> boolean
        peekAfterCurrent(self) -> any type
        peekBeforeCurrent(self) -> any type
        removeCurrentAndAdvance(self)
        removeCurrentAndRetreat(self)
    '''

    def __init__(self, queue):
        '''
        Constructor - initializes the iterator to be past end

        Parameters:
            queue: FIFOQueue (although this may also be a PriorityQueue or SortedQueue

        Returns:
            None
        Raises:
            ValueError if queue is None
        '''

