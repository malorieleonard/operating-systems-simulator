# Student: Malorie Leonard
# Date: 04/28/2026

"""
This module implements the Devices, including disks, block devices, and character devices.


Classes:
    Disk(BlockDevice)
"""

from Globals import Globals
from MyQueue import FIFOQueue,SortedQueue
from Devices import Device,BlockDevice
from Interrupts import Interrupt
from Hardware import CPU,Bus
from SimExceptions import SimException

class Disk(BlockDevice):
    """ Implements a Disk Device in the Simulator. Disks are block devices,
    but they also have surface/track/sector, which makes then different
    the other block devices, such as solid-state.

    Functions:
        Class (Static) Functions:
            initDisks(cls)
            diskInterruptHandler(cls, interrupt)

        Instance Functions:
            __init__(self, id, name, controllerAddress,
                 surfaces, tracksPerSurface, sectorsPerTrack,
                 bytesPerSector)
            block2Surface(self, blockNum) -> int
            block2Cylinder(self, blockNum) -> int
            block2Sector(self, blockNum) -> int
            block2SurfaceCylinderSector(self, blockNum) -> int
            getControllerAddress(self) -> int
            getTotalSpace(self) -> int
            getTotalNumBlocks(self) -> int
            isBusy(self) -> boolean
            isBlockFree(self, i) -> boolean
            setBlockUsed(self, i)
            setBlockFree(self, i)
            getNumFreeBlocks(self) -> int
            enqueue(self, io_request)
            dequeue(self) -> IO_Request
            getQueue(self) -> FIFOQueue or SortedQueue
            __str__(self) -> string
    """

    @classmethod
    def initDisks(cls):
        """
        This is a class method that is called at boot time to initialize any class data.

        Parameters:
            None
        Returns:
            None
        """
        assert Globals.getMode() == Globals.PrivilegedMode
        Interrupt.registerHandler(Globals.DiskInterrupt, cls.diskInterruptHandler)

    def __init__(self, id, name, controllerAddress,
                 surfaces, tracksPerSurface, sectorsPerTrack,
                 bytesPerSector):
        '''
        Create a new disk with id, name, bus address of the controller,
        number of surfaces, number of tracks per surface, number of sectors per track,
        and number of bytes per sector
        Parameters:
            id: int
            name: string
            controllerAddress: int
            surfaces: int
            tracksPerSurface: int
            sectorsPerTrack: int
            bytesPerSector: int

        Returns:
            None
        '''
        self.__controllerAddress = controllerAddress
        self.__blockSize = Globals.getPageSize()

        self.__surfaces = surfaces
        self.__tracksPerSurface = tracksPerSurface
        self.__sectorsPerTrack = sectorsPerTrack
        self.__bytesPerSector = bytesPerSector

        self.__totalSpace = surfaces * tracksPerSurface * sectorsPerTrack * bytesPerSector
        self.__totalNumBlocks = self.__totalSpace // self.__blockSize

        super().__init__(id, name, controllerAddress, self.__totalNumBlocks)

        self.__busy = False

        self.__sectorsPerBlock = self.__blockSize // self.__bytesPerSector
        self.__blocksPerTrack = self.__sectorsPerTrack // self.__sectorsPerBlock
        self.__blocksPerCylinder = self.__blocksPerTrack * self.__surfaces

        self.__freeBlocks = []
        for i in range(self.__totalNumBlocks):
            self.__freeBlocks.append(True)

        self.__numFreeBlocks = self.__totalNumBlocks

        self.__queue = SortedQueue()
        self.__iterator = self.__queue.newIterator()

        # 1 means the SCAN head is moving toward larger cylinder numbers.
        # -1 means it is moving toward smaller cylinder numbers.
        self.__direction = 1

    @classmethod
    def diskInterruptHandler(cls):
        """
        The interrupt handler for disks.

        Parameters:
            None
        Returns:
            None
        """
        assert Globals.getMode() == Globals.PrivilegedMode

        io_request = CPU.registers[5]

        if io_request is not None:
            disk = io_request.getDevice()
            task = io_request.getTask()
            thread = io_request.getThread()
            page = io_request.getPage()
            frame = io_request.getFrame()
            openFileDescriptor = io_request.getfd()

            openFileDescriptor.decrementIOCount()

            if task is not None and page is not None:
                task.getPageTable().unLockPage(page)

            if openFileDescriptor.getNumIOs() == 0 and openFileDescriptor.closePending():
                openFileDescriptor.close()

            if thread is not None and thread.getStatus() != Globals.ThreadKill:
                thread.wake(frame)

        else:
            disk = CPU.registers[4]

        disk.__busy = False

        nextRequest = disk.dequeue()

        if nextRequest is not None:
            data = disk.block2SurfaceCylinderSector(nextRequest.getBlockNum())

            disk.__busy = True

            Bus.out(
                disk.getControllerAddress(),
                nextRequest.getFrame(),
                data,
                nextRequest
            )

        Globals.setUserMode()

    def block2Surface(self, blockNum):
        """
        Gets the disk surface that a particular block maps to.

        Parameters:
            blockNum: int

        Returns:
            surface number: int
        """
        blockInCylinder = blockNum % self.__blocksPerCylinder
        return blockInCylinder // self.__blocksPerTrack

    def block2Cylinder(self, blockNum):
        """
        Gets the disk cylinder number that a particular block maps to.

        Parameters:
            blockNum: int

        Returns:
            cylinder number: int
        """
        return blockNum // self.__blocksPerCylinder

    def block2Sector(self, blockNum):
        """
        Gets the disk sector number that a particular block maps to.

        Parameters:
            blockNum: int

        Returns:
            sector number: int
        """
        blockInTrack = blockNum % self.__blocksPerTrack
        return blockInTrack * self.__sectorsPerBlock

    def block2SurfaceCylinderSector(self, blockNum):
        """
        Maps a particular block to a surface/cylinder/sector combination, which
        is what needs to be written to the bus for the disk controller to read.
        The returned value will be a 3 byte sequence.  The highest order byte
        will be the track.  The middle byte will be the surface.  The lowest
        order byte will be the sector.  For example, if we have surface 3 track 510
        and sector 4, then the data will be 33424132 = 00000001111111100000001100000100
        0000000111111110 00000011 00000100
                510          3        4

        Parameters:
            blockNum: int

        Returns:
            cylinder/surface/sector : int
        """
        cylinder = self.block2Cylinder(blockNum)
        surface = self.block2Surface(blockNum)
        sector = self.block2Sector(blockNum)

        return (cylinder << 16) | (surface << 8) | sector

    def enqueue(self, io_request):
        """
        Enqueues an IO_Request.

        Parameters:
            io_request: IO_Request

        Returns:
            None
        """
        super().enqueue(io_request)

        blockNum = io_request.getBlockNum()
        io_request.setCylinder(self.block2Cylinder(blockNum))

        self.__queue.enqueue(io_request)

        if not self.isBusy():
            CPU.registers[5] = None
            CPU.registers[4] = self
            Interrupt.trap(Globals.DiskInterrupt)

    def dequeue(self):
        """
        Removes and returns the next IO_Request.

        Parameters:
            None

        Returns:
            io_request: IO_Request
        """
        if self.__queue.isEmpty():
            return None

        if self.__iterator.isPastEnd():
            self.__iterator.setCurrentFront()
            return self.__iterator.getCurrentValue()

        currentRequest = self.__iterator.getCurrentValue()

        if currentRequest is not None:
            super().remove(currentRequest)

        if self.__direction > 0:
            self.__iterator.removeCurrentAndAdvance()

            if self.__iterator.isPastEnd():
                self.__direction = -1
                self.__iterator.setCurrentBack()
        else:
            self.__iterator.removeCurrentAndRetreat()

            if self.__iterator.isPastEnd():
                self.__direction = 1
                self.__iterator.setCurrentFront()

        return self.__iterator.getCurrentValue()

    def getControllerAddress(self):
        """
        Gets the controller address of a device.

        Parameters:
            None

        Returns:
            controllerAddress: int
        """
        return self.__controllerAddress

    def getTotalSpace(self):
        """
        Gets the total amount of storage space this device provides in bytes.

        Parameters:
            None

        Returns:
            total space in bytes: int
        """
        return self.__totalSpace

    def getTotalNumBlocks(self):
        """
        Gets the total number of blocks this device provides.

        Parameters:
            None

        Returns:
            total number of blocks: int
        """
        return self.__totalNumBlocks

    def isBusy(self):
        """
        Indicates whether the device is currently busy with an IO request.

        Parameters:
            None

        Returns:
            busy: boolean
        """
        return self.__busy

    def isBlockFree(self, i):
        """
        Determines if a particular block is free.

        Parameters:
            block number: int

        Returns:
            boolean
        """
        if i < 0 or i >= self.__totalNumBlocks:
            return False

        return self.__freeBlocks[i]

    def setBlockUsed(self, i):
        """
        Sets a particular block to used (not free).

        Parameters:
            block number: int

        Returns:
            None
        """
        if i < 0 or i >= self.__totalNumBlocks:
            raise SimException("Disk: setBlockUsed(): block number out of range")

        if self.__freeBlocks[i]:
            self.__freeBlocks[i] = False
            self.__numFreeBlocks -= 1

    def setBlockFree(self, i):
        """
        Sets a particular block to free (unused).

        Parameters:
            block number: int

        Returns:
            None
        """
        if i < 0 or i >= self.__totalNumBlocks:
            raise SimException("Disk: setBlockFree(): block number out of range")

        if not self.__freeBlocks[i]:
            self.__freeBlocks[i] = True
            self.__numFreeBlocks += 1

    def getNumFreeBlocks(self):
        """
        Gets the number of free blocks.

        Parameters:
            None

        Returns:
            number of free blocks: int
        """
        return self.__numFreeBlocks

    def getQueue(self):
        """
        Gets the queue of IO_Requests.

        Parameters:
            None

        Returns:
            queue: FIFOQueue or SortedQueue
        """
        return self.__queue

    def __str__(self):
        """
        Returns a string representation of a disk useful for logging purposes.

        Parameters:
            None:
        Returns:
            A string representation of a disk: string
        """
        # Feel free to modify this if you don't like the way disks are printing.
        return self.getName() + " "