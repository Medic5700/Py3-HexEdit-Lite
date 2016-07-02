#!/usr/bin/env python3
'''A program to help test the various modules of Py3HexEditLite.py, in addition to help develop it'''
import sys

env = None
try:
    import tty #linux specific operations
    import termios #linux specific operations
    env = "UNIX"
except:
    pass
try:
    import msvcrt #windows specific operations
    env = "WIN"
except:
    pass

def getch():
    if (env == "WIN"):
        return msvcrt.getch()
    if (env == "UNIX"):
        terminalFD = sys.stdin.fileno()
        oldSetting = termios.tcgetattr(terminalFD)
        #try
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        #finally
        termios.tcsetattr(terminalFD, termios.TCSADRAIN, oldSetting)
        return ch

if __name__ == "__main__":
    #To help figure out the keymappings to Windows and Linux
    if (False):
        print("input 20 characters")
        i = 20
        while(i>0):
            i -= 1
            temp = getch()
            print(str(temp))
            print(":" + str(ord(temp)))
            print(str(hex(ord(temp))))
        
    #unit tests of the various modules in Py3HexEditLite.py
    if (True):
        try:
            import Py3HexEditLite as py3
        except:
            print("could not import Py3HexEditLite.py")
            print("aborting unit tests")
            exit()
        
        #create test file
        fd = open("test.tmp","wb")
        for i in range(0,256):
            for j in range(0,256):
                fd.write(j.to_bytes(1, sys.byteorder))
        fd.close()
