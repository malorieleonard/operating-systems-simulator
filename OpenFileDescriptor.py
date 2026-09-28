# Student: Malorie Leonard
# Date: 4/14/2026

"""
This module implements an open file for the Simulator.

Author: Clayton S. Ferner
Date: 3/27/2024

Classes:
    OpenFileDescriptor
"""
from Globals import Globals
from SimExceptions import SimException
from Devices import Device,Block
from IO_Request import IO_Request

class OpenFileDescriptor:
    """
    Implements an open file descriptor.  Files must first be opened
    in order to read or write their contents.

    Functions:
        Class (Static) Functions:
            None

        Instance Functions:
            __init__(self, file, task)
            __str__(self) -> string
            getTask(self) -> Task
            getFile(self) -> File
            getNumIOs(self) -> int
            incrementIOCount(self)
            decrementIOCount(self)
            closePending(self) -> boolean
            setClosePending(self)
            clearClosePending(self)
            close(self)
            read(self, logicalBlockNum, page, thread, suppressPageLock) -> boolean or None
            write(self, logicalBlockNum, page, thread, suppressPageLock) -> boolean or None
            delete(self, logicalBlockNum)
    """

    def __init__(self, file, task):
        """ This is the constructor.

         Parameters:
             file: File
             task: Task

         Returns:
             None
        """
        self.__file = file
        self.__task = task
        self.__closePending = False
        self.__numIOs = 0
        self.__file.incrementOpenCount()

    def read(self, logicalBlockNum, page, thread=None, suppressPageLock = False):
        """
        Reads a block of data from the file into a page. Blocks are the same size as
        pages (or frames).

        This function will lock the page (preventing it from being swapped out)
        during the IO.  If the locking of the page causes a page fault,
        then a False is returned.  These causes the simulator to try the
        read() request again after the thread has been woken from the page
        fault.

        The suppressPageLock is there so that the pageFaultHandler can
        prevent a 2nd page fault from occurring doing the PageFault process.
        It should ONLY be used by the pageFaultHandler.

        If the IO request is submitted, then this function will return
        True.  The thread is put into a waiting state until the device can
        complete the IO request.  After the IO request is complete, the
        device driver will wake up the thread so that it can continue.

        Parameters:
            logicalBlockNum: int
            page: Page
            thead: Thread (default None)
            suppressPageLock: boolean (default False)

        Returns:
            boolean or None:
                True if IO Request submitted
                False if a PageFault is generated to load the page
                None if the logical block number is invalid (out of range)
        """
        task = self.getTask()
        pageTable = task.getPageTable()

        if isinstance(page, int):
            page = pageTable.getPage(page)

        file = self.getFile()
        iNode = file.getINode()
        device = file.getDevice()

        if logicalBlockNum >= len(iNode):
            Globals.setWarning()
            Globals.logMessage("OpenFileDescriptor: read(): logical block number out of range")
            return None

        physicalBlockNum = iNode.getBlock(logicalBlockNum)

        if not suppressPageLock:
            if not pageTable.lockPage(page):
                return False

        frame = page.getFrame()

        if thread is not None:
            thread.sleep()

        io_request = IO_Request(
            task,
            device,
            physicalBlockNum,
            page,
            frame,
            self,
            IO_Request.IORead,
            thread
        )

        self.incrementIOCount()
        device.enqueue(io_request)
        return True

    def write(self, logicalBlockNum, page, thread=None, suppressPageLock = False):
        """
        Writes a block of data from a page to the file. Blocks are the same size as
        pages (or frames).

        If the logicalBlockNum is bigger than the number of blocks allocated to the
        file, then additional blocks will need to be allocated. This is
        different from the read() which will not allow for reading beyond
        the size of the file. If there are not enough blocks on the device
        that will allow the file to grow, then None is returned.

        This function will lock the page (preventing it from being swapped out)
        during the IO.  If the locking of the page causes a page fault,
        then a False is returned.  These causes the simulator to try the
        write() request again after the thread has been woken from the page
        fault.

        The suppressPageLock is there so that the pageFaultHandler can
        prevent a 2nd page fault from occurring doing the PageFault process.
        It should ONLY be used by the pageFaultHandler.

        If the IO request is submitted, then this function will return
        a True.  The thread is put into a waiting state until the device can
        complete the IO request.  After the IO request is complete, the
        device driver will wake up the thread so that it can continue.

        Parameters:
            offset: int (bytes)
            page: Page
            thead: Thread (default None)
            suppressPageLock: boolean (default False)

        Returns:
            boolean or None
                True if IO Request submitted
                False if a PageFault is generated to load the page
                None if the file cannot be made bigger (e.g. no more free blocks on the device)
        """
        task = self.getTask()
        pageTable = task.getPageTable()

        if isinstance(page, int):
            page = pageTable.getPage(page)

        file = self.getFile()
        iNode = file.getINode()
        device = file.getDevice()

        if logicalBlockNum >= len(iNode):
            totalBlocksNeeded = logicalBlockNum + 1
            success = iNode.allocateBlocks(totalBlocksNeeded)

            if success is False:
                return None

            file.setSize(len(iNode) * Globals.getPageSize())

        physicalBlockNum = iNode.getBlock(logicalBlockNum)

        if not suppressPageLock:
            if not pageTable.lockPage(page):
                return False

        frame = page.getFrame()

        if thread is not None:
            thread.sleep()

        io_request = IO_Request(
            task,
            device,
            physicalBlockNum,
            page,
            frame,
            self,
            IO_Request.IOWrite,
            thread
        )

        self.incrementIOCount()
        device.enqueue(io_request)
        return True

    def close(self):
        """
        Closes the file.  If there are still pending IO requests on this file,
        the close pending flag will be set to True and the file left open.
        When the device driver completes an IO requests, it checks to see if
        the last pending IO has been done and if the close pending flag is set.
        If both of these are true, then device driver will then call this function
        again, which will then be able to complete the close.

        Parameters:
            None

        Returns:
            None
        """
        if self.getNumIOs() > 0:
            self.setClosePending()
        else:
            self.clearClosePending()
            file = self.getFile()
            task = self.getTask()

            file.decrementOpenCount()
            task.removeOpenFile(self)

            if file.getOpenCount() <= 0 and file.getDeletePending():
                parentDir = file.getParentDir()
                if parentDir is not None:
                    parentDir.rm(file.getFilename())

    def delete(self, logicalBlockNum):
        """
        Deletes a block from the file. The physical block corresponding to this logical block number
        will be freed on the device and the total number of blocks for this file will be incremented
        by one.

        Parameters:
            logicalBlockNum: int

        Returns:
            None
        """
        file = self.getFile()
        iNode = file.getINode()

        iNode.deleteBlocks(logicalBlockNum, logicalBlockNum + 1)
        file.setSize(len(iNode) * Globals.getPageSize())

    def getTask(self):
        """
        Gets the task that owns the open file descriptor.  Even though threads
        open files, the files and open file descriptors are own by the tasks,
        therefore the threads share the same open files.

        Parameters:
            None

        Returns:
            task: Task
        """
        return self.__task

    def getFile(self):
        """
        Gets the file that is opened.

        Parameters:
            None

        Returns:
            file: File
        """
        return self.__file

    def getNumIOs(self):
        """
        Gets the number of pending IO requests on this file.  This is important
        because we can't completely close a file where there are IO requests
        that will still be serviced by the devices.  We have to have a
        "close pending" flag so that we can delay the closing of a file until
        all pending IO requests on this file have completed.

        Parameters:
            None

        Returns:
            IOCount: int
        """
        return self.__numIOs

    def incrementIOCount(self):
        """
        Increments the number of pending IO requests by one

        Parameters:
            None

        Returns:
            None
        """
        self.__numIOs += 1

    def decrementIOCount(self):
        """
        Decrements the number of pending IO requests by one

        Parameters:
            None

        Returns:
            None
        """
        self.__numIOs -= 1

    def closePending(self):
        """
        Return true if this file is pending a close after all IO requests have completed.

        Parameters:
            None

        Returns:
            boolean
        """
        return self.__closePending

    def setClosePending(self):
        """
        Sets the close pending flag to True

        Parameters:
            None

        Returns:
            None
        """
        self.__closePending = True

    def clearClosePending(self):
        """
        Clears the close pending flag (which means sets it to False)

        Parameters:
            None

        Returns:
            None
        """
        self.__closePending = False

    def __str__(self):
        """
        Returns a string representation of an open file descriptor.

        Parameters:
            None

        Returns:
            A string representation of an open file descriptor: string
        """
        # Feel free to modify this if you don't like the way open file descriptor are printing.

        return "OpenFile: " + str(self.getFile().getFilename())