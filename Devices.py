"""
This module implements the Devices, including disks, block devices, and character devices.

Author: Clayton S. Ferner
Date: 7/19/2022

Classes:
    Block
    Device
    BlockDevice(Device)
    CharacterDevice(Device)
"""

from Globals import Globals
from MyQueue import FIFOQueue,QueueIterator
from Interrupts import Interrupt
from Hardware import CPU,Bus
from SimExceptions import SimException

class Block:
    ''' This class implements a Block of data for a block-type device (including Disks).
    It has no functionality.  It is simply for data. '''
    def __init__(self, device, data = None, nextBlock = None):
        """ This is the constructor. The nextBlock is so that they can be changed together, such as for a
        Linked file system.

        Parameters:
            data: any type
            nextBlock: a Block
        Returns:
            None
        """
    def getDevice(self):
        """
        Gets the device.

        Parameters:
            None

        Returns:
            device: block device
        """
    def getData(self):
        """
        Gets the data.

        Parameters:
            None

        Returns:
            data: any type
        """
    def getNextBlock(self):
        """
        Gets the next Block.

        Parameters:
            None

        Returns:
            next block: Block
        """
    def setData(self, data):
        """
        Sets the data

        Parameters:
            data: any type

        Returns:
            none
        """
    def setNextBlock(self, nextBlock):
        """
        Sets the next block

        Parameters:
            next block: Block

        Returns:
            none
        """

class Device:
    """ Implements a generic Device in the Simulator.

    Functions:
        Class (Static) Functions:
            initDevices(cls)
            deviceInterruptHandler(cls)
            getDeviceById(cls, id) -> Device
            getDeviceByName(cls, name) -> Device
            snapshot(cls) -> string
            getSummary(cls) -> string

        Instance Functions:
            __init__(self, id, name, controllerAddress)
            getId(self) -> int
            getName(self) -> string
            getControllerAddress(self) -> int
            enqueue(self, io_request)
            dequeue(self) -> IO_Request
            remove(self, io_request)
            getQueue(self) -> FIFOQueue or SortedQueue
            __str__(self) -> string
    """

    def __init__(self, id, name, controllerAddress = None):
        """
         This is the constructor.

         Parameters:
             id: int
             name: string
             controllerAddress: int (default None)

         Returns:
             None
        """
    @classmethod
    def initDevices(cls):
        """
        This is a class method that is called at boot time to initialize any class data.

        Parameters:
            None
        Returns:
            None
        """
    @classmethod
    def deviceInterruptHandler(cls):
        """
        The interrupt handler for generic devices.

        Parameters:
            None
        Returns:
            None
        """
    @classmethod
    def getDeviceById(cls, id):
        """
        Gets a device using the id.

        Parameters:
            id: int
        Returns:
            Device
        """
    @classmethod
    def getDeviceByName(cls, name):
        """
        Gets a device using the Name.

        Parameters:
            name: string
        Returns:
            Device
        """
    def getId(self):
        """
        Gets the id of a device.

        Parameters:
            None

        Returns:
            id: int
        """
    def getName(self):
        """
        Gets the name of a device.

        Parameters:
            None

        Returns:
            name: string
        """
    def getControllerAddress(self):
        """
        Gets the controller address of a device.

        Parameters:
            None

        Returns:
            controllerAddress: int
        """
    def enqueue(self, io_request):
        """
        Enqueues an IO_Request.

        Parameters:
            io_request: IO_Request

        Returns:
            None
        """
    def dequeue(self):
        """
        Removes and returns the next IO_Request.

        Parameters:
            None

        Returns:
            io_request: IO_Request
        """
    def remove(self, io_request):
        """
        Removes an IO_Request from the queue

        Parameters:
            io_request: IO_Request

        Returns:
            None
        """
    def getQueue(self):
        """
        Gets the queue of IO_Requests.

        Parameters:
            None

        Returns:
            ioQueue: FIFOQueue or SortedQueue
        """
    def __str__(self):
        """
        Returns a string representation of a device useful for logging purposes.

        Parameters:
            None
        Returns:
            A string representation of a device: string
        """
        # Feel free to modify this if you don't like the way devices are printing.

        return "Device " + str(self.__id) + " " + self.__name, + " " + str(self.getControllerAddress())
    @classmethod
    def snapshot(cls):
        """
        Takes a snapshot of the current state of the devices and returns it as a string.

        Parameters:
            None

        Returns:
            string
        """
        result = "\n\n\n\t\t\tDevice Table:\n"
        result += "  \t      \tController\t    \tNum Free\t                \n"
        result += "Id\t Name \tAddress   \tBusy\t Blocks \tIO Request Queue\n"
        result += "-" * 70 + "\n"

        for device in cls.__Devices:
            result += str(device.getId()) + "\t"
            result += str(device.getName()) + "\t"
            result += str(device.getControllerAddress()) + "      \t"

            if device.isBusy(): result += "Busy" + "\t"
            else: result += "Idle" + "\t"

            result += str(format(device.getNumFreeBlocks(), "8d")) + "\t"

            result += str(device.getQueue()) + "\n"
        result += "-" * 70 + "\n"

        # result += "Free (.) / Occupied (X) blocks:\n"
        # for device in cls.__Devices:
        #     if type(device) is BlockDevice:
        #         result += str(device.getName()) + ":\t"
        #         for block in range(device.getTotalNumBlocks()):
        #             if device.isBlockFree(block):
        #                 result += "."
        #             else:
        #                 result += "X"
        #         result += "\n"
        result += "-" * 70 + "\n\n\n"

        return result
    @classmethod
    def getSummary(cls):
        """
        This provides a summary of the device performance.

        Parameters:
            None

        Returns:
            Summary: string
        """

        result = "\n\n\n"
        result += """\t\t\tSummary of Devices:

The Turnaround time is the time from origination to completion.
The Service time is the time for the device to process the IO.
"""

        result += "        \t           \t             \t            \t           \t   Total\n"
        result += "        \t  Number of\t  Number of  \t   Average  \t  Average  \t  R/W Head\n"
        result += "        \t  Completed\t Incompleted \t Turnaround \t  Service  \t  Movement\n"
        result += "Device  \t      IOs  \t      IOs    \t     Time   \t    Time   \t(Cylinders)\n"
        result += "-" * 95
        result += "\n"
        for i in range(Globals.getNumDevices()):
            ioQueue = cls.__Devices[i].getQueue()
            result += format(cls.__Devices[i].getName(), "8s") + "\t"
            result += format(cls.__ioTurnCounts[i], "9d") + "\t"
            result += format(len(ioQueue), "11d") + "\t  "
            if cls.__ioTurnCounts[i] != 0:
                result += format(cls.__ioTurnSums[i] / cls.__ioTurnCounts[i], "10.2f") + "\t  "
            else:
                result += format("- ", ">10s") + "\t  "
            if cls.__ioServiceCounts[i] != 0:
                result += format(cls.__ioServiceSums[i] / cls.__ioServiceCounts[i], "10.2f") + "\t"
            else:
                result += format("- ", ">10s") + "\t"

            # Because the Disk class is separate and a subclass, I can't just check to see if
            # it is the type
            if type(cls.__Devices[i]) is not BlockDevice and type(cls.__Devices[i]) is not CharacterDevice :
                result += format(cls.__totalTrackMovement[i], "8d")
            else:
                result += format("N/A", ">8s") + "\t"
            result += "\n"

        return result

