import math
import os
import sys

version = "v0.2"

class Debug:
    """Class for logging and debuging"""
    def __init__(self, debugMode, file="Py3HexEditLite.log"):
        self.__filename = file
        self.showDebug = debugMode #Bool
        
    def __save(self, text):
        """Function to save each log entry"""
        logfile = open(self.__filename, 'a')
        try:
            logfile.write(text)
        except:
            self.err("Error Occured in Error Logging Function: Attempting to report previous error")
            for i in text:
                try:
                    logfile.write(i)
                except:
                    logfile.write("[ERROR]")
        logfile.close()
    
    def err(self, text):
        """Takes string, pushes to stdout and saves it to the log file
        
        Mainly meant for non-recoverable errors that should cause the program to terminate"""
        temp = "[" + time.asctime() + "] ERR: " + text
        print(temp)
        self.__save(temp + "\n")        
    
    def debug(self, *args):
        """takes n number of strings, pushes to stdout and log file
        
        only writes input to stdout/log file when showDebug is True"""
        if (self.showDebug):
            temp = "Debug:"
            for i in args:
                temp += "\t" + str(i) + "\n"
            print(temp, end="") #fixes issue where log and sceen output newlines don't match
            self.__save(temp)

class Keyboard:
    """A small class for handling AND parsing single character keyboard input"""
    env = None
    try:
        import msvcrt #windows specific operations
        env = "W"
    except:
        import tty #unix specific operation
        import sys
        import termios #unix specific operation
        env = "L"
    
    def __init__(self):
        self.regularKeys = "" #TODO: is this needed?
        self.escape = {"L":0x1B,"W":0xE0}
        #this looks backwards, but is meant to make it easy to edit these character bindings
        self.specialKeys = {"CTRL+A"  :{"L":0x01      ,"W":0x01      },
                            "CTRL+E"  :{"L":0x05      ,"W":0x05      },
                            "CTRL+Q"  :{"L":0x11      ,"W":0x11      },
                            "CTRL+S"  :{"L":0x13      ,"W":0x13      },
                            "CTRL+Y"  :{"L":0x19      ,"W":0x19      },
                            "CTRL+Z"  :{"L":0x1A      ,"W":0x1A      },
                            "UP"      :{"L":0x1B5B41  ,"W":0xE048    },
                            "DOWN"    :{"L":0x1B5B42  ,"W":0xE050    },
                            "LEFT"    :{"L":0x1B5B44  ,"W":0xE04B    },
                            "RIGHT"   :{"L":0x1B5B43  ,"W":0xE04D    },
                            #"ESC"     :{"L":0x1B      ,"W":0x1B      } #problimatic since 0x1B is the linux escape character (I think?)
                            "DEL"     :{"L":0x1B5B33  ,"W":0xE053    } #"L" should be 0x1B5B337E, but I'll ignore the 4th chr for simplicity
                            }

    def _getch(self):
        """Gets a single raw character from the keyboard"""
        # http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
        if (self.env == "W"):
            return self.msvcrt.getch()
        if (self.env == "L"):
            terminalFD = self.sys.stdin.fileno()
            oldSetting = self.termios.tcgetattr(terminalFD)
            try:
                self.tty.setraw(self.sys.stdin.fileno())
                ch = self.sys.stdin.read(1)
            except:
                pass
            finally:
                self.termios.tcsetattr(terminalFD, self.termios.TCSADRAIN, oldSetting)
            return ch
        
    def getch(self):
        """parses keyboard input, returns str representing keypress (IE: 'a', '1', 'Ctrl+Z')"""
        raw = self._getch()
        output = None
        #print(str(raw))
        if (ord(raw) == self.escape[self.env]):
            if (self.env == "W"):
                temp = ord(raw)*256 + ord(self._getch())
            if (self.env == "L"):
                temp = ord(raw)*256**2 + ord(self._getch())*256 + ord(self._getch())
            #print(temp)
            for i in self.specialKeys.keys():
                if (self.specialKeys[i][self.env] == temp):
                    return i
        else:
            for i in self.specialKeys.keys():
                if (self.specialKeys[i][self.env] == ord(raw)):
                    return i
        return raw

