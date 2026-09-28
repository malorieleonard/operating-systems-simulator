# Student: Malorie Leonard
# Date: 03/31/2026

"""
Implements Memory Management in the Simulator.

Classes:
    MMU extends SimMMU
    PageTable
"""

import math
from Globals import Globals
from MyQueue import FIFOQueue
from Interrupts import Interrupt
from SimMemory import SimMMU, Frame, Page
from SimExceptions import SimException
from Hardware import CPU


class MMU(SimMMU):
    """ Implements the MMU (Memory Management Unit) in the Simulator.

    Attributes:
        Class (Static) Data:
            __PTBR
            __PageTableSize
            __FrameTable
            __frameQueue

    Functions:
        Class (Static) Functions:
            initMMU(cls)
            pageFaultHandler(cls)
            evictVictimPage(cls, frame)
            pageFaultSwapIn(cls)
            pageFaultCleanUp(cls)
            load(cls, address, register) -> boolean
            stor(cls, address, register) -> boolean
            removeFromFrameQueue(cls, frame)
            getPTBR(cls) -> PageTable
            setPTBR(cls, pageTable)
            getFrame(cls, frameNum) -> Frame or None
            getPageTableSize(cls) -> int
            getFrameTable(cls) -> list of Frames
            getFrameQueue(cls) -> queue of Frames
            snapshot(cls) -> string

        Instance Functions:
            none
    """

    __PTBR = None
    __PageTableSize = None
    __FrameTable = None
    __frameQueue = None

    @classmethod
    def initMMU(cls):
        """
        This is a class method that is called at boot time to initialize any class data.
        In particular, the FrameTable (among other things) must be initialized.

        Parameters:
            None
        Returns:
            None
        """
        assert Globals.getMode() == Globals.PrivilegedMode

        cls.__PTBR = None

        offsetBits = int(math.log2(Globals.getPageSize()))
        pageBits = Globals.getNumAddressBits() - offsetBits
        cls.__PageTableSize = 2 ** pageBits

        cls.__FrameTable = []
        for i in range(Globals.getMaxFrames()):
            cls.__FrameTable.append(Frame(i))

        cls.__frameQueue = FIFOQueue()

        Interrupt.registerHandler(Globals.PageFault, cls.pageFaultHandler)
        Interrupt.registerHandler(Globals.PageFaultSwapInInterrupt, cls.pageFaultSwapIn)
        Interrupt.registerHandler(Globals.PageFaultCleanUpInterrupt, cls.pageFaultCleanUp)

    @classmethod
    def pageFaultHandler(cls):
        """
        This is handler for a page fault. It initiates the page fault, but does not
        complete the process because of the possible need to swap in and swap out.
        It uses the evictVictimPage() to do the swap out and the pageFaultSwapIn()
        to do the swap in.

        Parameters:
            None

        Returns:
            None
        """
        assert Globals.getMode() == Globals.PrivilegedMode

        task = CPU.registers[1]
        thread = CPU.registers[2]
        page = CPU.registers[3]

        thread.sleep()

        if page.isThreadQueueEmpty():
            page.addThread(thread)
        else:
            page.addThread(thread)
            Globals.setUserMode()
            return

        selectedFrame = None

        for frame in cls.__FrameTable:
            if frame.isFree() and not frame.isReserved() and frame.getLockCount() == 0:
                selectedFrame = frame
                selectedFrame.setReserved(True)
                selectedFrame.setNewOwner(task)
                selectedFrame.setNewPage(page)
                selectedFrame.incrementLockCount()
                break

        if selectedFrame is None:
            if cls.__frameQueue.isEmpty():
                raise SimException("Out of Memory")

            victim = None
            iterator = cls.__frameQueue.newIterator()

            iterator.setCurrentFront()

            while not iterator.isPastEnd():
                candidate = iterator.getCurrentValue()

                if candidate.getLockCount() == 0 and not candidate.isReserved():
                    victim = candidate
                    break

                iterator.advance()

            if victim is None:
                raise SimException("Out of Memory")

            cls.removeFromFrameQueue(victim)

            victim.setReserved(True)
            victim.setNewOwner(task)
            victim.setNewPage(page)
            victim.incrementLockCount()
            selectedFrame = victim

            swapOutDone = cls.evictVictimPage(selectedFrame)

            if swapOutDone:
                CPU.registers[7] = selectedFrame
                Globals.setUserMode()
                return

        CPU.registers[7] = selectedFrame
        cls.pageFaultSwapIn()
        Globals.setUserMode()

    @classmethod
    def evictVictimPage(cls, frame):
        """
        This function evicts a page from a frame. The page may or may not
        need to be swapped out depending on if it has been modified since
        the last time swapping it. It returns True if a swap out was needed,
        False if a swap out was not done. This is important because the
        pageFaultHandler() needs to know whether it should call the
        pageFaultSwapIn() function directly or not.

        Parameters:
            frame: Frame

        Returns:
            boolean (whether a swap out was done or not)
        """
        assert Globals.getMode() == Globals.PrivilegedMode

        victimOwner = frame.getOwner()
        victimPage = frame.getPage()

        if victimPage is not None:
            victimPage.setValid(False)

        if victimOwner is None or victimPage is None:
            return False

        if not frame.isModified():
            return False

        logicalBlockNum = victimPage.getId()
        swapFile = victimOwner.getSwapFile()
        evictionCleanUpThread = cls.getEvictionCleanUpThread()

        swapFile.write(logicalBlockNum, victimPage, evictionCleanUpThread, True)
        return True

    @classmethod
    def pageFaultSwapIn(cls):
        """
        This is step 2 for handling for a page fault, which does the swap in of the
        new page. It is the steps after a swap out (if it was needed).

        Parameters:
            None

        Returns:
            None
        """
        assert Globals.getMode() == Globals.PrivilegedMode

        frame = CPU.registers[7]
        task = frame.getNewOwner()
        page = frame.getNewPage()

        if task.getStatus() == Globals.TaskKill:
            frame.setFree(True)
            frame.setOwner(None)
            frame.setPage(None)
            frame.setNewOwner(None)
            frame.setNewPage(None)
            frame.setModified(False)
            frame.setReserved(False)
            frame.setRefBit(0)
            frame.setLockCount(0)

            if page is not None:
                page.setValid(False)

            Globals.setUserMode()
            return

        page.setFrame(frame)

        logicalBlockNum = page.getId()
        swapFile = task.getSwapFile()
        pageFaultCleanUpThread = cls.getPageFaultCleanUpThread()

        swapFile.read(logicalBlockNum, page, pageFaultCleanUpThread, True)
        Globals.setUserMode()

    @classmethod
    def pageFaultCleanUp(cls):
        """
        This is the clean up for a page fault. It is run after all the swapping is complete.

        Parameters:
            None

        Returns:
            None
        """
        assert Globals.getMode() == Globals.PrivilegedMode

        frame = CPU.registers[7]
        task = frame.getNewOwner()
        page = frame.getNewPage()

        if task.getStatus() == Globals.TaskKill:
            frame.setFree(True)
            frame.setOwner(None)
            frame.setPage(None)
            frame.setNewOwner(None)
            frame.setNewPage(None)
            frame.setModified(False)
            frame.setReserved(False)
            frame.setRefBit(0)
            frame.setLockCount(0)

            if page is not None:
                page.setValid(False)

            Globals.setUserMode()
            return

        frame.setFree(False)
        frame.setOwner(task)
        frame.setPage(page)
        frame.setNewOwner(None)
        frame.setNewPage(None)
        frame.setModified(False)
        frame.setReserved(False)
        frame.setRefBit(1)
        frame.decrementLockCount()

        cls.__frameQueue.enqueue(frame)

        page.setFrame(frame)
        page.setValid(True)
        page.wakeThreads()

        Globals.setUserMode()

    @classmethod
    def load(cls, address, register):
        """
        Loads a byte from memory into a register

        Parameters:
            address (logical address): int
            register (register number): int

        Returns:
            boolean - success or failure
        """
        if cls.__PTBR is None:
            return False

        pageTable = cls.__PTBR
        task = pageTable.getTask()

        pageNum = address // Globals.getPageSize()
        offset = address % Globals.getPageSize()

        page = pageTable.getPage(pageNum)

        if page is None:
            raise SimException("Invalid page number in load")

        if not page.getValid():
            CPU.registers[0] = Globals.PageFault
            CPU.registers[1] = task
            CPU.registers[2] = task.getActiveThread()
            CPU.registers[3] = page
            Interrupt.trap(Globals.PageFault)
            return False

        frame = page.getFrame()
        frame.setRefBit(1)

        cls.removeFromFrameQueue(frame)
        cls.__frameQueue.enqueue(frame)

        physicalAddress = frame.getId() * Globals.getPageSize() + offset

        if Globals.isMemoryLogging():
            Globals.logMessage(
                "MMU: load(): loading byte from logical address " +
                str(address) + " to physical address " + str(physicalAddress) +
                " frame " + str(frame.getId()) + " offset " + str(offset)
            )

        CPU.registers[register] = cls.physicalMemory[physicalAddress]
        return True

    @classmethod
    def stor(cls, address, register):
        """
        Stores a byte from a register into memory

        Parameters:
            address (logical address): int
            register (register number): int

        Returns:
            boolean - success or failure
        """
        if cls.__PTBR is None:
            return False

        pageTable = cls.__PTBR
        task = pageTable.getTask()

        pageNum = address // Globals.getPageSize()
        offset = address % Globals.getPageSize()

        page = pageTable.getPage(pageNum)

        if page is None:
            raise SimException("Invalid page number in stor")

        if not page.getValid():
            CPU.registers[0] = Globals.PageFault
            CPU.registers[1] = task
            CPU.registers[2] = task.getActiveThread()
            CPU.registers[3] = page
            Interrupt.trap(Globals.PageFault)
            return False

        frame = page.getFrame()
        frame.setRefBit(1)
        frame.setModified(True)

        cls.removeFromFrameQueue(frame)
        cls.__frameQueue.enqueue(frame)

        physicalAddress = frame.getId() * Globals.getPageSize() + offset

        if Globals.isMemoryLogging():
            Globals.logMessage(
                "MMU: stor(): storing byte from register " +
                str(register) + " to logical address " + str(address) +
                " physical address " + str(physicalAddress) +
                " frame " + str(frame.getId()) + " offset " + str(offset)
            )

        cls.physicalMemory[physicalAddress] = CPU.registers[register]
        return True

    @classmethod
    def removeFromFrameQueue(cls, frame):
        """
        Removes a frame from the Frame queue

        Parameters:
            frame: Frame

        Returns:
            None
        """
        newQueue = FIFOQueue()

        while not cls.__frameQueue.isEmpty():
            current = cls.__frameQueue.dequeue()
            if current != frame:
                newQueue.enqueue(current)

        cls.__frameQueue = newQueue

    @classmethod
    def getPTBR(cls):
        """
        Gets the Page Table Base Register (PTBR).

        Parameters:
            None

        Returns:
            PTBR: PageTable
        """
        return cls.__PTBR

    @classmethod
    def setPTBR(cls, pageTable):
        """
        Sets the Page Table Base Register (PTBR).

        Parameters:
            pageTable: PageTable

        Returns:
            None
        """
        cls.__PTBR = pageTable

    @classmethod
    def getFrame(cls, frameNum):
        """
        Gets a frame give its number or id.

        Parameters:
            frameNum: int

        Returns:
            Frame or None if frameNum is out of range
        """
        if frameNum < 0 or frameNum >= len(cls.__FrameTable):
            return None
        return cls.__FrameTable[frameNum]

    @classmethod
    def getPageTableSize(cls):
        """
        Gets the size of the page table (specifically, the number of pages,
        not the number of bytes).

        Parameters:
            None

        Returns:
            page table size: int
        """
        return cls.__PageTableSize

    @classmethod
    def getFrameTable(cls):
        """
        Gets the frame table (the entire table).

        Parameters:
            None

        Returns:
            list of frames
        """
        return cls.__FrameTable

    @classmethod
    def getFrameQueue(cls):
        """
        Gets the frame queue.

        Parameters:
            None

        Returns:
            queue of Frames
        """
        return cls.__frameQueue

    @classmethod
    def snapshot(cls):
        """
        Takes a snapshot of the current state of memory (specifically, the frame table) and
        returns it as a string (suitable for printing).

        Parameters:
            None

        Returns:
            string
        """
        frameTable = cls.getFrameTable()
        frameQueue = cls.getFrameQueue()
        result = "\n\n\t\t\tFrame Table:\n"
        result += "# \t    \t     \t    \tLock \t        \t        \t      \t  \n"
        result += "# \tFree\tOwner\tPage\tCount\tReserved\tModified\tRefBit\tRO\n"
        result += "-" * 90 + "\n"
        for frame in frameTable:
            result += str(frame.getId()) + "\t"

            if frame.isFree():
                result += "Free" + "\t"
            else:
                result += "Used" + "\t"

            if frame.getOwner() is not None:
                result += str(frame.getOwner().getId()) + "   \t"
            else:
                result += "     " + "\t"

            if frame.getPage() is not None:
                result += str(frame.getPage().getId()) + "   \t"
            else:
                result += "     " + "\t"

            result += str(frame.getLockCount()) + "    \t"

            if frame.isReserved():
                result += "R" + "       \t"
            else:
                result += "        " + "\t"

            if frame.isModified():
                result += "M        " + "\t"
            else:
                result += "        " + "\t"

            result += str(frame.getRefBit()) + "\t"

            if frame.isReadOnly():
                result += "RO" + "\n"
            else:
                result += "  " + "\n"

        result += "-" * 90 + "\n"

        result += "Frame Queue:\n"
        result += str(frameQueue)
        result += "\n\n"
        return result


