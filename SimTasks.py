"""
This is the super class of the Thread class used by the Simulator.
Author: Clayton S. Ferner
Date: 7/19/2022


Classes:
    SimTask


"""
import random
from Globals import Globals
from SimThreads import SimThread
from SimExceptions import SimException
from Files import File,Directory,OpenFileDescriptor

class SimTask:
    """
    This is the super class of the Thread class used by the Simulator.

    Functions:
        Class (Static) Functions:
            initTask(cls)
            getUniqueTaskId(cls) -> int
            registerTask(cls, Task)
            getTaskById(cls, id) -> Task
            getNumTasks(cls) -> int
            taskTable2String(cls) -> string
            taskPageTable2String(cls) -> string
            openFilesTable2String(cls) -> string
            snapshot(cls) -> string
            getSummary(cls) -> string

        Instance Functions:
            __init__(self, id, user, nonPreemptive)
            kill(self)
            spawn(self)
            getPrettyStatus(self) -> string
    """

    @classmethod
    def initTasks(cls):
        """
        This is a class method that is called at boot time to initialize any class data.

        Parameters:
            None

        Returns:
            None
        """
    def __init__(self, id, user = None, nonPreemptive = False):
        """
        This is the constructor.

        Parameters:
            id: int
            user: string (default is None)
            nonPreemptive: boolean (default is False)

        Returns:
            None
        """
    @classmethod
    def getUniqueTaskId(cls):
        """
        Gets a unique task Id.  All tasks must have unique ids, so it is imperative
        to have a global function that can ensure each id is unique.  The ids may
        be reused if a task is killed or terminated.

        Parameters:
            None

        Returns:
            id: int
        """
    @classmethod
    def registerTask(cls, task):
        """
        Registers a new task with its id.  It is assumed that the getUniqueTaskId() was
        used to ensure that this new task has a unique id. If tasks are not registered,
        the there is no guarantee that getUniqueTaskId() will be able to provide a unique id.

        Parameters:
            task: Task

        Returns:
            None
        """
    def kill(self):
        """
        This doesn't do anything. It is up to the kill() in the Task class to do
        the actual killing. This function is meant to record that the task should be
        killed so that some error checking can be done.

        Parameters:
            None

        Returns:
            None
        """
    def spawn(self):
        """
        This doesn't do anything. It is up to the spawn() in the Task class to do
        the actual spawning. This function is meant to record that a new thread should
        be spawned so that some error checking can be done.

        Parameters:
            None

        Returns:
            None
        """
    @classmethod
    def getTaskById(cls, id):
        """
        Gets a task with the id, if it exists

        Parameters:
            id: int

        Returns:
            task or None
        """
    @classmethod
    def getNumTasks(cls):
        """
        Gets the total number of tasks that currently exist in the system. This is not
        the same as the maximum number of tasks allowed.

        Parameters:
            None

        Returns:
            number of tasks: int
        """
    def getPrettyStatus(self):
        """
        Returns an English version of the status.  For example, instead of getting numbers
        711, 712, and 713, it will return "TaskNew", "TaskReady", and "TaskKill", respectively.
        The function should not be used for any purpose other than printing or displaying the
        status.

        Parameters:
            None

        Returns:
            status: string
        """
    @classmethod
    def taskTable2String(cls):
        """
        Creates a Task Table and returns it as a string (suitable for printing).
        The table includes the task ids, their statuses, the active thread, the
        swap file, and the list of threads.

        Parameters:
            None

        Returns:
            string
        """
    @classmethod
    def taskPageTable2String(cls):
        """
        Creates Page Tables for each task and returns it as a string (suitable for printing).

        Parameters:
            None

        Returns:
            string
        """
    @classmethod
    def openFilesTable2String(cls):
        """
        Creates a table of the open files for each task and returns it as a string (suitable for printing).

        Parameters:
            None

        Returns:
            string
        """
    @classmethod
    def snapshot(cls):
        """
        Takes a snapshot of the current state of the tasks (specifically, the task table) and
        returns it as a string (suitable for printing).

        Parameters:
            None

        Returns:
            string
        """
    @classmethod
    def getSummary(cls):
        """
        This provides a summary of the tasks.

        Parameters:
            None

        Returns:
            Summary: string
        """

