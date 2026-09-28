"""
This module implements an IO Request.  An IO Request is just a structure used
to hold information about a request for I/O.  The IO_Request class doesn't
have any real functionality to it.

Author: Clayton S. Ferner
Date: 7/19/2022

Classes:
    IO_Request
"""

from Globals import Globals

class IO_Request:
    """
        An IO Request is just that: a request for I/O to be done. This class doesn't
        have any real functionality. It is basically a structure to hold information
        about the I/O being requested.

        Attributes:
            Class (Static) Data:
                IORead: int
                IOWrite: int
                These attributes are used just to specify the type of I/O (IOType), whether
                it is a request to read from a device or wrote to a device.

        Functions:
            Class (Static) Functions:
                none

            Instance Functions:
                __init__(self, task, device, blockNum, page, frame, fd, type, thread, priority, cylinder) (Constructor)
                __str__(self) -> string
                getId(self) -> int
                getType(self)
                prettyType(self) -> string
                getKey(self) -> int
                getTask(self) -> Task
                getThread(self) -> Thread
                getDevice(self) -> Device
                getPriority(self)
                getBlockNum(self) -> int
                getPage(self) -> Page
                getFrame(self) -> Frame
                getfd(self) -> OpenFileDescriptor
                getCylinder(self) -> int
                getNumPendingIOs(self) -> int
                getOriginationTime(self) -> int
                getStartTime(self) -> int
                incrementIOCount(self)
                decrementIOCount(self)
                setCylinder(self, int)
                __eq__(self, other) -> boolean
                __ne__(self, other) -> boolean

    """

    def __init__(self, task, device, blockNum, page, frame, fd, type, thread = None, priority = 0, cylinder = None):
        """
        This is the constructor.

        Parameters:
            task: Task
            device: Device
            blockNum: int
            page: Page
            frame: Frame
            fd: OpenFileDescriptor
            type: IOType
            thread: Thread (default None)
            priority: int (default zero)
            cylinder: int (default None)

        Returns:
            None
        """
    def __str__(self):
        """
        Returns string representation of an IO_Request

        Parameters:
            None
        Returns:
            A string representation of an IO_Request: string
        """
    def getId(self):
        """
        Gets the IO_Request Id

        Parameters:
            None

        Returns:
            int
        """
    def getType(self):
        """
        Gets the IO Type

        Parameters:
            None

        Returns:
            IOType
        """
    def prettyType(self):
        """
        Returns an English desciption of the IO Type.  For example, instead
        of 1001 (IORead), it returns "Read".  Instead of 1002 (IOWrite), it returns "Write".

        Parameters:
            None

        Returns:
            string
        """
    def getKey(self):
        """
        Gets the key for this IO Request.  This is used by the SortedQueue
        to keep the queue sorted.  When implementing algorithms like Shortest-
        Seek-Time-Next, Scan, or circular Scan for Disks, it is much easier
        if the IO Requests are kept in the queue sorted by cylinder/track number. The
        SortedQueue class expects there to be a getKey() function by which it
        can sort the data put into the queue.

        Parameters:
            None

        Returns:
            int
        """
    def getTask(self):
        """
        Gets the Task

        Parameters:
            None

        Returns:
            Task
        """
    def getThread(self):
        """
        Gets the Thread

        Parameters:
            None

        Returns:
            Thread
        """
    def getDevice(self):
        """
        Gets the Device

        Parameters:
            None

        Returns:
            Device
        """
    def getPriority(self):
        """
        Gets the number priority

        Parameters:
            None

        Returns:
            int
        """
    def getBlockNum(self):
        """
        Gets the block number

        Parameters:
            None

        Returns:
            int
        """
    def getPage(self):
        """
        Gets the Page

        Parameters:
            None

        Returns:
            Page
        """
    def getFrame(self):
        """
        Gets the Frame

        Parameters:
            None

        Returns:
            Frame
        """
    def getfd(self):
        """
        Gets the OpenFileDescriptor

        Parameters:
            None

        Returns:
            OpenFileDescriptor
        """
    def getCylinder(self):
        """
        Gets the Cylinder

        Parameters:
            None

        Returns:
            int
        """
    def getNumPendingIOs(self):
        """
        Gets the number of Pending IOs

        Parameters:
            None

        Returns:
            int
        """
    def getOriginationTime(self):
        """
        Gets the origination time (the time the IO request was created).

        Parameters:
            None

        Returns:
            int
        """
    def getStartTime(self):
        """
        Gets the start time (the time the device starts working on the reqeust).

        Parameters:
            None

        Returns:
            int
        """
    def incrementIOCount(self):
        """
        Increments by one number of Pending IOs

        Parameters:
            None

        Returns:
            None
        """
    def decrementIOCount(self):
        """
        Decrements by one number of Pending IOs

        Parameters:
            None

        Returns:
            None
        """
    def setCylinder(self, cylinder):
        """
        Sets the Cylinder number

        Parameters:
            cylinder: int

        Returns:
            None
        """
    def __eq__(self, other):
        """
        Overloads the equals (==) operator. Returns True of self and other
        have the same ID, False otherwise.

        Parameters:
            None

        Returns:
            boolean
        """
    def __ne__(self, other):
        """
        Overloads the not equals (!=) operator. Returns True of self and other
        have the different IDs, False otherwise.

        Parameters:
            None

        Returns:
            boolean
        """
