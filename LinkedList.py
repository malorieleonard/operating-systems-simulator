'''
Implements a doubly-linked list

Author: Clayton S. Ferner
Date: 5/24/2016

Classes:
    listNode
    LinkedList
    LinkedListIterator
'''
import random


class listNode:
    '''
    This is a list node that is used by the LinkedList class.  There is no
    reason to directly access this class.
    '''
    def __init__(self, data = None, next = None, prev = None):
        '''
        Constructor of a list node
        Parameters:
            data (or payload): any type (default None)
            next: listNode (default None)
            prev: listNode (default None)

        Returns:
            None
        '''
    def getData(self):
        '''
        Gets the data in the list node
        Parameters:
            None

        Returns:
            payload: any type
        '''
    def setData(self, payload):
        '''
        Sets the payload in a list node

        Parameters:
            payload: any type

        Returns:
            None
        '''
    def getNext(self):
        '''
        Gets the next list node

        Parameters:
            None

        Returns:
             next: listnode
        '''
    def setNext(self, next):
        '''
        Sets the next list node
        Parameters:
            next: listNode
        Returns:
             None
        '''
    def getPrev(self):
        '''
        Gets the prev list node

        Parameters:
            None

        Returns:
             prev: listNode
        '''
    def setPrev(self, prev):
        '''
        Sets the prev list node

        Parameters:
            prev: listNode

        Returns:
             None
        '''

