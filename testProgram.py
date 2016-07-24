#!/usr/bin/env python3
'''A program to help test the various modules of Py3HexEditLite.py, in addition to help develop it'''
import sys
import unittest
import tracemalloc # https://docs.python.org/3/library/tracemalloc.html

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
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        termios.tcsetattr(terminalFD, termios.TCSADRAIN, oldSetting)
        return ch

class BufferTest(unittest.TestCase):
    # https://docs.python.org/3.5/library/unittest.html#module-unittest  
    
    def setUp(self):
        """This resets the file and loads buffer for each test"""
        fd = open("temp.tmp","wb")
        for i in range(0,256):
            for j in range(0,256):
                fd.write(j.to_bytes(1, sys.byteorder))
        fd.close()        
        self.buf = py3.Buffer("temp.tmp")
        
    def tearDown(self):
        """Closes buffer after each test"""
        self.buf.close()     
        
    def testFileStats(self):
        """Tests that buffer gets the stats of the file correct"""
        self.assertEqual(self.buf.filePath, "temp.tmp")
        self.assertEqual(self.buf.fileSize, 256*256)
        
    def testFileReadWrite(self):
        """Tests reading and writing to a file"""
        pass
    
    def testSimpleRead(self):
        """Tests simple reads from buffer"""
        temp = [j for i in range(0, 256) for j in range(0, 256)]
        self.assertEqual(self.buf[0:256*256], temp)
        self.assertEqual(self.buf[256*256-1], 255) #remember, indexes are zero indexed
        self.assertEqual(self.buf[256*256], None)
        
    def testReadWrite(self):
        """Tests reading and writing to/from buffer"""
        self.buf[0] = 255
        self.assertEqual(self.buf[0], 255)
        ''' #testing ability to store deleted characters, will have to replan how to handle them
        self.buf[0] = None
        self.assertEqual(self.buf[0], None)
        self.assertEqual(self.buf[0:2], [None, 1])
        for i in range(0,256):
            self.buf[i] = None
        self.assertEqual(self.buf[0:256], [None for i in range(0, 256)])
        '''
        for i in range(0, 256):
            self.buf[i] = 255
        self.assertEqual(self.buf[0:256], [255 for i in range(0, 256)])
        
    def testReadSlice(self):
        """Tests reading from buffer using slice notation"""
        temp = [j for i in range(0, 256) for j in range(0, 256)]
        
        #test reading with None slice inputs
        self.assertEqual(self.buf[:], temp)
        self.assertEqual(self.buf[:256*256], temp)
        self.assertEqual(self.buf[0:], temp) 
        self.assertEqual(self.buf[0:256*256], temp) #regular
        
        #test reading with None slice inputs
        self.assertEqual(self.buf[::], temp)
        self.assertEqual(self.buf[::1], temp)
        self.assertEqual(self.buf[:256*256:], temp)
        self.assertEqual(self.buf[:256*256:1], temp)
        self.assertEqual(self.buf[0::], temp)
        self.assertEqual(self.buf[0::1], temp)
        self.assertEqual(self.buf[0:256*256:], temp)
        self.assertEqual(self.buf[0:256*256:1], temp)
        self.assertEqual(self.buf[0::], temp)
        self.assertEqual(self.buf[0::1], temp)
        
        #read beyond EOF
        self.assertEqual(self.buf[0:256*256 + 1024], temp + [None for i in range(0, 1024)])
        self.assertEqual(self.buf[:256*256 + 1024], temp + [None for i in range(0, 1024)])
        self.assertEqual(self.buf[0:256*256 + 1024:], temp + [None for i in range(0, 1024)])
        self.assertEqual(self.buf[:256*256 + 1024:1], temp + [None for i in range(0, 1024)])        
        
        #read a subsection to EOF
        self.assertEqual(self.buf[1024:], temp[1024:])
        self.assertEqual(self.buf[1024:256*256], temp[1024:])
        self.assertEqual(self.buf[1024::], temp[1024:])
        self.assertEqual(self.buf[1024::1], temp[1024:])
        self.assertEqual(self.buf[1024:256*256:1], temp[1024:])
        
        #read a subsection to before EOF
        self.assertEqual(self.buf[1024:256*256-1024], temp[1024:256*256-1024])
        self.assertEqual(self.buf[1024:256*256-1024:], temp[1024:256*256-1024])
        self.assertEqual(self.buf[1024:256*256-1024:1], temp[1024:256*256-1024])
        
        #read a subsection to after EOF
        self.assertEqual(self.buf[1024:256*256+1024], temp[1024:] + [None for i in range(0, 1024)])
        self.assertEqual(self.buf[1024:256*256+1024:], temp[1024:] + [None for i in range(0, 1024)])
        self.assertEqual(self.buf[1024:256*256+1024:1], temp[1024:] + [None for i in range(0, 1024)])
        
        #read a subsection from EOF to EOF
        self.assertEqual(self.buf[256*256:256*256+1024], [None for i in range(0, 1024)])
        self.assertEqual(self.buf[256*256+1024:256*256+1024*2], [None for i in range(0, 1024)])
        
    def testReadSliceSingle(self):
        """Tests reading a slice of len == 0"""
        self.assertEqual(self.buf[:1], [0])
        self.assertEqual(self.buf[0:1], [0])
        self.assertEqual(self.buf[:1:], [0])
        self.assertEqual(self.buf[0:1:1], [0])
        self.assertEqual(self.buf[256*256-1:], [255])
        self.assertEqual(self.buf[256*256-1:256*256], [255])
        self.assertEqual(self.buf[256*256-1::], [255])
        self.assertEqual(self.buf[256*256-1:256*256:], [255])
        self.assertEqual(self.buf[256*256-1::1], [255])
        self.assertEqual(self.buf[256*256-1:256*256:1], [255])
        
        #read after EOF
        self.assertEqual(self.buf[256*256:256*256+1], [None])
        self.assertEqual(self.buf[256*256:256*256+1:], [None])
        self.assertEqual(self.buf[256*256:256*256+1:1], [None])
        
    def testReadSliceEmpty(self):
        self.assertEqual(self.buf[:0], [])
        self.assertEqual(self.buf[0:0], [])
        self.assertEqual(self.buf[:0:], [])
        self.assertEqual(self.buf[0:0:1], [])
        self.assertEqual(self.buf[256*256:], [])
        self.assertEqual(self.buf[256*256:256*256], [])
        self.assertEqual(self.buf[256*256::], [])
        self.assertEqual(self.buf[256*256:256*256:1], [])
        
    def testLen(self):
        """Tests len() works properly, even after writes"""
        self.assertEqual(len(self.buf), 256*256)
        #self.buf[256*256-1] = None
        #self.assertEqual(len(self.buf), 256*256-1)
        self.buf[256*256-1] = 255
        self.assertEqual(len(self.buf), 256*256)
        self.buf[256*256+256] = 0
        self.assertEqual(len(self.buf), 256*256+256+1)
        #self.buf[256*256+256] = None
        #self.assertEqual(len(self.buf), 256*256)
        for i in range(0, 10):
            self.buf[i] = 1
        self.assertEqual(len(self.buf), 256*256+256+1)
            
    def testMask(self):
        """Test that bitmap of changed bytes is valid"""
        empty = [False for i in range(0, 256*256+1024)]
        
        self.assertEqual(self.buf.mask(0), False)
        self.assertEqual(self.buf.mask(256*256), False)
        self.assertEqual(self.buf.mask(256*256+1024), False)
        
    def testBlockEviction(self):
        assert self.buf._blockSize == 4096
        
        self.buf.refresh()
        self.assertEqual(len(self.buf._readBuffer), 0)

        self.buf.refresh()        
        self.buf[0]
        self.assertEqual(len(self.buf._readBuffer), 1)
        self.assertEqual(sorted(self.buf._readBuffer.keys()), [0])
        
        #test reading all bytes from one block
        self.buf.refresh()
        for i in range(0, 4096):
            self.buf[i]
            self.assertEqual(len(self.buf._readBuffer), 1)
            self.assertEqual(sorted(self.buf._readBuffer.keys()), [0])
        
        #test reading one byte from 8 blocks
        self.buf.refresh()
        for j in range(0, 16):
            for i in range(0+j, 8+j):
                self.buf[i*4096]
            self.assertEqual(len(self.buf._readBuffer), 8)
            self.assertEqual(sorted(self.buf._readBuffer.keys()), [i*4096 for i in range(0+j, 8+j)])
            
        #test reading one byte from 8 blocks
        self.buf.refresh()
        for j in range(0, 16):
            for i in range(8-1+j, 0-1+j, -1): #reverse read order
                self.buf[i*4096]
            self.assertEqual(len(self.buf._readBuffer), 8)
            self.assertEqual(sorted(self.buf._readBuffer.keys()), [i*4096 for i in range(0+j, 8+j)])
            
        #test reading one byte at x offset from boundry from 8 blocks
        self.buf.refresh()
        for k in range(0, 4096, 16):
            for j in range(0, 16):
                for i in range(0+j, 8+j):
                    self.buf[i*4096+k]
                self.assertEqual(len(self.buf._readBuffer), 8)
                self.assertEqual(sorted(self.buf._readBuffer.keys()), [i*4096 for i in range(0+j, 8+j)])        
        
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
            
        with self.assertRaises(TypeError):
            self.buf[""]
            self.buf[[]]
            self.buf[{}]
            self.buf[True]
            self.buf[0.0]

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
        
    """Manual testing
    # http://stackoverflow.com/questions/6522644/how-to-open-disks-in-windows-and-read-data-at-low-level
    # http://blog.lifeeth.in/2011/03/reading-raw-disks-with-python.html
    sudo python3 ./Py3HexEditLite.py '/dev/sda'
    sudo python3 ./Py3HexEditLite.py '/dev/sda1'
    """    
