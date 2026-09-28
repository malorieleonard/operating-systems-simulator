"""
This module implements the file system for the Simulator.

Author: Clayton S. Ferner
Date: 7/19/2022

Classes:
    File
    Directory extends File
"""

from Globals import Globals
from SimExceptions import SimException
from Devices import Device
from IO_Request import IO_Request
from FileAllocations import iNode #,FAT
from OpenFileDescriptor import OpenFileDescriptor

class File:
    """ Implements a File.
    Attributes:
        Class (Static) Data:
            RegularFileType
            DirectoryType
            LinkType

    Functions:
        Class (Static) Functions:
            initFiles(cls)
            getMountPoint(cls, pathname) -> Directory
            getFullPathFile(cls, pathname) -> File or Directory
            open(cls, pathname, task) -> OpenFileDescriptor

        Instance Functions:
            __init__(self, pathname, type, device, parentDir, initialSize)
            getType(self) -> RegularFileType or DirectoryType or LinkType (int)
            getFilename(self) -> string
            getDevice(self) -> Device
            getOpenCount(self) -> int
            setDeletePending(self, value)
            getDeletePending(self) -> boolean
            incrementOpenCount(self)
            decrementOpenCount(self)
            getINode(self) -> INode
            getSize(self) -> int
            getParentDir(self) -> Directory
            rename(self, name)
            __str__(self) -> string
            __eq__(self, other) -> boolean
    """

    @classmethod
    def initFiles(cls):
        """
        This is a class method that is called at boot time to initialize any class data.

        Parameters:
            None
        Returns:
            None
        """
    def __init__(self, pathname, type = RegularFileType, device = None, parentDir = None, initialSize = 0):
        """
         This is the constructor.

         Parameters:
             pathname: string
             type: int (default RegularFileType)
             device: Device (default None)
             parentDir: Directory (default None)
             initialSize: int (default zero)

         Returns:
             None
        """
    @classmethod
    def getMountPoint(cls, pathname):
        """
        Gets the mount point of the device on which the pathname is stored.
        Mount points are directories.

        Parameters:
            pathname: string
        Returns:
            Directory
        """
    def getType(self):
        """
        Gets the file type: RegularFileType, DirectoryType, or LinkType

        Parameters:
            None

        Returns:
            type: File type (int)
        """
    def getFilename(self):
        """
        Gets the filename.

        Parameters:
            None

        Returns:
            filename: string
        """
    def getDevice(self):
        """
        Gets the device the file is store on.

        Parameters:
            None

        Returns:
            device: Device
        """
    def getOpenCount(self):
            """
            Gets the number of times this file is currently opened. Although
            each task (and all its threads) should only open a file once, it
            may be opened by multiple tasks.

            Parameters:
                None

            Returns:
                openCount: int
            """
    def setDeletePending(self, value = True):
            """
            Sets the delete-pending status.

            Parameters:
                value: boolean (default True)
            Returns:
                None
            """
    def getDeletePending(self):
            """
            Gets the delete-pending status.

            Parameters:
                None

            Returns:
                deletePending: boolean
            """
    def incrementOpenCount(self):
            """
            Increments the number of opens by one

            Parameters:
                None

            Returns:
                None
            """
    def decrementOpenCount(self):
            """
            Decrements the number of opens by one

            Parameters:
                None

            Returns:
                None
            """
    def getINode(self):
        """
        Gets the INode for the file.

        Parameters:
            None

        Returns:
            inode: INode
        """
    def getSize(self):
        """
        Gets the size of the file in bytes.

        Parameters:
            None

        Returns:
            size: int
        """
    def getParentDir(self):
        """
        Gets the directory this file resides in.

        Parameters:
            None

        Returns:
            parent directory : Directory
        """
    def rename(self, name):
        """
        Renames a file.

        Parameters:
            name: string

        Returns:
            None
        """
    def __str__(self):
        """
        Returns a string representation of a file useful for logging purposes.

        Parameters:
            None
        Returns:
            A string representation of a file: string
        """
        # Feel free to modify this if you don't like the way files are printing.
    def __eq__(self, other):
        """
        Overloads the equals (==) operator. Returns True if self and other
        have the same name.  Note that different files in different directories
        could have the same name.  This should be used with caution.

        Parameters:
            None

        Returns:
            boolean
        """
    @classmethod
    def getFullPathFile(cls, pathname):
        """
        Gets a File object given its full pathname. The File object may be
        a Directory (or mount point), or it may be a regular file.

        Parameters:
            pathname: string

        Returns:
            file: File or Directory
        """
    @classmethod
    def open(cls, pathname, task):
        """
        Opens a file, given the pathname of the file and the task that is
        opening the file. Note that threads open files, but the file
        is owned by the task.  Therefore, threads share open files.

        If the parameter is a File, it opens the file directly.
        If the parameter is a string, this function calls the
        File.getFullPathFile() function to find the file.

        Parameters:
            pathname: string or File
            task: Task

        Returns:
            OpenFileDescriptor
        """

