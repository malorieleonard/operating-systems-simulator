# Student: Malorie Leonard
# Date: 03/09/2026

"""
Implements a Thread in the Simulator.

Classes:
    Thread extends SimThread

"""

from Globals import Globals
from Hardware import Timer, CPU
from Memory import MMU
from Interrupts import Interrupt
from MyQueue import PriorityQueue
from SimThreads import SimThread
from SimExceptions import SimException

class Thread(SimThread):
    """ Implements a Thread in the Simulator.

    Attributes:
        Class (Static) Data:
            __readyQueue : PriorityQueue
                 The ready-to-run queue of threads
            __Quantum : int
                 This is an optional field that would be used when implemented Round-Robin
            __alpha : float
                 This is a weighted average of the last burst length and the last estimate
                 This value should be between 0 and 1 (inclusive).
            __initialEstimate
                 This value should be the estimated burst length for new threads (for which
                 there is no history).

    Functions:
        Class (Static) Functions:
            initThreads(cls)
            scheduler(cls)
            getReadyQueue(cls) -> queue
            snapshot(cls) -> string

        Instance Functions:
            __init__(self, id, task, nonPreemptive) (Constructor)
            kill(self)
            sleep(self)
            wake(self, frame = None)
            getId(self) -> int
            getStatus(self) -> Thread Status
            getTask(self) -> Task
            getNonPreemptive(self) -> boolean
            getPriority(self) -> int
            getKey(self) -> int
            __eq__(self, other) -> boolean
            __ne__(self, other) -> boolean
            __str__(self) -> string

    """
    __readyQueue = None
    __quantum = 50

    @classmethod
    def initThreads(cls):
        """
        This is a class method that is called at boot time to initialize any class data.

        Parameters:
            None

        Returns:
            None
        """

        assert Globals.getMode() == Globals.PrivilegedMode
        cls.__readyQueue = PriorityQueue()
        Interrupt.registerHandler(Globals.TimerInterrupt, cls.scheduler)

    def __init__(self, id, task, nonPreemptive = False):
        """
        This is the constructor.

        Parameters:
            id: int
            task: Task
            nonPreemptive: boolean (default is False)

        Returns:
            None
        """
        super().__init__(id, task, nonPreemptive)

        self.__id = id
        self.__task = task
        self.__nonPreemptive = nonPreemptive
        self.__status = Globals.ThreadNew
        self.__lastDispatched = 0
        self.__priority = task.getPriority()
        self.__status = Globals.ThreadReady

        Thread.__readyQueue.enqueue(self)

    def kill(self):
        """
        Kills the thread.

        Parameters:
            None

        Returns:
            None
        """
        super().kill()

        if self.__status == Globals.ThreadRunning:
            Timer.clearTimer()
            MMU.setPTBR(None)
            Globals.setRescheduleNeeded()

        elif self.__status == Globals.ThreadReady:
            Thread.__readyQueue.remove(self)

        self.__status = Globals.ThreadKill
        self.__task.removeThread(self)

        if self.__task.getStatus() != Globals.TaskKill and self.__task.getNumThreads() <= 0:
            CPU.registers[0] = Globals.TaskKillInterrupt
            CPU.registers[1] = self.__task
            Interrupt.trap(Globals.TaskKillInterrupt)

    def sleep(self):
        """
        Puts a thread to sleep (or puts it in a waiting state).

        Parameters:
            None

        Returns:
            None
        """
        super().sleep()

        if self.__status == Globals.ThreadRunning:
            Timer.clearTimer()
            MMU.setPTBR(None)
            self.__task.setActiveThread(None)
            self.__status = Globals.ThreadWaiting
            Globals.setRescheduleNeeded()

        elif self.__status == Globals.ThreadReady:
            Thread.__readyQueue.remove(self)
            self.__status = Globals.ThreadWaiting

        else:
            self.__status += 1

    def wake(self, frame = None):
        """
        Wakes up a thread, although it may only decrement the waiting counter leaving
        it still in a waiting state.

        Parameters:
            frame: Frame (default None)

        Returns:
            None
        """
        assert Globals.getMode() == Globals.PrivilegedMode

        super().wake(frame)

        if self.__priority < 0:
            self.__status = Globals.ThreadReady
            Thread.__readyQueue.enqueue(self)
            Globals.setRescheduleNeeded()

        elif self.__status <= Globals.ThreadWaiting:
            self.__status = Globals.ThreadReady
            self.__priority = max(0, self.__priority - 1)
            Thread.__readyQueue.enqueue(self)
            Globals.setRescheduleNeeded()

        else:
            self.__status -= 1

    @classmethod
    def scheduler(cls):
        """
        This is the scheduler.  Its job is to decide which thread should run next.
        It is also the handler for the timer interrupt. The scheduler should be
        called whenever there is an "opportunity" to reschedule. An "opportunity" is:
            - The timer interrupt occurs
            - A new thread is created
            - A thread is added to the queue because:
               + a new thread was create
               + a thread was woken
            - The current running thread has stopped because:
               + it was killed or terminated
               + it is put to sleep
        There is a Global flag (see Globals.setRescheduleNeeded()) that indicates
        there is an "opportunity" to reschedule, which will invoke the scheduler.
        The reason that flag should be used instead of just calling the scheduler
        is because a system call or interrupt handler must complete its work before
        the scheduler can reschedule.  Therefore, we need to delay that call to the
        scheduler.

        Parameters:
            None

        Returns:
            None
        """
        assert Globals.getMode() == Globals.PrivilegedMode
        ptbr = MMU.getPTBR()

        if ptbr is not None:
            task = ptbr.getTask()

            if task is not None:
                activeThread = task.getActiveThread()

                if activeThread is not None:
                    if activeThread.getNonPreemptive():
                        Globals.setUserMode()
                        return

                    nextThread = cls.__readyQueue.peek()
                    interruptType = CPU.registers[0]

                    if interruptType == Globals.TimerInterrupt:
                        activeThread.__status = Globals.ThreadReady
                        activeThread.__priority += 1
                        cls.__readyQueue.enqueue(activeThread)
                        Timer.clearTimer()
                        MMU.setPTBR(None)

                    elif nextThread is not None and nextThread.getPriority() < activeThread.getPriority():
                        activeThread.__status = Globals.ThreadReady
                        cls.__readyQueue.enqueue(activeThread)
                        Timer.clearTimer()
                        MMU.setPTBR(None)

                    else:
                        activeThread.__lastDispatched = Globals.getTime()
                        Globals.setUserMode()
                        return
        if MMU.getPTBR() is None:

            if not cls.__readyQueue.isEmpty():
                thread = cls.__readyQueue.dequeue()
                task = thread.getTask()
                task.setActiveThread(thread)
                thread.__status = Globals.ThreadRunning
                MMU.setPTBR(task.getPageTable())
                thread.__lastDispatched = Globals.getTime()
                Timer.clearTimer()
                Timer.setTimer(Globals.getTime() + cls.__quantum)
                Globals.setUserMode()
                return

        Globals.setUserMode()

    def getId(self):
        """
        Gets the thread's id.

        Parameters:
            None

        Returns:
            id: int
        """
        return self.__id

    def getStatus(self):
        """
        Gets the thread's status.

        Parameters:
            None

        Returns:
            id: int
        """
        return self.__status

    def getTask(self):
        """
        Gets the thread's task.

        Parameters:
            None

        Returns:
            task: Task
        """
        return self.__task

    def getNonPreemptive(self):
        """
        Gets the thread's non-preemptive status.

        Parameters:
            None

        Returns:
            non-preemptive status: boolean
        """
        return self.__nonPreemptive

    def getPriority(self):
        """
        Gets the thread's priority.

        Parameters:
            None

        Returns:
            priority: int
        """
        return self.__priority

    def getKey(self):
        """
        Gets the thread's key.  The Priority Queue looks specifically for a function
        called "getKey()" that it can call to determine the ordering of values in
        a queue.  Since we will want to use a priority queue where a thread's priority
        is how it should order them, this function simply return the priority of the thread.

        Parameters:
            None

        Returns:
            key: int
        """
        return self.__priority

    def __eq__(self, other):
        """
        Determines if two threads are equal based upon their task id's and
        thread id's.

        Parameters:
            self: Thread
            other: Thread

        Returns:
            True if self and other are the same thread, False otherwise.
        """
        if other is None:
            return False

        return (self.getId() == other.getId() and
                self.getTask().getId() == other.getTask().getId())

    def __ne__(self, other):
        """
        Determines if two threads are not equal based upon their task id's and
        thread id's.

        Parameters:
            self: Thread
            other: Thread

        Returns:
            True if self and other are not the same thread, False otherwise.
        """
        return not self.__eq__(other)

    def __str__(self):
        """
        Returns a string representation of a thread useful for logging purposes.

        Parameters:
            None

        Returns:
            A string representation of a thread: string
        """
        return "Thread " + str(self.getTask().getId()) + ":" + str(self.getId()) + \
               "(" + self.getPrettyStatus() + " P" + str(self.getPriority()) + ")"

    @classmethod
    def getReadyQueue(cls):
        """
        This returns the Ready-to-run queue.  It's main purpose is to allow the
        Simulator to check the queue for errors.

        Parameters:
            None

        Returns:
            The ready queue: Priority Queue
        """
        return cls.__readyQueue

    @classmethod
    def snapshot(cls):
        """
        Takes a snapshot of the current state of the threads (specifically, the ready queue) and
        returns it as a string (suitable for printing).

        Parameters:
            None

        Returns:
            string
        """
        result = ""
        readyQ = cls.getReadyQueue()
        result += "Student's Ready Queue = \n" + str(readyQ) + "\n"
        return result