'''
class WriteBuffer:
    def __init__(self):
        self.actions = []
        self.redoStack = []
    def undo(self):
        """removes last action from action queue (appends to redo stack)"""
        pass
    def redo(self):
        """Appends action from redo stack to action queue"""
        pass
    #ef write(self):
    #   #resets redo buffer
    #    pass
    def __setitem__(self,key,value):
        # https://docs.python.org/3/reference/datamodel.html#object.__setitem__
        pass
    def __getitam__(self,key):
        # https://docs.python.org/3/reference/datamodel.html#object.__getitem__
        pass
    def __len__(self):
        # https://docs.python.org/3/reference/datamodel.html#object.__len__
        pass
    def status(self):
        """returns float representing how 'full' the buffer is as percentage"""
        pass

class ReadBuffer:
    def __init__(self):
        self.fd = None
        self.blocks = {}
        self.blockSize = 1024*4
    def __getitam__(self,key):
        # https://docs.python.org/3/reference/datamodel.html#object.__getitem__
        pass
    def __len__(self):
        # https://docs.python.org/3/reference/datamodel.html#object.__len__
        pass
    def status(self):
        """returns float representing how 'full' the buffer is as percentage"""
        pass
'''
class Buffer:
    import os
    import math
    def __init__(self, filePath):
        self.filePath = filePath
        self.file = open(filePath,'r+b') #assume filepath is valid
        self.blocks = {} #contains {Offset:(lastAccessTime, bytearray)}
        self.blockSize = 16 #1024*4
        self.actionQueue = [] #contains actions as an ordered list of tuples (offset, data)
        self.redoStack = []
        
        self._cacheMiss(0x00)
        debug.debug("buffer Blocks", self.blocks)
        
    def __delitem__(self,key):
        # https://docs.python.org/3/reference/datamodel.html#object.__delitem__
        self.actionQueue.append((key,None))
        
    def __getitem__(self,key):
        """returns array of ints (NOT BYTES)
        
        will return array of ints, or None in cases where the byte has been deleted
        DO NOT itterate over with a for loop, IndexError will not be raised
        """
        # https://docs.python.org/3/reference/datamodel.html#object.__getitem__
        if (isinstance(key,slice)):
            #print("Slice stuff:", key.start, key.stop, key.step)
            step = 1
            if (key.step != None):
                step = key.step
            i = key.start
            temp = []
            while (i<key.stop):
                if (self._inCache(i) == False):
                    self._cacheMiss(i)
                temp.append(self.blocks[(i // self.blockSize) * self.blockSize][i - (i // self.blockSize) * self.blockSize])
                i += step
            
            for i in self.actionQueue:
                if ((i[0] >= key.start) and (i[0] < key.stop) and (i[0] % step == key.start % step)):
                    temp[(i[0] - key.start) // step] = i[1]
                
                
            return temp
        else: #it's a regular int
            if (self._inCache(key) == False):
                self._cacheMiss(key)
            temp = self.blocks[(key // self.blockSize) * self.blockSize][key - (key // self.blockSize) * self.blockSize]
            for i in self.actionQueue:
                if (i[0] == key):
                    temp = i[1]
            return temp
        
    def __len__(self):
        """Returns length equal to the last last byte available/altered"""
        # https://docs.python.org/3/reference/datamodel.html#object.__len__
        temp = self.os.path.getsize(self.filePath)
        for i in self.actionQueue:
            if (i[0] > temp):
                temp = i[0]
        return temp
    def __setitem__(self,key,value):
        # https://docs.python.org/3/reference/datamodel.html#object.__setitem__
        self.actionQueue.append((key,value))
    
    def _inCache(self,offset):
        if ((offset // self.blockSize) * self.blockSize in self.blocks.keys()):
            return True
        else:
            return False
    
    def _cacheMiss(self,offset):
        """loads a block of the file into memeory"""
        #Assume _inCache() has already been called
        closestBlock = (offset // self.blockSize) * self.blockSize
        if (len(self.blocks) >= 8):
            self._cacheEvict(closestBlock)
        fileSize = self.os.path.getsize(self.filePath)
        block = []
        if (closestBlock > fileSize):
            block = [None for i in range(0,self.blockSize)]
        else:
            self.file.seek(closestBlock)
            temp = self.file.read(self.blockSize)
            for i in range(0,len(temp)):
                block.append(temp[i]) #temp[i] is int
            for i in range(len(temp),self.blockSize):
                block.append(None)
        self.blocks[closestBlock] = block
    def _cacheEvict(self,current):
        """Takes the current location of read, evicts block from memory that isn't current"""
        # evict furthest block from current block
        closestBlock = (current // self.blockSize) * self.blockSize
        furthestBlock = closestBlock
        for i in list(self.blocks.keys()):
            if (abs(closestBlock - i) > abs(closestBlock - furthestBlock)):
                furthestBlock = i
        del(self.blocks[furthestBlock])
        
    def undo(self):
        """removes last action from action queue (appends to redo stack)"""
        pass
    def redo(self):
        """Appends action from redo stack to action queue"""
        pass
    def status(self):
        """returns float representing how 'full' the buffer is as percentage"""
        pass
    def flag(self, start, finish):
        """Returns array of bool signifying which bytes have been changed"""
        pass
    def close(self):
        #remember to delete all the buffers
        self.file.close()
    def save(self):
        #if editied file is smaller then original, create a copy to resize
        pass

def _interface(data, curserLocation, screenLocation):
    """Prints file name, size of file, buffer status, and the hex editing interface"""
    #test interface
    text = "Py3HexEditLite " + version.ljust(8, " ") + "File:" + filePath[-52:].ljust(52," ") + "\n"
    text += "Size: " + "{0:7.2f}".format(fileSize / int(1024 ** math.floor(math.log(fileSize,1024)))) + " " 
    try: #Just in case 2**10 years in the future, someone decides to open the entirety of the internet worth of a file in this hex editor...
        text += " KMGTPEZY"[int(math.floor(math.log(fileSize,1024)))] + "B"
    except IndexError:
        text += "?B"
    text += " Buffer:XXX%|XXX% Location:" + ("0x" + hex(math.floor(curserLocation))[2:].upper()).rjust(18, " ")
    text += "/" + ("0x" + hex(fileSize)[2:].upper()).rjust(18, " ") + "\n"
    for i in range(screenLocation//16,screenLocation//16 + 16): #TODO: this is a shortcut, fix it
        temp = hex(i*16)[2:].zfill(12) + "|"
        for j in range(0,8):
            temp += " "
            if (curserLocation == i*16+j): #large 4 bits
                temp += "-"
            elif (len(data) <= i*16+j):
                temp += "_"
            else:
                temp += hex(data[i*16+j] // 16)[2:].upper()
            
            if (curserLocation == i*16+j+0.5): #small 4 bits
                temp += "-"
            elif (len(data) <= i*16+j):
                temp += "_"
            else:
                temp += hex(data[i*16+j] % 16)[2:].upper()
        temp += "|"
        for j in range(8,16):
            temp += " "
            if (curserLocation == i*16+j): #large 4 bits
                temp += "-"
            elif (len(data) <= i*16+j):
                temp += "_"
            else:
                temp += hex(data[i*16+j] // 16)[2:].upper()
            
            if (curserLocation == i*16+j+0.5): #small 4 bits
                temp += "-"
            elif (len(data) <= i*16+j):
                temp += "_"
            else:
                temp += hex(data[i*16+j] % 16)[2:].upper()
        temp += "| "
        for j in range(0,16):
            if i*16+j >= len(data):
                temp += " "
            else:
                if chr(data[i*16+j]).isprintable():
                    temp += chr(data[i*16+j])
                else:
                    temp += "."
        text += temp + "\n"
    text += "[" + mode+ "]"
    print(text)

def _up():
    """Move curser up: takes current curser/screen location, returns new curser/screen location"""
    global curserLocation
    global screenLocation    
    if (screenLocation > curserLocation - 16):
        temp = max(0, screenLocation - 16)
    else:
        temp = screenLocation
    if (curserLocation < 16):
        temp2 = curserLocation
    else:
        temp2 = curserLocation - 16
    curserLocation = temp2
    screenLocation = temp
def _down():
    """Move curser down: takes current curser/screen location, returns new curser/screen location"""
    global curserLocation
    global screenLocation    
    if (((curserLocation + 16)// 16) * 16 - screenLocation) >= 256:
        temp = screenLocation + 16
    else:
        temp = screenLocation
    curserLocation = curserLocation + 16
    screenLocation = temp
def _left():
    """Move curser left: takes current curser/screen location, returns new curser/screen location"""
    global curserLocation
    global screenLocation    
    if (screenLocation > curserLocation - 0.5):
        temp = max(0, screenLocation - 16)
    else:
        temp = screenLocation
    curserLocation = max(0, curserLocation - 0.5)
    screenLocation = temp
def _right():
    """Move curser right: takes current curser/screen location, returns new curser/screen location"""
    global curserLocation
    global screenLocation    
    if (((curserLocation + 0.5)// 16) * 16 - screenLocation) >= 256:
        temp = screenLocation + 16
    else:
        temp = screenLocation
    curserLocation = curserLocation + 0.5
    screenLocation = temp

def save():
    pass
def openfile(filePath):
    if (os.path.exists(filePath) == False):
        commandMessage = "ERROR: filepath does not exist"
        return -1
    else:
        fileBuffer = Buffer(filePath)
def new(filePath):
    pass
def quit():
    pass
def goto(x):
    pass
def find(x):
    pass
def _write(location, byte):
    global curserLocation
    global screenLocation
    debug.debug("_write", location, byte)
    number = int(byte,16)
    if ((location - math.floor(location)) == 0):
        buffer[int(math.floor(location))] = number*16 + (buffer[int(math.floor(location))] % 16)
        _right()
    elif ((location - math.floor(location)) == 0.5):
        buffer[int(math.floor(location))] = (buffer[int(math.floor(location))] // 16) * 16 + number
        _right()
    else:
        debug.debug("_write error")
        
if __name__ == "__main__":
    debug = Debug(True)
    print("Starting Py3HexEditLite.py")
    debug.debug("Starting Py3HexEditLite.py===================================")

    filePath = None
    try:
        debug.debug("sys.argv", sys.argv)
        filePath = sys.argv[1]
    except:
        print("file has not been passed to argument")
        filePath = ""
        while (os.path.exists(filePath) == False):
            filePath = input("Enter a file path:")
        
    print("Py3HexEditLite " + version + " has started")
    print("Attempting to Open file: " + filePath)
    
    buffer = Buffer(filePath)
    
    fileSize = os.path.getsize(filePath)
    curserLocation = 0.0 #A real, since in hex, a byte is represented as 2 hex chars
    screenLocation = 0 #in multiples of 16
    mode = "Hex"
    
    #Keyboard input
    keyboard = Keyboard()
    while (True):
        _interface(buffer, curserLocation, screenLocation)
        
        raw = keyboard.getch()
        debug.debug("variable \"raw\"", type(raw),len(raw),str(raw))
        if (raw == "UP"):
            _up()
        elif (raw == "DOWN"):
            _down()
        elif (raw == "LEFT"):
            _left()
        elif (raw == "RIGHT"):
            _right()
        elif (raw == "CTRL+Q"):
            if (mode == "Hex"):
                mode = "Text"
            elif (mode == "Text"):
                mode = "Hex"         
        #elif (raw == "CTRL+E"): #TODO
        #    mode = "Input"
        elif (len(raw) == 1):
            if (chr(ord(raw)) in "1234567890abcdefABCDEF"):
                _write(curserLocation, raw)
                debug.debug("raw 1", raw)
