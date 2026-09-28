"""
This module implements an Event.  An event is something that will happend
in the future.  Because this is a simulation, we have to pretend that
things happen.  That means making events that happen in the future.

Author: Clayton S. Ferner
Date: 7/21/2022

Classes:
    Event
"""


class Event:
    """ An event is for a future event.  It should have a time and type.
        the interupt is optional.

        Functions:
            Instance Functions:
                __init__(self, InterruptType, task, thread, page, device, io_request, user) (Constructor)
                getType(self) -> InterruptType
                getTime(self) -> int
                getTask(self) -> Task
                getThread(self) -> Thread
                getPage(self) -> Page
                getDevice(self) -> Device
                getIORequest(self) -> IORequest
                getUser(self) -> User
                getKey(self) -> int
                __eq__(self, other) -> boolean
                __ne__(self, other) -> boolean
                __str__(self, ) -> string
    """

    def __init__(self, type, time, task = None, thread = None, page = None, device = None,
                 io_request = None, user = None):
        """
        This is the constructor.

        Parameters:
            type: interruptType
            time: int
            task: Task (default None)
            thread: Thread (default None)
            page: Page (default None)
            device: Device (default None)
            io_request: IO_Request (default None)
            user: User (default None)

        Returns:
            None
        """
    def getType(self):
        """
        Gets the event type, which is an Interrupt Type.

        Parameters:
            None

        Returns:
            eventType: int
        """
    def getTime(self):
        """
        Gets the event time.

        Parameters:
            None

        Returns:
            time: int
        """
    def getTask(self):
        """
        Gets the event task.

        Parameters:
            None

        Returns:
            task: Task
        """
    def getThread(self):
        """
        Gets the event thread.

        Parameters:
            None

        Returns:
            thread: Thread
        """
    def getPage(self):
        """
        Gets the event page.

        Parameters:
            None

        Returns:
            page: Page
        """
    def getDevice(self):
        """
        Gets the event device.

        Parameters:
            None

        Returns:
            device: Device
        """
    def getIORequest(self):
        """
        Gets the event IO Request.

        Parameters:
            None

        Returns:
            io_request: IORequest
        """
    def getUser(self):
        """
        Gets the event user.

        Parameters:
            None

        Returns:
            user: User
        """
    def getKey(self):
        """
        Returns the event's time so that the Priority Queue can
        order the queue by time.

        Parameters:
            None

        Returns:
            time: int
        """
    def __eq__(self, other):
        """
        Determines if two events are equal, based upon their type.
        This function is designed to be able to remove all events
        of a particular type.  So events of the same type are equal.

        Parameters:
            self: Event
            other: Event

        Returns:
            boolean
        """
    def __ne__(self, other):
        """
        Determines if two events are not equal, based upon their type.

        Parameters:
            self: Event
            other: Event

        Returns:
            boolean
        """
    def __str__(self):
        """
        Returns string representation of an event

        Parameters:
            None
        Returns:
            A string representation of an event: string
        """
