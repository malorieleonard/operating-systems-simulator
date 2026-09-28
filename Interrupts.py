"""
This is the interrupt system.

Author: Clayton S. Ferner
Date: 7/19/2022

Classes:
    Interrupt

"""

from Globals import Globals
from SimExceptions import SimException


class Interrupt:
    """ This is the interrupt system.
    NOTE THAT DATA NEEDS TO BE PASSED TO AN INTERRUPT HANDLER OR SYSTEM CALL VIA REGISTERS.
    There are specific registers that should be used for different types of data that may
    need to be passed to the handlers.  Those registers are:
        Data            Register #
        -------------------------
        Interrupt Type      0
        Task                1
        Thread              2
        Page                3
        Device              4
        IORequest           5
        User                6
        Frame               7

    Functions:
        Class (Static) Functions:
            getInterruptNames(cls) -> list of strings
            getInterruptName(cls, type) -> string
            getInterruptTypes(cls) -> list of InterruptTypes (ints)
            registerHandler(cls, interruptType, handler)
            GIH(cls, interruptType)
            trap(cls, interruptType)
            snapshot(cls) -> string
            interruptTable2String(cls) -> string

        Instance Functions:
            __init__(self, interruptType, Task, Thread, Page, Device, IO_Request, User)
            getType(self) -> interruptType
            getTask(self) -> Task
            getUser(self) -> User
            getThread(self) -> Thread
            getPage(self) -> Page
            getDevice() -> Device
            getIO_Request(self) -> IO_Request
            __str__(self) -> string
            trap(self)

    """

    @classmethod
    def getInterruptNames(cls):
        """
        Gets the list of interrupt names

        Parameters:
            None

        Returns:
            InterruptNames: list of strings
        """
    @classmethod
    def getInterruptName(cls, type):
        """
        Returns the name (string) of an interrupt type

        Parameters:
            type: (int): Interrupt type (which are defined in Globals)

        Returns:
            A string representation of the interrupt type name
        """
    @classmethod
    def getInterruptTypes(cls):
        """
        Gets the list of interrupt types

        Parameters:
            None

        Returns:
            InterruptTypes: list of ints
        """
    @classmethod
    def registerHandler(cls, interruptType, handler):
        """
        Registers an interrupt handler.  An interrupt handler is a function.
        To pass a function as a parameter, you just give the function name
        WITHOUT THE PARENTHESES.  For example, to register the pageFaultHandler()
        as the handler for the PageFault Interrupt, you would do
            Interrupt.registerHandler(Globals.PageFault, MMU.pageFaultHandler)
        If you add parentheses after the pageFaultHandler, then Python will
        CALL the function first, and then pass the result as an argument, instead
        of passing the function as a parameter.

        Parameters:
            interruptType: int
                This is the interrupt type
            handler: function
                The function that handles the interrupt

        Returns:
            None
        """
    @classmethod
    def GIH(cls, interruptType):
        """
        This is the General Interrupt Handler.  What it does is call the appropriate
        interrupt handler based upon the interrupt type. The appropriate interrupt
        handler must be a function that was previously registered.

        Parameters:
            interruptType: int

        Returns:
            None
        """
    @classmethod
    def trap(cls, interruptType):
        """
        This generates a software interrupt.  Although it could be used to generate any type
        of interrupt, it is specifically intended for software to make a call to a system call.

        Parameters:
            interruptType: int

        Returns:
            None
        """
    @classmethod
    def snapshot(cls):
        """ Returns a snapshot of the interrupts.  Basically, it just the result of
         the interruptTable2String()

        Parameters:
            None

        Returns:
            string
        """
    @classmethod
    def interruptTable2String(cls):
        """ Returns a string (suitable for printing) containing the interrupt table.

        Parameters:
            None

        Returns:
            string
        """
