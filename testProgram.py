#!/usr/bin/env python3
'''A program to help test the various modules of Py3HexEditLite.py, in addition to help develop it'''
import sys
import unittest

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

class BufferTest(unittest.TestCase):
    # https://docs.python.org/3.5/library/unittest.html#module-unittest
    pass
    '''
    def setUp(self):
        self.buf = py3.Buffer("test.tmp")
        
    def testRead(self):
        temp = []
        for i in range(0,256):
            for j in range(0,256):
                temp.append(j)
        self.assertListEqual(self.buf[0:256*256], temp)
        self.assertEqual(len(self.buf), 256*256)
        
    def testSanity(self):
        self.assertListEqual(self.buf[0:5], [0,1,2,3,4])
        
    def tearDown(self):
        self.buf.close()
        '''

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

        #Unit Tests
        unittest.main()