class BlockDevice(Device):
    """ Implements a Block Device in the Simulator. A block device is a device
        that reads and writes an entire block at a time.  A block is the same
        size as a page or frame. Solid-state devices, such as thumb drives,
        are block devices as well as disks.  Disks have their own sub-class
        because of the need to map from blocks to surface/track/sector.

    Functions:
        Class (Static) Functions:
            initBlockDevices(cls)
            blockDeviceInterruptHandler(cls)

        Instance Functions:
            __init__(self, id, name, controlleraddress, numBlocks)
            getControllerAddress(self) -> int
            getTotalSpace(self) -> int
            getTotalNumBlocks(self) -> int
            isBusy(self) -> boolean
            isBlockFree(self, i) -> boolean
            setBlockUsed(self, i)
            setBlockFree(self, i):
            getNumFreeBlocks(self) -> int
            enqueue(self, io_request)
            dequeue(self) -> IO_Request
            getQueue(self) -> FIFOQueue or SortedQueue
            __str__(self) -> string
    """
    @classmethod
    def initBlockDevices(cls):
        """
        This is a class method that is called at boot time to initialize any class data.

        Parameters:
            None
        Returns:
            None
        """
    def __init__(self, id, name, controlleraddress, numBlocks):
        """
         This is the constructor.

         Parameters:
             id: int
             name: string
             controllerAddress: int
             numBlocks: int

         Returns:
             None
        """
    @classmethod
    def blockDeviceInterruptHandler(cls):
        """
        The interrupt handler for block devices that are NOT disks.
        Disk interrupts are handled by the diskInterruptHandler.

        Parameters:
            None
        Returns:
            None
        """
    def getControllerAddress(self):
        """
        Gets the controller address of a device.

        Parameters:
            None

        Returns:
            controllerAddress: int
        """
    def getTotalSpace(self):
        """
        Gets the total amount of storage space this device provides in bytes.

        Parameters:
            None

        Returns:
            total space in bytes: int
        """
    def getTotalNumBlocks(self):
        """
        Gets the total number of blocks this device provides.

        Parameters:
            None

        Returns:
            total number of blocks: int
        """
    def isBusy(self):
        """
        Indicates whether the device is currently busy with an IO request.

        Parameters:
            None

        Returns:
            busy: boolean
        """
    def isBlockFree(self, i):
        """
        Determines if a particular block is free to be used.

        Parameters:
            block number: int

        Returns:
            boolean
        """
    def setBlockUsed(self, i):
        """
        Sets a particular block to used (not free).

        Parameters:
            block number: int

        Returns:
            None
        """
    def setBlockFree(self, i):
        """
        Sets a particular block to free (unused).

        Parameters:
            block number: int

        Returns:
            None
        """
    def getNumFreeBlocks(self):
        """
        Gets the number of free blocks.

        Parameters:
            None

        Returns:
            number of free blocks: int
        """
    def enqueue(self, io_request):
        """
        Enqueues an IO_Request.

        Parameters:
            io_request: IO_Request

        Returns:
            None
        """
    def dequeue(self):
        """
        Removes and returns the next IO_Request.

        Parameters:
            None

        Returns:
            io_request: IO_Request
        """
    def getQueue(self):
        """
        Gets the queue of IO_Requests.

        Parameters:
            None

        Returns:
            controllerAddress: queue
        """
    def __str__(self):
        """
        Returns a string representation of a block device useful for logging purposes.

        Parameters:
            None
        Returns:
            A string representation of a block device: string
        """
        # Feel free to modify this if you don't like the way devices are printing.

        return "Block Device " + str(self.getId()) + " " + self.getName() + " " + str(self.getControllerAddress())

class CharacterDevice(Device):
    """
    This class has not yet been implemented.
    """
    @classmethod
    def charcterDeviceInterruptHandler(cls):
        pass
