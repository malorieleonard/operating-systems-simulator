"""
Globals. This File is imported by all other files in used in the simulator
so all the data that needs to be accessible to all modules goes in here.
This module is responsible for maintaining the input parameter files.
It also included the logMessage() function that allows students to write
any message to the log file.

Author: Clayton S. Ferner
Date: 4/15/2022

Classes:
    Globals
"""

import random
import time
import sys
import os
from Event import Event
from MyQueue import PriorityQueue
from SimExceptions import SimException


class Globals:
    """ Globals that need to be accessible by all other modules

    Attributes:
        Class (Static) Data:
            Task Status (not the same as Thread Status):
                TaskNew
                TaskReady
                TaskKill

            Thread Status (not the same as Task Status):
                ThreadNew
                ThreadReady
                ThreadRunning
                ThreadKill
                ThreadWaiting

            Interrupts:
                PageFault
                TaskCreate
                TaskKillInterrupt
                DiskInterrupt
                BlockDeviceInterrupt
                DeviceInterrupt
                TimerInterrupt
                PageFaultSwapInInterrupt
                PageFaultCleanUpInterrupt
                ReservedInterrupt1
                ReservedInterrupt2

            Simulation Parameters:
                maxTasks
                maxThreads
                seed
                paramFileName
                simulationTime
                maxFrames
                PageSize
                numAddressBits
                numRegisters
                numDevices
                numBlockDevices
                numDisks
                logFile
                users
                events
                numSnapShots

            Other Constants:
                PrivilegedMode
                UserMode

    Functions:
        Class (Static) Functions:
            initGlobals(cls, newSeed, paramFileName, echoToConsole)
            end(cls)
            logMessage(cls, message, level)
            getMaxNumTasks(cls) -> int
            getMaxNumThreads(cls) -> int
            getNumSnapshots(cls) -> int
            getSimulationTime(cls) -> int
            getTime(cls) -> int
            getMaxFrames(cls) -> int
            getPageSize(cls) -> int
            getNumAddressBits(cls) -> int
            getNumRegisters(cls) -> int
            getNumDevices(cls) -> int
            getNumBlockDevices(cls) -> int
            getNumDisks(cls) -> int
            getUsers(cls) -> list of strings
            setUserMode(cls)
            getMode(cls) -> Globals.PrivilegedMode or Globals.UserMode (int)
            getRescheduleNeeded(cls) -> boolean
            setRescheduleNeeded(cls)
            clearRescheduleNeeded(cls)
            getLogging(cls) -> int
            isSimulatorLogging(cls) -> boolean
            isHardwareLogging(cls) -> boolean
            isInterruptLogging(cls) -> boolean
            isDevicesLogging(cls) -> boolean
            isFilesLogging(cls) -> boolean
            isMemoryLogging(cls) -> boolean
            isThreadsLogging(cls) -> boolean
            isTasksLogging(cls) -> boolean
            addEvent(cls, Event)
            findEvent(cls, Event) -> Event
            removeEvents(cls, interruptType)
            peekEvent() -> Event
            dequeueEvent() -> Event
    """

    @classmethod
    def initGlobals(cls, newSeed, paramFileName, echoToConsole = False):
        """
        This is a class method that is called at the beginning of the simulation
        to read the parameters from the parameters file.

        Parameters:
            newSeed: boolean
                Whether or not to use a new random number seed.  If this is False, then the
                same sequences of event will happen.  That is useful for debugging, if the
                same things happend with each run.
            paramFileName: string
                This is the name of the parameters file to use for the simulation.
            echoToConsole: boolean (default False)
                Whether or not to echo the log messages to the console
        Returns:
            None
        """

    @classmethod
    def end(cls):
        """
        This is a class method that is called at the end of the simulation
        to write the parameters back to the parameters file.  Really, the only
        thing that would have changed is (potentially) the random number seed.

        Parameters:
            None
        Returns:
            None
        """

    @classmethod
    def logMessage(cls, message, level=None):
        """
        This function will write the message to the log file as well as the console.
        This is how one should produce debugging messages.

        Parameters:
            message: string
            level: int (default None) (None or zero - normal, 1 - Warning, 2 - Critical)

        Returns:
            None
        """

    @classmethod
    def getMaxNumTasks(cls):
        """
        Gets the Maximum number of tasks the simulator will generate at one time.

        Parameters:
            None

        Returns:
            maxTasks: int
        """

    @classmethod
    def getMaxNumThreads(cls):
        """
        Gets the Maximum number of threads that should be allowed per task.

        Parameters:
            None

        Returns:
            maxThreads: int
        """

    @classmethod
    def getNumSnapshots(cls):
        """
        Gets the number of snapshots that will be generated.

        Parameters:
            None

        Returns:
            numSnapShots: int
        """

    @classmethod
    def getSimulationTime(cls):
        """
        Gets the total length of the simulation.

        Parameters:
            None

        Returns:
            simulationTime: int
        """

    @classmethod
    def getTime(cls):
        """
        Gets the current time of the simulation.

        Parameters:
            None

        Returns:
            time: int
        """

    @classmethod
    def getMaxFrames(cls):
        """
        Gets the number of frames

        Parameters:
            None

        Returns:
            maxFrames: int
        """

    @classmethod
    def getPageSize(cls):
        """
        Gets the page size.

        Parameters:
            None

        Returns:
            PageSize: int
        """

    @classmethod
    def getNumAddressBits(cls):
        """
        Gets the number of bits used for an address (ex. 32 bits, 64 bits)

        Parameters:
            None

        Returns:
            numAddressBits: int
        """

    @classmethod
    def getNumRegisters(cls):
        """
        Gets the number of CPU registers.

        Parameters:
            None

        Returns:
            numRegisters: int
        """

    @classmethod
    def getNumDevices(cls):
        """
        Gets the number of devices, including disks, block devices, and character devices.

        Parameters:
            None

        Returns:
            numDevices: int
        """

    @classmethod
    def getNumBlockDevices(cls):
        """
        Gets the number of block devices

        Parameters:
            None

        Returns:
            numBlockDevices: int
        """

    @classmethod
    def getNumDisks(cls):
        """
        Gets the number of disks

        Parameters:
            None

        Returns:
            numDisks: int
        """

    @classmethod
    def getUsers(cls):
        """
        Gets the list of users

        Parameters:
            None

        Returns:
            users: list of strings
        """

    @classmethod
    def setUserMode(cls):
        '''Sets the mode back to "User" mode, so that user application do not have access to the full system.'''

    @classmethod
    def getMode(cls):
        '''Gets the mode: either Globals.PrivilegedMode or Globals.UserMode.'''

    @classmethod
    def getRescheduleNeeded(cls):
        '''This indicates that the scheduler needs to be called again when
        any interrupt has been handled. This is needed because some events,
        like the creation of a new task, the creation of a new thread, the
        waking of a thread, etc. are opportunities to reschedule.  But we
        can't run the scheduler while we are currently handling an interrupt.
        The running of the schedule needs to be delayed. '''

    @classmethod
    def setRescheduleNeeded(cls):
        '''Sets the flag to indicate that the scheduler needs to be called again when
        any interrupt has been handled. This is needed because some events,
        like the creation of a new task, the creation of a new thread, the
        waking of a thread, etc. are opportunities to reschedule.  But we
        can't run the scheduler while we are currently handling an interrupt.
        The running of the schedule needs to be delayed. '''

    @classmethod
    def clearRescheduleNeeded(cls):
        '''This clears the flag that indicates the scheduler needs to be called.  This is
        usually called by the simulator after it does call the scheduler. '''

    @classmethod
    def getLogging(cls):
        """
        Gets the Logging level

        Parameters:
            None

        Returns:
            logging: int
        """

    @classmethod
    def isSimulatorLogging(cls):
        """
        Returns true if Simulator logging is turned on

        Parameters:
            None

        Returns:
            boolean
        """

    @classmethod
    def isHardwareLogging(cls):
        """
        Returns true if Hardware logging is turned on

        Parameters:
            None

        Returns:
            boolean
        """

    @classmethod
    def isInterruptLogging(cls):
        """
        Returns true if Interrupt logging is turned on

        Parameters:
            None

        Returns:
            boolean
        """

    @classmethod
    def isDevicesLogging(cls):
        """
        Returns true if Devices logging is turned on

        Parameters:
            None

        Returns:
            boolean
        """

    @classmethod
    def isFilesLogging(cls):
        """
        Returns true if Files logging is turned on

        Parameters:
            None

        Returns:
            boolean
        """

    @classmethod
    def isMemoryLogging(cls):
        """
        Returns true if Memory logging is turned on

        Parameters:
            None

        Returns:
            boolean
        """

    @classmethod
    def isThreadsLogging(cls):
        """
        Returns true if Threads logging is turned on

        Parameters:
            None

        Returns:
            boolean
        """

    @classmethod
    def isTasksLogging(cls):
        """
        Returns true if Tasks logging is turned on

        Parameters:
            None

        Returns:
            boolean
        """

    @classmethod
    def addEvent(cls, event):
        """
        Adds an event to the queue of events. The Event queue is a PriorityQueue
        where priority is the time.

        Parameters:
            event: Event

        Returns:
            None
        """

    @classmethod
    def findEvent(cls, event):
        """
        Finds an event in the Event Queue.

        Parameters:
            event: Event

        Returns:
            event: Event or None if not found
        """

    @classmethod
    def removeEvents(cls, interruptType):
        """
        Removes ALL events with the interrupt type given as a parameter.

        Parameters:
            interruptType: int

        Returns:
            None
        """

    @classmethod
    def peekEvent(cls):
        """
        Returns the next event from the queue WITHOUT removing it.  Since the event queue
        is a priority queue where the time is the priority, it will return the earliest
        event in the queue.

        Parameters:
            None

        Returns:
            event: Event
        """

    @classmethod
    def dequeueEvent(cls):
        """
        Removes and returns the next event from the queue.  Since the event queue
        is a priority queue where the time is the priority, it will return the earliest
        event in the queue.

        Parameters:
            None

        Returns:
            event: Event
        """

