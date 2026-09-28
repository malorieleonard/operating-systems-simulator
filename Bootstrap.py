'''
Starts the Simulator.  This is the module that has the main() function.
Author: Clayton S. Ferner
Date: 4/21/2022
'''

import sys
import traceback
from Simulator import Simulator
from Globals import Globals
from SimExceptions import SimException

def main(argv):
    """
    Starts the Simulator.  This is the main() function.
    This usage is:  python Bootstrap.py [--help] [-s] -parameters <parameter file>
    Parameters:
        --help (optional) - prints the usage and quits
        -s (optional)     - uses the same random number seed as the last time it was run
                            so that the sequence of events will be the same.  This is
                            very helpful for debugging, when you want the same things to
                            happen until you figure out the problem. Without the -s,
                            different things will happen.
        -d (optional)     - Echos log messages to the console
        -debug (optional) - Runs tests on student module only (Automatically turns on -d)
        -parameters <parameter file>
                      - This is the parameters for the simulation, provided by your
                        instructor.

    Returns:
        None
    """
    newSeed = True
    echoToConsole = False
    paramFile = None
    # testThreads = False
    # testMemory = False
    # testDisks = False
    usage = '''Usage: python Bootstrap.py [--help] [-d] [-s] -parameters <parameter file>
-d Echo log messages to the console
-s Use the same random number seed as last exectuion
'''

    if len(argv) <= 1:
        raise Exception("parameter file not provided\n" + usage)

    for i in range(1,len(argv)):
        if argv[i] == "-s":
            newSeed = False
        elif argv[i] == "-d":
            echoToConsole = True
        elif argv[i] == "-debug":
            # testThreads = False
            # testMemory = False
            testDisks = True
            echoToConsole = True
        elif argv[i] == "--help" or argv[i] == "-help":
            print(usage)
            return
        elif argv[i] == "-parameters":
            try:
                paramFile = argv[i+1]
            except:
                raise Exception("parameter file not provided\n" + usage)

    if paramFile is None:
        raise Exception("parameter file not provided\n" + usage)

    try:
        simulator = Simulator(newSeed, paramFile, echoToConsole)
        # if testThreads:
        #     simulator.testThreads()
        # elif testMemory:
        #     simulator.setup()
        #     simulator.testMemory()
        # elif testDisks:
        #     simulator.setup()
        #     simulator.testDisks()
        # else:
        simulator.setup()
        simulator.start()

    except SimException as e:
        theClass = e.getTheClass()
        intro = e.getIntro()
        # Globals.logMessage("Exception at Simulation time: " + str(Globals.getTime()))
        Globals.logMessage(traceback.format_exc())
        if intro is not None:
            Globals.logMessage(intro)
        if theClass is not None:
            Globals.logMessage(theClass.snapshot())
        else:
            simulator.snapshot()
        Globals.end()
        raise(e)






if __name__ == "__main__":
    main(sys.argv)