class PageTable:
    """ This is the implements a PageTable.

    Functions:
        Class (Static) Functions:
            none

        Instance Functions:
            __init__(self, task) (Constructor)
            getPage(self, pageNum) -> Page
            getTask(self) -> Task
            lockPage(self, page) -> boolean
            unLockPage(self, page)
            deallocatePages(self)
            __str__(self) -> string
    """

    def __init__(self, task):
        """
        This is the constructor.

        Parameters:
            task: Task

        Returns:
            None
        """
        self.__task = task
        self.__pageTable = []

        for i in range(MMU.getPageTableSize()):
            self.__pageTable.append(Page(i))

    def getPage(self, pageNum):
        """
        Gets a page from the page table based upon its id or index.
        Returns None if the page number is not within range.

        Parameters:
            page number: int

        Returns:
            page: Page or None
        """
        if pageNum < 0 or pageNum >= len(self.__pageTable):
            return None
        return self.__pageTable[pageNum]

    def getTask(self):
        """
        Gets the task that owns this page table.

        Parameters:
            None

        Returns:
            owner: Task
        """
        return self.__task

    def lockPage(self, page):
        """
        Locks a page into memory. This is a little different than simply incrementing the
        lock count on a frame. The reason is because the page may not be in a frame yet.
        If the page is not yet valid, it will generate a page fault to get it into a frame.
        It returns False if a page fault is generated, so that the lockPage() can be called
        again after the pagefault is completed. If there is no page fault, and the page
        can be locked right away, True is returned.

        Parameters:
            page: Page

        Returns:
            boolean
        """
        if not page.getValid():
            CPU.registers[0] = Globals.PageFault
            CPU.registers[1] = self.__task
            CPU.registers[2] = self.__task.getActiveThread()
            CPU.registers[3] = page
            Interrupt.trap(Globals.PageFault)
            return False

        frame = page.getFrame()
        frame.incrementLockCount()
        return True

    def unLockPage(self, page):
        """
        UnLocks a page. This actually just decrements the lock count and may not completely unlock it
        because there may be multiple I/O operations on this page. That is why the lock count is a
        counter and not a boolean. This will not generate a PageFault since the page should already
        have been locked into a frame.

        Parameters:
            page: Page

        Returns:
            None
        """
        frame = page.getFrame()
        frame.decrementLockCount()

        if frame.getLockCount() < 0:
            raise SimException("Lock count became negative")

    def deallocatePages(self):
        """
        This function deallocates all of the pages for a task. This function should be used when
        a task is killed or terminates, therefore freeing up its memory. There is no need to
        swap anything out, because it is being killed. It was up to the task or threads
        to save anything it needed to a device already.

        Parameters:
            None

        Returns:
            None
        """
        for page in self.__pageTable:
            if page.getValid():
                frame = page.getFrame()
                frame.setFree(True)
                frame.setOwner(None)
                frame.setPage(None)
                frame.setNewOwner(None)
                frame.setNewPage(None)
                frame.setModified(False)
                frame.setReserved(False)
                frame.setRefBit(0)
                MMU.removeFromFrameQueue(frame)
                page.setValid(False)

    def __str__(self):
        """
        Returns a string representation of a page table useful for logging purposes.

        Parameters:
            None
        Returns:
            A string representation of a page table (suitable for printing): string
        """
        result = "\n           Task " + str(self.getTask()) + " PageTable \n"
        result += "           Page\tFrame\tValid\n"
        for i in range(MMU.getPageTableSize()):
            result += "           " + str(self.getPage(i).getId()) + "\t"

            if not self.getPage(i).getValid():
                result += "  -  \t"
            else:
                result += str(self.getPage(i).getFrame().getId()) + "\t"

            if self.getPage(i).getValid():
                result += "T\n"
            else:
                result += "F\n"

        return result