# Student: Malorie Leonard
# Date: 02/17/2026

"""
Implements a Task in the Simulator.

Classes:
    Task extends SimTask

"""

from Globals import Globals
from Threads import Thread
from Memory import PageTable
from Hardware import CPU
from Interrupts import Interrupt
from Files import File, Directory, OpenFileDescriptor
from SimTasks import SimTask
from SimExceptions import SimException
from Devices import Device

class Task(SimTask):
    """
      Implements a Task in the Simulator.

      Functions:
          Class(Static) Functions:
              initTasks(cls)
              create(cls, nonPreemptive) -> Task
              killTask(cls)

          Instance Functions:
              __init__(self, id, user, nonPreemptive) (Constructor)
              kill(self)
              spawn(self)
              __str__(self) -> string
              getId(self) -> int
              getNonPreemptive(self) -> boolean
              getStatus(self) -> Task Status
              getPriority(self) -> int
              getPageTable(self) -> PageTable
              getUser(self) -> User
              getSwapFile(self) -> OpenfileDescriptor

              The following functions are related to maintaining a list of threas:
                  getNumThreads(self) -> int
                  addThread(self, Thread)
                  removeThread(self, Thread)
                  getThread(self, id) -> Thread
                  getActiveThread(self) -> Thread
                  setActiveThread(self, thread)
                  getThreadList(self) -> list of threads
              The following functions are related to maintaining a list of open files:
                  addOpenFile(self, fileDescriptor)
                  removeOpenFile(self, fileDescriptor)
                  getOpenFileList(self) -> list of OpenFileDescriptors
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
        assert Globals.getMode() == Globals.PrivilegedMode

        SimTask.initTasks()

        Interrupt.registerHandler(Globals.TaskCreate, cls.create)
        Interrupt.registerHandler(Globals.TaskKillInterrupt, cls.killTask)

    def __init__(self, id, user=None, nonPreemptive=False):
        """
        This is the constructor.

        Parameters:
            id: int
                This will be the task id

            user: User
                This is the user that owns the task

            nonPreemptive: boolean (default is False)
                nonPreemptive means that the task is a high priority task and should not
                be preempted from the CPU once it is running.  Such tasks are Operating
                System tasks that need to do important, although very short, work.  All
                User-level tasks may be preemptive.

        Returns:
            None
        """

        assert Globals.getMode() == Globals.PrivilegedMode

        super().__init__(id, user, nonPreemptive)

        self.__status = Globals.TaskNew
        self.__id = id
        self.__user = user
        self.__nonPreemptive = nonPreemptive
        self.__priority = -1 if nonPreemptive else 0
        self.__threadList = []
        self.__nextThreadNum = 0
        self.__openFileList = []
        self.__activeThread = None
        self.__pageTable = PageTable(self)

        swap_size = 2 ** Globals.getNumAddressBits()
        swap_dir = File.getFullPathFile("/swap")
        swap_name = str(self.__id)
        swap_file = swap_dir.getFileEntry(swap_name)

        if swap_file is None:
            swap_file = swap_dir.newFile(swap_name, swap_size)

        self.__swapFile = File.open(swap_file, self)

        self.addOpenFile(self.__swapFile)

    @classmethod
    def create(cls, nonPreemptive=False):
        """
        Creates a new task. This is NOT the constructor.  It is a class or static
        function.  It does, however, call the constructor. This is a system call
        and should only be invoked using a trap.  That is why it is static. Tasks
        should only be created using a trap.

        Parameters:
            nonPreemptive: boolean (default False)
                nonPreemptive means that the task is a high priority task and should not
                be preempted from the CPU once it is running.  Such tasks are Operating
                System tasks that need to do important, although very short, work.  All
                User-level tasks may be preemptive.

        Returns:
            Task
        """

        assert Globals.getMode() == Globals.PrivilegedMode

        if SimTask.getNumTasks() >= Globals.getMaxNumTasks():
            CPU.registers[1] = None
            Globals.setUserMode()
            return None

        user = CPU.registers[6]

        task_id = SimTask.getUniqueTaskId()
        task = cls(task_id, user, nonPreemptive)

        SimTask.registerTask(task)

        task.spawn()
        task._Task__status = Globals.TaskReady

        CPU.registers[1] = task

        Globals.setUserMode()
        return task

    @classmethod
    def killTask(cls):
        """
        Kills a task. It is a class or static function because it is a system call
        and should only be invoked using a trap.  That is why it is static. Tasks
        should only be killed (including normal termination) using a trap.

        Parameters:
            None

        Returns:
            None
        """

        assert Globals.getMode() == Globals.PrivilegedMode

        task = CPU.registers[1]
        if task is not None:
            task.kill()

        CPU.registers[1] = None

        Globals.setUserMode()

    def kill(self):
        """
        Kills the task. This function should not be called direction
        from anywhere except the above killTask() function.

        Parameters:
            None

        Returns:
            None
        """

        assert Globals.getMode() == Globals.PrivilegedMode

        super().kill()

        self.__status = Globals.TaskKill

        for i in range(len(self.__threadList) - 1, -1, -1):
            self.__threadList[i].kill()

        for i in range(len(self.__openFileList) - 1, -1, -1):
            self.__openFileList[i].close()

        self.__pageTable.deallocatePages()

        swap_dir = File.getFullPathFile("/swap")
        swap_dir.rm(str(self.__id))

    def spawn(self):
        """
        Spawns (creates) a new thread.

        Parameters:
            None

        Returns:
            None
        """

        super().spawn()

        if len(self.__threadList) < Globals.getMaxNumThreads():
            new_thread = Thread(self.__nextThreadNum, self, self.__nonPreemptive)
            self.addThread(new_thread)
            self.__nextThreadNum += 1
            Globals.setRescheduleNeeded()

    def __str__(self):
        """
        Returns string representation of a task (suitable for printing).

        Parameters:
            None

        Returns:
            A string representation of a task: string
        """
        return "Task " + str(self.getId()) + "(" + self.getPrettyStatus() + ")"

    def getId(self):
        """
        Gets the id of the task.

        Parameters:
            None

        Returns:
            id: int
        """
        return self.__id

    def getNonPreemptive(self):
        """
        Indicates whether the task is non-preemptive.  Non-preemptive means that it is a critical task
        (e.g. an O/S task or a real-time task) and therefore should not be preempted from the CPU.

        Parameters:
             None

        Returns:
            non-preemptive: boolean
        """
        return self.__nonPreemptive

    def getStatus(self):
        """
        Gets the status of the task.

        Parameters:
            None

        Returns:
            status: int
        """
        return self.__status

    def getPriority(self):
        """
        Gets the priority of the task.

        Parameters:
             None

        Returns:
            priority: int
        """
        return self.__priority

    def getPageTable(self):
        """
        Gets the page table for this task.

        Parameters:
            None

        Returns:
            pageTable: PageTable
        """
        return self.__pageTable

    def getUser(self):
        """
        Gets the user for this task

        Parameters:
            None

        Returns:
            user: User
        """
        return self.__user

    def getSwapFile(self):
        """
        Gets the swap file for this task. Note that this is an OpenFileDescriptor, not a File.
        Therefore, it is already opened and can be read or written to without any other processing.

        Parameters:
            None

        Returns:
            swap file: OpenFileDescriptor
        """
        return self.__swapFile

    def getNumThreads(self):
        """
        Returns the number of threads.

        Parameters:
            None

        Returns:
            Number of threads: int
        """
        return len(self.__threadList)

    def addThread(self, thread):
        """
        Adds a thread to the list of threads.

        Parameters:
            thread: Thread

        Returns:
            None
        """
        self.__threadList.append(thread)

    def removeThread(self, thread):
        """
        Removes a thread from the list of threads.

        Parameters:
             thread: Thread

        Returns:
             None
         """
        if thread is self.__activeThread:
            self.__activeThread = None
        try:
            self.__threadList.remove(thread)
        except Exception:
            pass

    def getThread(self, id):
        """
        Gets a thread (using its id) from the list of threads

        Parameters:
            id: int

        Returns:
            The thread from the list of threads that has a thread id given as a parameter
            or returns None.
        """
        for t in self.__threadList:
            if t.getId() == id:
                return t
        return None

    def getActiveThread(self):
        """
        Returns the active thread for the task. The "active" thread is the thread
        of a task that is the one currently executing.

        Parameters:
            None

        Returns:
            The active thread or None
        """
        return self.__activeThread

    def setActiveThread(self, thread):
        """
        Sets the active thread for the task. The "active" thread is the thread
        of a task that is the one currently executing. If the thread is not in
        the task's list of threads, then it raises a SimException.

        Parameters:
            thread: Thread

        Returns:
            None
        """
        if thread is None:
            self.__activeThread = None
            return

        if thread in self.__threadList:
            self.__activeThread = thread
        else:
            raise SimException(
                "Task.setActiveThread(): thread is not in this task's thread list"
            )

    def getThreadList(self):
        """
        Gets the thread list. (The entire list)

        Parameters:
            None

        Returns:
            The list of threads
        """
        return self.__threadList

    def addOpenFile(self, fileDescriptor):
        """
        Adds an open file descriptor to the list of open files if it is not
        already in the list. A task should not open the same file twice.

        Parameters:
            fileDescriptor: OpenFileDescriptor

        Returns:
            None
        """
        if fileDescriptor not in self.__openFileList:
            self.__openFileList.append(fileDescriptor)

    def removeOpenFile(self, fileDescriptor):
        """
        Removes an open file from the list of open files.

        Parameters:
            None
        Returns:
            None
        """
        try:
            self.__openFileList.remove(fileDescriptor)
        except Exception:
            pass

    def getOpenFileList(self):
        """
        Returns the list of open files (the entire list)

        Parameters:
            None

        Returns:
            list of open files: list
        """
        return self.__openFileList
