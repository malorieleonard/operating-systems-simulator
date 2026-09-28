"""
This module implements some pieces of hardware, specifically the
Bus and the Timer.

Author: Clayton S. Ferner
Date: 7/19/2022

Classes:
    CPU
    Bus
    Timer
"""

from Globals import Globals
from Event import Event
from Interrupts import Interrupt
from SimExceptions import SimException
import math
import random

class CPU:
    """ Implements the CPU, which is just a set of registers.

    Attributes:
        Class (Static) Attibutes:
            registers - This is a list of size Globals.getNumRegisters

    Functions:
        Class (Static) Functions:
            initCPU(cls)
    """
    registers = []
    @classmethod
    def initCPU(cls):
        """
        This is a class method that is called at boot time to initialize any class data.

        Parameters:
            None
        Returns:
            None
        """


class Bus:
    """ Implements Bus in the Simulator that is used to communicate between the CPU (device drivers)
    and the devices.

    Functions:
        Class (Static) Functions:
            initBus(cls)
            out(cls, controllerAddress, frame, data, io_request)
            interrupt(cls)
    """
    @classmethod
    def initBus(cls):
        """
        This is a class method that is called at boot time to initialize any class data.

        Parameters:
            None

        Returns:
            None
        """
    @classmethod
    def out(cls, controllerAddress, frame, data, io_request):
        """
        This will write information to the Bus to communicate with a device controller.
        Each controller is given an address, for which is listens on the bus
        for a message that has its contoller address.  If a message is written on
        the bus that matches a controller's address, that controller picks of
        the data off of the bus and acts upon it.

        Block devices will use the bus to move data in and out of memory using
        the DMA (Direct Memory Access).

        Parameters:
            controllerAddress: int
                Address of the particular controller to communicate with
            frame: Frame
                For block style devices, the frame is where the data should
                be read or written to or from the device
            data: int
                Information for the controller to communicate with it
            io_request: IO_Request
                The controller needs to communcate with the interrupt handler
                when the IO has finished what IO_Request was just been serviced.
        Returns:
            None
        """
    @classmethod
    def interrupt(cls):
        """
        This is how controllers can generate an interrupt() to let the CPU know
        that the device is done with the last I/O Request. There is a special
        line on the bus that signals the CPU. The system will switch to
        privileged mode and run the General Interrup Handler (which takes
        control of the system).

        Parameters:
            None

        Returns:
            None
        """


class Timer:
    """ Implements a Timer use the system clock.

    Functions:
        Class (Static) Functions:
            setTimer(cls, future)
            clearTimer(cls)
    """

    @classmethod
    def setTimer(cls, future):
        """
        This sets a timer to go off in the future (like an alarm clock).
        When the timer goes off, it generates a TimerInterrupt, for which
        the scheduler is the interrupt handler.  This is how round-robin
        scheduling can be done.

        Parameters:
            future: int
                time when the interrupt should happen

        Returns:
            None
        """
    @classmethod
    def clearTimer(cls):
        """
        This clears ALL TimerInterrupt events. That prevents an error
        should multiple timers inadvertently be set.

        Parameters:
            None

        Returns:
            None
        """