class Directory(File):
    """ Implements a Directory.  Note that Directories are just special files.

    Functions:
        Static Functions (This is NOT a class function):
            normalize(pathname) -> string

        Instance Functions:
            __init__(self, pathname, parent, device)
            getFileEntry(self, filename) -> File
            mkdir(self, pathname)
            newFile(self, name, initialSize) -> File
            rm (self, name)
            rmdir(self, name)
            ls(self, showHidden) -> string
            isEmpty(self) -> boolean
    """
    def __init__(self, pathname, parent, device = None):
        """ This is the constructor. The parent is the parent directory of
         this new directory.  Only the root directory (/) has no parent.

         Parameters:
             pathname: string
             parent: Directory
             device: Device (default None)

         Returns:
             None
        """
    def getFileEntry(self, filename):
        """ Gets a sub file given its name.  The name is NOT a path name.
        This function will only search within the directory for that name.
        If a full path is given, this function will not able to find the file.
        If a full pathname needs to be used, the use the
        File.getFullPathFile().

        Parameters:
            filename: string

        Returns:
            file: File or Directory
        """
    def mkdir(self, pathname):
        """
        Make a new subdirectory within this directory

        Parameters:
            pathname: string

        Returns:
            None
        """
    @staticmethod
    def normalize(pathname):
        """
        Normalizes a pathname.  A normalized pathname will have duplicate
        forward slashes removed as well as the trailing forward slash (except
        in the case where the pathname is only a single forward slash).
        Examples:
            Pathname        Normalized
            "/"          -> "/"
            "/etc//cron.d/anacron"          -> "/etc/cron.d/anacron"
            "//usr///lib////systemd//"      -> "/usr/lib/systemd"

        Parameters:
            pathname: string

        Returns:
            string
        """
    def newFile(self, name, initialSize = 0):
        """ Make a new file that is within this directory. If a file or directory with
        that same name already exists in the directory, the file will not be
        created, and None will be returned.

        Parameters:
            name: string
            initialSize: int (bytes) (default zero)

        Returns:
            File or None
        """
    def rm (self, name):
        """
        Removes or deletes a file that is within this directory if the file is not currently
        opened. If the file is open, it will not be removed.

        Parameters:
            name: string

        Returns:
            None
        """
    def rmdir(self, name):
        """
        Removes a subdirectory from this directory.  The subdirectory needs to
        be empty.  An exception is thrown if the subdirectory is not empty.

        Parameters:
            name: string

        Returns:
            None

        Raises:
            SimException: if the directory is not empty
        """
    def ls(self, showHidden = False):
        """
        Lists the contents of this directory. Hidden files or directories
        are files or directories that begin with a period in their name.
        For example, .bashrc would be considered a hidden file and .private/
        would be a hidden directory. There is nothing special about hidden
        files or directories.  They are the same a non-hidden except that
        their names begin with a period.  This function will not show the
        hidden files (hence hiding them) unless the "showHidden" flag is True.

        Parameters:
            showHidden: boolean (default False)

        Returns:
            string
        """
    def isEmpty(self):
        """
        Returns True if this directory is empty. False otherwise.

        Parameters:
            None

        Returns:
            boolean
        """

