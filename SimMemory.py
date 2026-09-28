"""
This is the super class of the Memory class used by the Simulator.

Author: Clayton S. Ferner
Date: 8/5/2022

Classes:
    SimMMU
    Frame
    Page
"""


import math
from Globals import Globals
from MyQueue import FIFOQueue
from SimExceptions import SimException

class SimMMU:
    """ This is the super class of the MMU (Memory Management Unit) class.
    Attributs:
        Class (Static) Attributes:
            physicalMemory (list of size Globals.getPageSize() * Globals.getMaxFrames())

    Functions:
        Class (Static) Functions:
            initSimMMU(cls)
            getPageFaultCleanUpThread() -> Thread
            getEvictionCleanUpThread() -> Thread

        Instance Functions:
            none
    """

    @classmethod
    def initSimMMU(cls):
        """
        Initializes the physical memory to empty cells. The size of the memory is
        number of Frames * page size.  The memory can be accessed directly using
        SimMemory.physicalMemory[<physical addresss>]

        Parameters:
            None

        Returns:
            None
        """

    @classmethod
    def getPageFaultCleanUpThread(cls):
        """
        Gets the thread that is used to call the PageFault cleanup.  Since the page
        fault might cause a swap in (as well as a possible swap out) we need to have
        the device driver call the pagefault clean up.  We do not know when the
        swap in will complete. This thread's only job is to execute the pageFaultCleanUp().

        Parameters:
            None

        Returns:
            Thread that call the pageFaultCleanUp : Thread
        """

    @classmethod
    def getEvictionCleanUpThread(cls):
        """
        Gets the thread that is used to call the PageFault eviction cleanup.  Since
        evicting a page may cause a swap out, we need to have the device driver call
        the pageFaultSwapIn to continue with the page fault. We do not know when the
        swap out will complete. This thread's only job is to execute the pageFaultSwapIn().

        Parameters:
            None

        Returns:
            Thread that call the pageFaultCleanUp : Thread
        """

