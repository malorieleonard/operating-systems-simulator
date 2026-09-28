# Student: PUT YOUR NAME HERE
# Date: 1/20/2026

"""
This module implements the File Allocations.  At present, only indexed allocation (inode) is implemented.

Author: Clayton S. Ferner
Date: 3/27/2024

Classes:
    iNode(Block)
"""
import math
import random
from Globals import Globals
from SimExceptions import SimException
from Devices import Device,Block

class iNode(Block):
    """
    Implements an iNode.  An iNode is an index block that contains
    all the physical blocks that are used by a file or directory.
    In other words, it provides a mapping from logical block number
    to physical block number.

    Functions:
        Class (Static) Functions:
            None

        Instance Functions:
            __init__(self, device)
            __len__(self) -> int
            getBlock(self, logicalBlock) -> int
            setBlock(self, logicalBlock, physicalBlock) -> int
            allocateBlocks(self, numberOfBytes) -> boolean
            deleteBlocks(self, start = 0, end = None)
    """
    def __init__(self, device):
        """
        This is the constructor.

        Parameters:
            device: Device

        Returns:
            None
        """

    def __len__(self):
        '''
        Overloads the len() operator. Returns the number of blocks used.

        Parameters:
            None

        Returns:
            int
        '''

    def getBlock(self, logicalBlock):
        """
        Gets the physical block given a logical block number.

        Parameters:
            logicalBlock: int

        Returns:
            physicalBlocks: int
        """

    def setBlock(self, logicalBlock, physicalBlock):
        """
        Sets the physical block for a given logical block number.

        Parameters:
            logicalBlock: int
            physicalBlock: int

        Returns:
            None
        """

    def allocateBlocks(self, numberOfBlocks):
        """
        Allocated additional blocks to the file so that the
        file has enough space to hold numberOfBlocks of data.

        Returns True if it is successful.

        Returns False if the number of bytes needed is less
        than zero.

        Raises an Exception if the device doesn't have enough
        free blocks left to make the request.

        Parameters:
            numberOfBytes: int

        Returns:
            boolean

        Raises:
            SimException: if the device does have enough free blocks to perform the allocation
        """

    def deleteBlocks(self, start = 0, end=None):
        """
        Deletes (or frees up) the blocks that have been allocated
        to a file, starting with start and ending with but excluding end. For example,
        if start = 10 and end = 18, then logical block number 10, 11, 12, 13, 14, 15, 16,
        and 17 will be deleted.  These are logical blocks, not physical blocks.  Also note
        that, if no parameter are given, ALL of the blocks will be deallocated.

        Parameters:
            start: int (default 0)
            end: int (default None)

        Returns:
            None
        """