class LinkedList:
    '''
    Implements a Doubly Linked List

    Functions:
        __init__(self)
        insert(self, int, any type)
        insertionSort(self, any type)
        prepend(self, any type)
        append(self, any type)
        front(self) -> any type
        back(self) -> any type
        pop(self, int) -> any type
        __len__(self, self) -> int
        isEmpty(self, self) -> boolean
        __str__(self, self) -> string
        find(self, x) -> any type
        index(self, any type) -> int
        remove(self, any type)
        newIterator(self) -> LinkedListIterator
    '''
    def __init__(self):
        '''
        Constructor - initializes the list to be empty

        Parameters:
            None

        Returns:
            None
        '''
    def insert(self, i, x):
        '''
        Inserts the value x into the list at position i.

        Parameters:
            i: int
            x: any value

        Returns:
            None
        '''
    def insertionSort(self, x):
        '''
        Inserts x into the list based upon its value. This assumes the
        list is maintained in sorted order. In other words, that everything
        is inserted using this method and NOT a mixture of insert() and insertionSort().
        insertionSort(). You should ither use insert() or insertionSort() but not both. Each value
        both. Each value is assumed to have a getKey() function that returns a comparable
        value.  This function will use the "<=" operator on the keys to
        put the values in sorted (ascending) order. You can put the values
        in descending order by reversing the key values.
        Parameters:
            x: any value (with a getKey() function)

        Returns:
            None
        '''
    def prepend(self, x):
        '''
        Inserts the value x at the front of the list

        Parameters:
            x: any type

        Returns:
            None
        '''
    def append(self, x):
        '''
        Inserts the value x at the back of the list

        Parameters:
            x: any type

        Returns:
            None
        '''
    def front(self):
        '''
        Gets the value at the front of the list

        Parameters:
            None

        Returns:
            value at the front: any value
        '''
    def back(self):
        '''
        Gets the value at the back of the list

        Parameters:
            None

        Returns:
            value at the back: any value
        '''
    def pop(self, i = None):
        '''
        Removes and returns the value from the list at position i

        Parameters:
            i: int (default None)
                The first value in the list is at position 0. The second value
                in the list is at position 1. The last value in the list is at
                position len(theList)-1.  You can leave the position out, and it
                will automatically pop the last value.
        Returns:
            the value: any type
        Exception:
            Raises an "IndexError" if i is not in the range 0 <= i < len(theList)
        '''
    def __len__(self):
        '''
        returns the size of the list.  This overloads the len() operator
        so you can do len(myList)

        Parameters:
            None

        Returns:
            length: int
        '''
    def isEmpty(self):
        '''
        Checks to see if the list is empty

        Parameters:
            None

        Returns:
            boolean
        '''
    def __str__(self):
        '''
        Returns a string of the values in the list. This overloads the str()
        operator so that you can do things like print(myList). It is
        assumed that each value in the list also can be converted to a string
        by using str(value).

        Parameters:
            None

        Returns:
            string
        '''
    def find(self, x):
        '''
        Finds the first occurrence of x in the list.  It is assumed that
        the equals operator (==) can be applied to the values in the list.
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
    def __removeListNode(self, ln):
        '''
        Removes the list node ln

        Parameters:
            ln: listNode

        Returns:
            None
        '''
    def newIterator(self):
        '''
        Creates a new iterator for this list.
        Parameters:
            None
        Returns:
            LinkedListIterator
        '''

class LinkedListIterator:
    '''
    Implements an Iterator for a Linked List

    Functions:
        __init__(self, linkedlist)
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
    def __init__(self, linkedlist):
        '''
        Constructor - initializes the iterator to be past end

        Parameters:
            ll: LinkedList (default None)

        Returns:
            None

        Raises:
            ValueError if linkedlist is None
        '''
    def setCurrentFront(self):
        '''
        Sets the current to point to the value at the front of the list.
        The current is a mechanism for doing iteration.  You can have
        it point to any value in the list; advance it (move it forward);
        and retreat it (move it backwards).

        Parameters:
            None

        Returns:
            None
        '''
    def setCurrentBack(self):
        '''
        Sets the current to point to the value at the back of the list.

        Parameters:
            None

        Returns:
            None
        '''
    def advance(self):
        '''
        Moves the current forward to the next value in the list.

        Parameters:
            None

        Returns:
            None
        '''
    def retreat(self):
        '''
        Moves the current backwards to the prev value in the list.

        Parameters:
            None

        Returns:
            None
        '''
    def getCurrentValue(self):
        '''
        Returns the value that current points to

        Parameters:
            None

        Returns:
            payload: any type
            or None if current is past end
        '''
    def isPastEnd(self):
        '''
        Returns true if the current has gone off either end of the list.

        This is an example of how one my iterator over a list:
            myIter = myList.newIterator() or myIter = LinkedListIterator(myList)
            myIter.setCurrentFront()
            while not myIter.isPastEnd():
                # Do something with myIter.getCurrentValue()
                # ...
                myIter.advance()

        Or iterating backwards through the list:
            myIter = myList.newIterator() or myIter = LinkedListIterator(myList)
            myIter.setCurrentBacl()
            while not myIter.isPastEnd():
                # Do something with myIter.getCurrentValue()
                # ...
                myIter.retreat()

        Parameters:
            None

        Returns:
            boolean
        '''
    def peekAfterCurrent(self):
        '''
        Returns the value that follows the value that the current points to (but does not
        remove anything). This is useful to decide if you want to move forward or backwards
        in the list by seeing what's next.

        Parameters:
            None

        Returns:
            any value (or None if there is no value after the current or current
            is past end)
        '''
    def peekBeforeCurrent(self):
        '''
        Returns the value that comes before the value that the current points to (but does not
        remove anything). This is useful to decide if you want to move forward or backwards
        in the list by seeing what's next.

        Parameters:
            None

        Returns:
            any value (or None if there is no value before the current or current
            is past end)
        '''
    def removeCurrentAndAdvance(self):
        '''
        Removes and returns the value pointed to by current, then advances the current.
        This is sort of like pop(), except that it uses the current instead of an index.
        The current must either advance or retreat (see removeCurrentAndRetreat())
        because the value it was pointing to is no longer there. In other words, if you
        just remove the value pointed to by current, then current wouldn't have anything
        to point to. So if you are iterating over a list, and want to remove the current
        value and continue iterating, the only way to do that (without having to reset
        the interator to the front and starting over) is to use the
        removeCurrentAndAvance() or removeCurrentAndRetreat().

        Parameters:
            None

        Returns:
            the value at current: any type
        '''
    def removeCurrentAndRetreat(self):
        '''
        Removes and returns the value pointed to by current, then retreats the current.
        This is sort of like pop(), except that it uses the current instead of an index.
        The current must either advance (see removeCurrentAndAdvance()) or retreat
        because the value it was pointing to is no longer there. In other words, if you
        just remove the value pointed to by current, then current wouldn't have anything
        to point to. So if you are iterating over a list, and want to remove the current
        value and continue iterating, the only way to do that (without having to reset
        the interator to the back and starting over) is to use the
        removeCurrentAndRetreat() or removeCurrentAndAvance().

        Parameters:
            None

        Returns:
            the value at current: any type
        '''

