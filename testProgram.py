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
    
    def setUp(self):
        fd = open("test.tmp","wb")
        for i in range(0,256):
            for j in range(0,256):
                fd.write(j.to_bytes(1, sys.byteorder))
        fd.close()        
        self.buf = py3.Buffer("test.tmp")
        
    def tearDown(self):
        self.buf.close()     
        
    def testSimpleRead(self):
        temp = []
        for i in range(0,256):
            for j in range(0,256):
                temp.append(j)
        self.assertListEqual(self.buf[0:256*256], temp)
        self.assertEqual(len(self.buf), 256*256)
        self.assertEqual(255, self.buf[256*256-1]) #remember, indexes are zero indexed
        self.assertEqual(None, self.buf[256*256])
        
    def testReadWrite(self):
        self.buf[0] = 255
        self.assertEqual(255, self.buf[0])
        self.buf[0] = None
        self.assertEqual(None, self.buf[0])
        self.assertListEqual([None, 1], self.buf[0:2])
        for i in range(0,256):
            self.buf[i] = None
        self.assertListEqual([None for i in range(0, 256)], self.buf[0:256])
        for i in range(0,256):
            self.buf[i] = 255
        self.assertListEqual([255 for i in range(0, 256)], self.buf[0:256])
        
    def testReadSlice(self):
        pass
        
    def testLen(self):
        self.assertEqual(len(self.buf), 256*256)
        self.buf[256*256-1] = None
        self.assertEqual(len(self.buf), 256*256-1)
        self.buf[256*256-1] = 255
        self.assertEqual(len(self.buf), 256*256)
        self.buf[256*256+256] = 0
        self.assertEqual(len(self.buf), 256*256+256-1)
        
    def testBlockEviction(self):
        pass
    
    def testRaisedError(self):
        with self.assertRaises(ValueError):
            self.buf[0] = -1
            self.buf[0] = 256
        with self.assertRaises(TypeError):
            self.buf[0] = ""
            self.buf[0] = []
            self.buf[0] = {}
            self.buf[0] = True
            self.buf[0] = 0.0

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

        #Unit Tests
        unittest.main(verbosity=2,exit=False)
        print("Test Complete")
