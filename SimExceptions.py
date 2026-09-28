"""
This is the SimException class. Its purpose is to be a generic exception
type for exceptions in the simulator. It adds a little extra features that
are useful for the Simulator.

Author: Clayton S. Ferner
Date: 7/19/2022

Classes:
    SimException extends Exception

"""

class SimException(Exception):
    ''' Exceptions used in the simulator.
    Functions:
        Class (Static) Functions:
            none

        Instance Functions:
            __init__(int, message, intro, theClass) (Constructor)
            getIntro(self) -> string
            getMessage(self) -> string
            getTheClass(self) -> Python class
    '''
    def __init__(self, message, intro = None, theClass = None):
        """
        This is the constructor.

        Parameters:
            message: string
            intro: string (default None)
            theClass: Class (default None)

        Returns:
            None

        The message (or error message) is a description of the exception. The class is used to run
        the snapshot of the relevant class. For example, if there is an exception related to CPU
        schedule, then printing the snapshot of the Thread class would be useful, in which case the
        Thread class should be provided as the class. The into is a message to put in front of
        the snapshot to indicate what is being printed. Both the class and the intro are optional.
        """
    def getIntro(self):
        """
        Gets the Intro message.

        Parameters:
            None

        Returns:
            intro: string
        """
    def getMessage(self):
        """
        Gets the error message.

        Parameters:
            None

        Returns:
            error message: string
        """
    def getTheClass(self):
        """
        Gets the relevant class, so that the snapshot can be run.

        Parameters:
            None

        Returns:
            relevant class: any class
        """