class Frame:
    """ This implements a Frame

    Functions:
        Class (Static) Functions:
            none

        Instance Functions:
            __init__(self, id) (Constructor)
            getId(self) -> int
            isFree(self) -> boolean
            getOwner(self) -> Task
            getPage(self) -> Page
            getLockCount(self) -> int
            getRefBit(self) -> int
            isReserved(self) -> boolean
            isModified(self) -> boolean
            isReadOnly(self) -> boolean
            getNewOwner(self) -> Task
            getNewPage(self) -> Page
            setFree(self, boolean)
            setOwner(self, Task)
            setPage(self, Page)
            setNewOwner(self, Task)
            setNewPage(Pself, age)
            setLockCount(self, lockCount)
            incrementLockCount(self)
            decrementLockCount(self)
            setReserved(self, reserved)
            setModified(self, modified)
            setRefBit(self, refit)
            setReadOnly(self, RO)
            __str__(self) -> string
            verbose_str(self) -> string


    """
    def __init__(self, id):
        """
        This is the constructor.

        Parameters:
            id: int

        Returns:
            None
        """

    def getId(self):
        """
        Gets the id. This should match the list index.  For example FrameTable[i].getId() == i.

        Parameters:
            None

        Returns:
            frame number: int
        """

    def isFree(self):
        """
        Indicates whether the frame is free or not.

        Parameters:
            None

        Returns:
            free: boolean
        """

    def getOwner(self):
        """
        Gets the owner. Tasks own frames/pages, not threads.

        Parameters:
            None

        Returns:
            owner: Task
        """

    def getPage(self):
        """
        Gets the page that is loaded into this frame.

        Parameters:
            None

        Returns:
            page: Page
        """

    def getLockCount(self):
        """
        Gets the lock count of this frame.

        Parameters:
            None

        Returns:
            int
        """

    def getRefBit(self):
        """
        Gets the reference bit of this frame.

        Parameters:
            None

        Returns:
            int
        """

    def isReserved(self):
        """
        Indicates whether the frame is reserved or not. Since a page fault may cause
        swapping, which can take a long time, a frame could potentially be stolen by
        another page fault before the swapping finishes.  The reserved flag is to
        prevent that.  We can't set the frame a not free, because selecting a victim
        means selecting a used frame.  We can't set the owner, because we need the
        old and new owners throughout the process.  We can't use the lock count because
        that is used for a different purpose. Having the reserved flag allows us to grab
        and hold on to a frame until we can complete the page fault.

        Parameters:
            None

        Returns:
            reserved: boolean
        """

    def isModified(self):
        """
        Indicates whether the frame has been modified. The purpose is to know whether
        we need to do a swap out if this frame is selected as a victim.  The frame is
        modified if it has been changed since the last swap in.  Changes to the frame
        are made when we do a "stor" from a register to memory, or we do a read() on a
        file from disk to memory.

        Parameters:
            None

        Returns:
            modified: boolean
        """

    def isReadOnly(self):
        """
        Indicates whether the frame is read-only. The purpose is so that we can
        prevent things like self-modifying programs.  If an operation that would
        modify memory is done on a read-only frame, it should cause an exception.
        Presently, this is not being used and all memory is writable.

        Parameters:
            None

        Returns:
            modified: boolean
        """

    def getNewOwner(self):
        """
        Gets the new owner. During the page fault process, we may have to swap out
        a victim page (which has a victim task and victim page), and then swap in
        the new page (which could be a different set of task and page).  Since we
        need both sets at different parts of the page fault process, we want to
        keep both (the victim and the new) until we are done.

        Parameters:
            None

        Returns:
            owner: Task
        """

    def getNewPage(self):
        """
        Gets the new page. During the page fault process, we may have to swap out
        a victim page (which has a victim task and victim page), and then swap in
        the new page (which could be a different set of task and page).  Since we
        need both sets at different parts of the page fault process, we want to
        keep both (the victim and the new) until we are done.

        Parameters:
            None

        Returns:
            page: Page
        """

    def setFree(self, free):
        """
        Sets the frame as free.

        Parameters:
            free: boolean

        Returns:
            None
        """


    def setOwner(self, owner):
        """
        Sets the owner of a frame.

        Parameters:
            owner: Task

        Returns:
            None
        """


    def setPage(self, page):
        """
        Sets the page of a frame.

        Parameters:
            page: Page

        Returns:
            None
        """


    def setNewOwner(self, owner):
        """
        Sets the new owner of a frame.

        Parameters:
            owner: Task

        Returns:
            None
        """


    def setNewPage(self, page):
        """
        Sets the new page of a frame.

        Parameters:
            page: Page

        Returns:
            None
        """


    def setLockCount(self, lockCount):
        """
        Sets the lock count of a frame.

        Parameters:
            lock count: int

        Returns:
            None
        """


    def incrementLockCount(self):
        """
        Increments the lock count of a frame by 1. This function should ONLY be
        called from one of the memory related classes (SimMMU, MMU, Frame, Page,
        or PageTable classes).

        Parameters:
            None

        Returns:
            None
        """

    def decrementLockCount(self):
        """
        Decrements the lock count of a frame by 1. This function should ONLY be
        called from one of the memory related classes (SimMMU, MMU, Frame, Page,
        or PageTable classes).

        Parameters:
            None

        Returns:
            None
        """

    def setReserved(self, reserved):
        """
        Sets the reserved flag of a frame.

        Parameters:
            reserved: boolean

        Returns:
            None
        """

    def setModified(self, modified):
        """
        Sets the modified flag of a frame.

        Parameters:
            modified: boolean

        Returns:
            None
        """

    def setRefBit(self, refbit):
        """
        Sets the reference bit of a frame.

        Parameters:
            value: int (although it should only be zero or one)

        Returns:
            None
        """

    def setReadOnly(self, RO):
        """
        Sets the read-only flag of a frame.

        Parameters:
            RO: boolean

        Returns:
            None
        """

    def __str__(self):
        """
        Returns a string representation of a frame (suitable for printing).

        Parameters:
            None

        Returns:
            A string representation of a frame: string
        """

        result = "Frame(" + str(self.getId())
        if self.getOwner() is None:
            result += " None "
        else:
            result += " Task " + str(self.getOwner().getId())
        if self.getPage() is None:
            result += " None "
        else:
            result += " Page " + str(self.getPage().getId())
        if self.getLockCount() > 0:
            result += " " + "L" + str(self.getLockCount())
        result += " " + "rb" + str(self.getRefBit())
        result += ")"
        return result
    def verbose_str(self):
        """
        Returns a string representation of a frame (suitable for printing).

        Parameters:
            None

        Returns:
            A string representation of a frame: string
        """

        result = "Frame(" + str(self.getId())
        if self.isFree():
            result += " Free"
        result += " " + str(self.getOwner())
        result += " " + str(self.getPage())
        if self.getLockCount() > 0:
            result += " " + "L" + str(self.getLockCount())
        if self.isReserved():
            result += " R"
        if self.isModified():
            result += " M"
        result += " " + "rb" + str(self.getRefBit())
        if self.isReadOnly():
            result += " RO"
        result += ")"
        return result

