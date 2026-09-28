"""
This is the super class of the Thread class used by the Simulator.

Author: Clayton S. Ferner
Date: 7/19/2022

Classes:
    SimThread
"""


import random
from Globals import Globals
from Memory import MMU
from SimMemory import SimMMU
from SimExceptions import SimException
from Interrupts import Interrupt
from Hardware import CPU

class SimThread:
    """
    This is the super class of the Thread class used by the Simulator.

    Functions:
        Class (Static) Functions:
            initSimThreads(cls)
            getSummary(cls) -> string

        Instance Functions:
            __init__(self, id, task, nonPreemptive = False) (Constructor)
            kill(self)
            sleep(self)
            wake(self, frame = None)
            getPrettyStatus(self) -> string
            getAccumulatedCPUTime(self) -> int
            getLastBurstLength(self) -> int
            clearLastBurstLength(self)
            getReadyWaitingTime(self) -> int
            getWaitingTime(self) -> int
            getBurstStartTime(self) -> int
    """

    @classmethod
    def initSimThreads(cls):
        """
        This is a class method that is called at boot time to initialize any class data.

        Parameters:
            None
        Returns:
            None
        """
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
    def kill(self):
        """
        This doesn't do anything. It is up to the kill() in the Thread class to do
        the actual killing. This function is meant to record that the thread should be
        killed so that some error checking can be done.

        Parameters:
            None

        Returns:
            None
        """
    def sleep(self):
        """
        This doesn't do anything. It is up to the sleep() in the Thread class to do
        the actual sleeping. This function is meant to record that the thread should
        have been put to sleep so that some error checking can be done.

        Parameters:
            None

        Returns:
            None
        """
    def wake(self, frame = None):
        """
        This doesn't do anything. It is up to the wake() in the Thread class to do
        the actual waking. This function is meant to record that the thread should
        have been woken so that some error checking can be done.

        Parameters:
            frame: Frame (default None)

        Returns:
            None
        """
    def getPrettyStatus(self):
        """
        Give the status as a word instead of an integer.  For example, it would return
        "ThreadRunning" instead of 716.

        Parameters:
            None

        Returns:
            The thread's status as a word: string
        """
    def getAccumulatedCPUTime(self):
        """
        Returns the accumulated CPU time so far (in clock ticks).

        Parameters:
            None

        Returns:
            The thread's accumulated CPU time: int
        """
    def getLastBurstLength(self):
        """
        Returns the length of the last CPU burst (in clock ticks).

        Parameters:
            None

        Returns:
            The thread's last CPU burst: int
        """
    def clearLastBurstLength(self):
        """
        Sets the last CPU burst to zero.

        Parameters:
            None

        Returns:
            None
        """
    def getReadyWaitingTime(self):
        """
        Returns the accumulated time spent in the ready-to-run queue.

        Parameters:
            None

        Returns:
            The thread's time spent in the ready-to-run queue (clock ticks): int
        """
    def getWaitingTime(self):
        """
        Returns the accumulated time spent in a waiting state (waiting for IO).
        This is the time spent in the ThreadWaiting state, not the ThreadReady state.

        Parameters:
            None

        Returns:
            The thread's time spent in a waiting state (waiting for IO) (clock ticks): int
        """
    def getBurstStartTime(self):
        """
        Returns the time when this burst was submitted to the ready queue (The first time
        it was changed to ThreadReady from a state other than ThreadRunning).

        Parameters:
            None

        Returns:
            The thread's time when this burst was submitted to the ready queue (clock ticks): int
        """
    @classmethod
    def getSummary(cls):
        """
        This provides a summary of the thread times, like average time spent
        waiting in the ready queue, average time waiting for I/O, and average
        running time.

        Parameters:
            None

        Returns:
            Summary: string
        """

