"""
This is the Simulator class that runs everything.

Author: Clayton S. Ferner
Date: 7/19/2022

Classes:
    Simulator
"""



import random
import time
import os

from Globals import Globals
from Files import File
from SimExceptions import SimException
from SimTasks import SimTask
from SimThreads import SimThread
from Tasks import Task
from Threads import Thread
from MyQueue import PriorityQueue,QueueIterator
# from Event import Event
from Memory import MMU
from SimMemory import SimMMU
from Hardware import *
from Interrupts import Interrupt
from Devices import Device,BlockDevice
from Disks import Disk
# from IO_Request import IO_Request
from Users import User


class Simulator:
    """
    This is the main Simulator class that runs everything.
    You really shouldn't call anything in this class, but rather run
    The BootStrap module which start everything off.

    Functions:
        __init__(newSeed, paramFileName)
        snapshot()
        start()
        end()
    """
    def __init__(self, newSeed, paramFileName, echoToConsole):
        """
        This is the constructor.

        Parameters:
            newSeed: boolean
                If newSeed is True, then the simulator will create a new sequence of events
                If newSeed is False, the simulator will have the same events as the last
                  run, making it easier to debug, because the exact same things happen again.

            paramFileName: string
                Name of the parameter file to use

        Returns:
            None
        """
    def setup(self):
        """
        Does some initial setup of the simulator to get thrings ready.  This should be
        called after the constructor but before the start() function.  The purpose of
        having this function is that it contains thing that are needed for the simulator
        but are not needed when running -debug mode where the simulator just runs
        some tests on the students code.

        Parameters:
            None

        Returns:
            None
        """
    def start(self):
        """
        Starts the execution of the simulation.

        Parameters:
            None

        Returns:
            None
        """
    def end(self):
        """
        Ends the simulation. In particular, it prints one more snapshot
        and then calls Globals.end() to write parameters to the paramters file.

        Parameters:
            None

        Returns:
            None
        """
    def snapshot(self):
        """
        Takes a snapshot of the current system and writes it to the log file.

        Parameters:
            None

        Returns:
            None
        """