class Page:
    """  This implements a Page

    Functions:
        Class (Static) Functions:
            none

        Instance Functions:
            __init__(self, id) (Constructor)
            getId(self) -> int
            getFrame(self) -> Frame
            getValid(self) -> boolean
            setFrame(self, frame)
            setValid(self, valid)
            __str__(self) -> string
            addThread(self, thread)
            isThreadQueueEmpty(self) -> boolean
            wakeThreads(self)

    """
    def __init__(self, id):
        """
        This is the constructor.

        Parameters:
            id: int

        Returns:
            None
        """

    def getId(self):
        """
        Gets the id. This should match the list index.  For example pageTable[i].getId() == i.

        Parameters:
            None

        Returns:
            page number: int
        """

    def getFrame(self):
        """
        Gets the frame this page is loaded into.

        Parameters:
            None

        Returns:
            frame: Frame
        """

    def getValid(self):
        """
          Indicates whether this page is loaded into a frame or not. In other words, can
          the frame be reliably used, or is a page fault required?

          Parameters:
              None

          Returns:
              valid: boolean
          """

    def setFrame(self, frame):
        """
        Sets the frame for this page.

        Parameters:
            frame: Frame

        Returns:
            None
        """

    def setValid(self, valid):
        """
        Sets the frame for this page.

        Parameters:
            valid: boolean

        Returns:
            None
        """

    def __str__(self):
        """
        Returns a string representation of a page (suitable for printing).

        Parameters:
            None

        Returns:
            A string representation of a page: string
        """

        result = "Page(" + str(self.getId())
        if self.getValid():
            result += " F" + str(self.getFrame().getId())
        result += ")"
        return result
    def addThread(self, thread):
        """
        Adds a thread to the threadQueue for this page.  Threads in the queue are threads
        that are waiting for this page to be loaded into memory (specifically a PageFault).
        Multiple reference to the same page can cause multiple page fault.  To prevent
        multiple pagefauls, if a thread causes a page fault, and the queue for that page
        is not empty, then it is already in a page fault, in which case we can just add
        the thread and not generate another page fault.  When the original page fault is done,
        ALL of the threads in this queue will be woken up.

        Parameters:
            thread: Thread

        Returns:
            None
        """

    def isThreadQueueEmpty(self):
        """
        Checks to see if the thread queue is empty

        Parameters:
            none

        Returns:
            boolean
        """

    def wakeThreads(self):
        """
        Wakes up all of the threads in the thread queue of this page.  Basically, the page fault
        has not been completed, so any and all threads waiting for that page fault to finish may
        now continue.

        Parameters:
            None

        Returns:
            None
        """
