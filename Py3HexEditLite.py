#!/usr/bin/env python3

import code
import math
import os
import sys

version = "v0.4"

class Debug:
    """Class for logging and debuging"""
    def __init__(self, debugMode, file="Py3HexEditLite.log"):
        self.__filename = file
        self.showDebug = debugMode #Bool
        
    def __save(self, text):
        """Function to save each log entry"""
        if (self.showDebug == True):
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
            finally:
                logfile.close()
    
    def err(self, text):
        """Takes string, pushes to stdout and saves it to the log file
        
        Mainly meant for non-recoverable errors that should cause the program to terminate"""
        line = "[" + time.asctime() + "] ERR: " + text
        print(line)
        self.__save(line + "\n")        
    
    def debug(self, *args):
        """takes n number of strings, pushes to stdout and log file
        
        only writes input to stdout/log file when showDebug is True"""
        if (self.showDebug):
            line = "Debug:"
            for i in args:
                line += "\t" + str(i) + "\n"
            print(line, end="")
            self.__save(line)

class Keyboard:
    """A small class for handling AND parsing single character keyboard input"""
    #TODO: should this be instatiated
    env = None #The detected environment, either "W" for windows, or "L" for linux
    
    #This detects what input method would would work (windows of linux) based on what imports work/fail
    try:
        #Windows
        import msvcrt #windows specific operations
        env = "W"
    except:
        #Unix
        import tty #unix specific operation
        import sys
        import termios #unix specific operation
        env = "L"
    
    def __init__(self):
        self.escape = {"L":[0x1B], "W":[0xE0, 0x00]}
        #this looks backwards, but is meant to make it easy to edit these character bindings
        self.specialKeys = {"CTRL+A"  :{"L":0x01      ,"W":0x01      },
                            "CTRL+B"  :{"L":0x02      ,"W":0x02      },
                            "CTRL+C"  :{"L":0x03      ,"W":0x03      },
                            "CTRL+D"  :{"L":0x04      ,"W":0x04      },
                            "CTRL+E"  :{"L":0x05      ,"W":0x05      },
                            "CTRL+F"  :{"L":0x06      ,"W":0x06      },
                            "CTRL+G"  :{"L":0x07      ,"W":0x07      },
                            "CTRL+H"  :{"L":0x08      ,"W":0x08      },
                            #"CTRL+I"  :{"L":0x09      ,"W":0x09      }, #Same as \t
                            #"CTRL+J"  :{"L":0x0A      ,"W":0x0A      }, #same as \n
                            "CTRL+K"  :{"L":0x0B      ,"W":0x0B      },
                            "CTRL+L"  :{"L":0x0C      ,"W":0x0C      },
                            #"CTRL+M"  :{"L":0x0D      ,"W":0x0D      }, #This is the same as ENTER
                            "CTRL+N"  :{"L":0x0E      ,"W":0x0E      },
                            "CTRL+O"  :{"L":0x0F      ,"W":0x0F      },
                            "CTRL+P"  :{"L":0x10      ,"W":0x10      },
                            "CTRL+Q"  :{"L":0x11      ,"W":0x11      },
                            "CTRL+R"  :{"L":0x12      ,"W":0x12      },
                            "CTRL+S"  :{"L":0x13      ,"W":0x13      },
                            "CTRL+T"  :{"L":0x14      ,"W":0x14      },
                            "CTRL+U"  :{"L":0x15      ,"W":0x15      },
                            "CTRL+V"  :{"L":0x16      ,"W":0x16      },
                            "CTRL+W"  :{"L":0x17      ,"W":0x17      },
                            "CTRL+X"  :{"L":0x18      ,"W":0x18      },
                            "CTRL+Y"  :{"L":0x19      ,"W":0x19      },
                            "CTRL+Z"  :{"L":0x1A      ,"W":0x1A      },
                            "ENTER"   :{"L":0x0D      ,"W":0x0D      }, #This is the same as CTRL+M
                            "UP"      :{"L":0x1B5B41  ,"W":0xE048    },
                            "DOWN"    :{"L":0x1B5B42  ,"W":0xE050    },
                            "LEFT"    :{"L":0x1B5B44  ,"W":0xE04B    },
                            "RIGHT"   :{"L":0x1B5B43  ,"W":0xE04D    },
                            #"ESC"     :{"L":0x1B      ,"W":0x1B      } #problimatic since 0x1B is the linux escape character (I think?)
                            "DEL"     :{"L":0x1B5B33  ,"W":0xE053    }, #"L" 0x1B5B337E
                            "PAGEUP"  :{"L":0x1B5B35  ,"W":0xE049    }, #"L" 0x1B5B357E
                            "PAGEDOWN":{"L":0x1B5B36  ,"W":0xE051    }  #"L" 0x1B5B367E
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
                character = self.sys.stdin.read(1)
            except:
                pass
            finally:
                self.termios.tcsetattr(terminalFD, self.termios.TCSADRAIN, oldSetting)
            return character
        
    def getch(self):
        """parses keyboard input, returns str representing keypress (IE: 'a', '1', 'Ctrl+Z')"""
        #TODO: decide what the output type should be
        raw = self._getch()
        output = None
        if (ord(raw) in self.escape[self.env]):
            characterCode = 0
            if (self.env == "W"):
                characterCode = ord(raw) * 256 + ord(self._getch())
            if (self.env == "L"):
                characterCode = ord(raw) * 256**2 + ord(self._getch()) * 256 + ord(self._getch())
            for i in self.specialKeys.keys():
                if (self.specialKeys[i][self.env] == characterCode):
                    if (self.env == "L") and (i in ["DEL","PAGEUP","PAGEDOWN"]): #TODO: figure out better way to figure out which keys need to get that special character
                        self._getch()
                    return i
        else:
            for i in self.specialKeys.keys():
                if (self.specialKeys[i][self.env] == ord(raw)):
                    if (self.env == "L") and (i in ["DEL","PAGEUP","PAGEDOWN"]): #TODO: figure out better way to figure out which keys need to get that special character
                        self._getch()
                    return i
        return raw

class Buffer:
    import os
    import math
    
    def __init__(self, path): #TODO: implement ability to open file in readonly mode
        self.filePath = path
        self.file = open(path, 'r+b') #does not handle exceptopns here, so calling function can handle raised exceptions
        self.fileSize = self.file.seek(0,2)
        
        self._readBuffer = {} #contains blocks of data from the open file, stored as {Offset:[array of int 0<=x<=255 or None]}
        self._writeBuffer = {} #contains blocks of data to be writen to file, stored as {Offset:[array of int 0<=x<=255 or None]}
        self._blockSize = 4096 #Size the data block loaded from files
        self._bufferSize = 8 #maximum number of read blocks to hold in memory
        
        self._actionQueue = [] #contains actions as an ordered list of tuples (offset, data)
        self._redoStack = [] #contains actions as stack of tuples (offset, data)
        
    def __delitem__(self, index):
        # https://docs.python.org/3/reference/datamodel.html#object.__delitem__
        self._actionQueue.append((index, None))
        #TODO: change this to also shift bytes when needed
        
    def __getitem__(self, key):
        """returns array of ints and Nones (NOT BYTES)
        
        will return array of ints, or None in cases where the byte has been deleted
        DO NOT itterate over directly with a 'for' loop, IndexError will not be raised, thus the for loop will NOT terminate
        """
        # https://docs.python.org/3/reference/datamodel.html#object.__getitem__
        if (isinstance(key, slice)): #it's a slice
            #TODO: implement full functionality (raise errors, handle cases ([1:],[:1],[:],[-1:],etc)
            step = 1
            if (key.step != None):
                step = key.step
            i = key.start
            temp = []
            while (i < key.stop):
                if (self._inCache(i) == False):
                    self._cacheMiss(i)
                temp.append(self._readBuffer[(i // self._blockSize) * self._blockSize][i - (i // self._blockSize) * self._blockSize])
                i += step
            
            for i in self._actionQueue:
                if ((i[0] >= key.start) and (i[0] < key.stop) and (i[0] % step == key.start % step)):
                    temp[(i[0] - key.start) // step] = i[1]
            return temp
        else: #it's a regular int
            if (self._inCache(key) == False):
                self._cacheMiss(key)
            temp = self._readBuffer[(key // self._blockSize) * self._blockSize][key - (key // self._blockSize) * self._blockSize]
            for i in self._actionQueue:
                if (i[0] == key):
                    temp = i[1]
            return temp
        
    def __len__(self):
        """Returns length equal to the last last byte available/altered"""
        # https://docs.python.org/3/reference/datamodel.html#object.__len__
        #length = self.os.path.getsize(self.filePath)
        length = self.fileSize
        for i in self._actionQueue:
            if (i[0] > length):
                length = i[0]
        return length
    
    def __setitem__(self,index,value):
        # https://docs.python.org/3/reference/datamodel.html#object.__setitem__
        self._actionQueue.append((index, value))
    
    def _inCache(self, offset):
        if ((offset // self._blockSize) * self._blockSize in self._readBuffer.keys()):
            return True
        else:
            return False
    
    def _cacheMiss(self, offset):
        """loads a block of the file into memeory"""
        #Assume _inCache() has already been called
        closestBlock = (offset // self._blockSize) * self._blockSize
        if (len(self._readBuffer) >= self._bufferSize):
            self._cacheEvict(closestBlock)
        block = []
        if (closestBlock > self.fileSize):
            block = [None for i in range(0, self._blockSize)]
        else:
            self.file.seek(closestBlock)
            temp = self.file.read(self._blockSize)
            for i in range(0, len(temp)):
                block.append(temp[i])
            for i in range(len(temp), self._blockSize):
                block.append(None)
        self._readBuffer[closestBlock] = block
        
    def _cacheEvict(self, current):
        """Takes the current location of read, evicts block from memory that isn't current
        
        Evict furthest block from current block
        """
        closestBlock = (current // self._blockSize) * self._blockSize
        furthestBlock = closestBlock
        for i in list(self._readBuffer.keys()):
            if (abs(closestBlock - i) > abs(closestBlock - furthestBlock)):
                furthestBlock = i
        del(self._readBuffer[furthestBlock])
        
    def undo(self):
        """removes last action from action queue (appends to redo stack)"""
        pass
    
    def redo(self):
        """Appends action from redo stack to action queue"""
        pass
    
    def status(self):
        """returns string representing how 'full' the various buffers are"""
        pass
    
    def mask(self, start, stop=None):
        """Returns bool signifying which bytes have been changed when stop == None
        Returns array of bool when stop != None"""
        pass
    
    def close(self):
        #remember to delete all the buffers
        del(self._actionQueue[:])
        del(self._redoStack[:])
        del(self._readBuffer)
        self.file.close()
        
    def flush(self):
        """Writes the actions to file"""
        #TODO: if editied file is smaller then original, create a copy to resize
        for i in self._actionQueue:
            self.file.seek(i[0])
            if (i[1] == None):
                self.file.write((0).to_bytes(1, sys.byteorder))
            else:
                self.file.write((i[1]).to_bytes(1, sys.byteorder))
        self.file.flush()
        del(self._actionQueue[:])
        del(self._redoStack[:])
        for i in list(self._readBuffer.keys()):
            del(self._readBuffer[i])
            
    def refresh(self):
        """refreshes all buffers without writing/updating file"""
        del(self._actionQueue[:])
        del(self._redoStack[:])
        for i in list(self._readBuffer.keys()):
            del(self._readBuffer[i])        

class window:   
    def interface():
        """Prints the interface window"""
        text = ""
        text += window._header()
        text += window._body()
        text += window._footer()
        print(text)
    
    def _header():
        """Returns String representing the first 4 lines of interface window, newline terminated"""
        global filePath
        global fileSize
        #global mode
        
        text = ""
        text = "Py3HexEditLite " + version.ljust(8, " ") + "File:" + filePath[-52:].ljust(52," ") + "\n"
        text += "Size: " + "{0:7.2f}".format(fileSize / int(1024 ** math.floor(math.log(fileSize, 1024)))) + " " 
        try: #Just in case 2**10 years in the future, someone decides to open the entirety of the internet worth of a file in this hex editor...
            text += " KMGTPEZY"[int(math.floor(math.log(fileSize, 1024)))] + "B"
        except IndexError:
            text += "?B"
        text += " Buffer:XXX%|XXX% Location:" + ("0x" + hex(math.floor(curserLocation))[2:].upper()).rjust(18, " ")
        text += "/" + ("0x" + hex(fileSize)[2:].upper()).rjust(18, " ")     
        return text + "\n"
    
    def _body():
        """Returns String representing 16 lines where you can edit stuff, newline terminated"""
        global screenLocation
        global curserLocation 
        global buffer
        
        text = ""
        line = ""
        #debug.debug("_body", curserLocation, screenLocation, mode)
        for i in range(screenLocation // 16, screenLocation // 16 + 16):
            line = hex(i * 16)[2:].upper().rjust(12, " ") + "|"
            for j in range(0, 16):
                if (j == 8):
                    line += "|"
                
                line += " "
                if ((curserLocation == i * 16 + j) and (mode == "HEX")): #large 4 bits
                    line += "-"
                elif (buffer[i * 16 + j] == None):
                    line += "_"
                else:
                    line += hex(buffer[i * 16 + j] // 16)[2:].upper()
                
                if ((curserLocation == i * 16 + j + 0.5) and (mode == "HEX")): #small 4 bits
                    line += "-"
                elif (buffer[i * 16 + j] == None):
                    line += "_"
                else:
                    line += hex(buffer[i * 16 + j] % 16)[2:].upper()

            line += "| "
            for j in range(0, 16):
                if ((math.floor(curserLocation) == i * 16 + j) and (mode == "TEXT")):
                    line += "-"
                elif (buffer[i * 16 + j] == None):
                    line += " "
                elif chr(buffer[i * 16 + j]).isprintable():
                    line += chr(buffer[i * 16 + j])
                else:
                    line += "."
            
            text += line + "\n"
        return text
    
    def _footer():
        """Returns String 4 lines max with any additional information needed, newline terminated"""
        global mode
        return "[" + mode + "]"

#control functions, not inteneded to be directly accesable to the user
def _command():
    """meant to help execute commands within the current python3 environement"""
    # https://docs.python.org/3.5/library/code.html
    # can't use sys.ps1 and sys.ps2 since it doesn't work on windows?
    # TODO: streamline this, it seems like a mess
    
    debug.debug("command")
    compiledCode = None
    userCode = ""
    line = ""
    while compiledCode == None:
        if userCode == "":
            line = input(">>>")#sys.ps1
        else:
            line = input("...")#sys.ps2
            
        if line == "":
            userCode += "\n"
            break
        else:
            userCode += line
            
        try:
            compiledCode = code.compile_command(userCode)
        except SyntaxError:
            userCode = ""
            print("syntax error")
        except (OverflowError, ValueError):
            userCode = ""
            print("invalid literal")
    debug.debug("command", userCode, compiledCode)
    userCode = code.compile_command(userCode)
    try:
        exec(userCode)
    except Exception as i:
        # TODO: return all error messages
        debug.debug("command execution error", i)
    
def _down():
    """Move curser down, sets curserLocation, adjusts screenLocation as needed"""
    global curserLocation
    global screenLocation
    
    if (((curserLocation + 16)// 16) * 16 - screenLocation) >= 256:
        screenLocation = screenLocation + 16
    curserLocation = curserLocation + 16
    
def _left():
    """Move curser left, sets curserLocation, adjusts screenLocation as needed"""
    global curserLocation
    global screenLocation
    global mode
    
    if (mode == "HEX"):
        moveAmount = 0.5
    elif (mode == "TEXT"):
        moveAmount = 1
    
    if (screenLocation > curserLocation - moveAmount):
        screenLocation = max(0, screenLocation - 16)
    curserLocation = max(0, curserLocation - moveAmount)
    
def _right():
    """Move curser right, sets curserLocation, adjusts screenLocation as needed"""
    global curserLocation
    global screenLocation
    global mode
    
    if (mode == "HEX"):
        moveAmount = 0.5
    elif (mode == "TEXT"):
        moveAmount = 1    
    
    if (((curserLocation + moveAmount)// 16) * 16 - screenLocation) >= 256:
        screenLocation = screenLocation + 16
    curserLocation = curserLocation + moveAmount

def _up():
    """Move curser up, sets curserLocation, adjusts screenLocation as needed"""
    global curserLocation
    global screenLocation
    
    if (screenLocation > curserLocation - 16):
        screenLocation = max(0, screenLocation - 16)
    if (curserLocation >= 16):
        curserLocation = curserLocation - 16
    
def _write(location, byte):
    """Write a single byte to the current curserLocation, use only when in HEX mode"""
    global curserLocation
    '''
    if (byte == None):
        buffer[int(math.floor(location))] = None
    elif ((location - math.floor(location)) == 0):
        number = int(byte,16)
        if (buffer[int(math.floor(location))] == None):
            buffer[int(math.floor(location))] = 0
        buffer[int(math.floor(location))] = number * 16 + (buffer[int(math.floor(location))] % 16)
        _right()
    elif ((location - math.floor(location)) == 0.5):
        number = int(byte,16)
        if (buffer[int(math.floor(location))] == None):
            buffer[int(math.floor(location))] = 0        
        buffer[int(math.floor(location))] = (buffer[int(math.floor(location))] // 16) * 16 + number
        _right()
    '''
    number = int(byte,16)
    if ((location - math.floor(location)) == 0):
        if (buffer[int(math.floor(location))] == None):
            buffer[int(math.floor(location))] = 0
        buffer[int(math.floor(location))] = number * 16 + (buffer[int(math.floor(location))] % 16)
    elif ((location - math.floor(location)) == 0.5):
        if (buffer[int(math.floor(location))] == None):
            buffer[int(math.floor(location))] = 0        
        buffer[int(math.floor(location))] = (buffer[int(math.floor(location))] // 16) * 16 + number

# API, accessable by user in 'COMMAND' mode
#TODO: decide if API functions should return a value, if they should be able to directly print to the console, and if they should be able to raise errors
def goto(x):
    """Moves curser to x, adjusts screenLocation accordingly"""
    global curserLocation
    global screenLocation
    if (not ((type(x) == int) or (type(x) == float))):
        raise TypeError
    elif (x < 0):
        raise ValueError
    curserLocation = math.floor(x * 2) / 2
    screenLocation = int(x // 16) * 16
    debug.debug("goto", curserLocation, screenLocation)
    
def newFile(path):
    """Creates a new empty file"""
    global buffer
    pass

def openFile(path):
    """opens a file for editing"""
    # TODO: make this also close the previously open file
    # https://docs.python.org/3/library/os.path.html#os.path.isfile
    global buffer
    global fileSize
    global filePath
    
    # TODO: fix and properly test this to enable use for block editing raw drive blocks, and other stuff?
    if (os.path.exists(path) == False):
        #raise FileNotFoundError
        print("ERROR: File Not Found")
        return -1
    if (os.path.isdir(path) == True):
        print("Attempting to open a directory")
    if (os.path.islink(path) == True):
        print("Attemtping to open a sumbolic link")
    if (os.path.ismount(path) == True):
        print("Attempting to open a mount point")
    '''
    if (os.path.isfile(path) == False): #this does not allow opening a drive (as a block device)
        #raise IsADirectoryError
        print("ERROR: Path Not File")
        return -1
    '''
    try:
        buffer = Buffer(path)
        #fileSize = os.path.getsize(path) #returns incorrect value when opening a drive (as a block device)
        fileSize = buffer.fileSize
        filePath = path
        print("Successfully opened file: " + path)
        return 0
    except PermissionError:
        print("ERROR: permission denied")
        return -1
    except Exception as i:
        buffer = None
        print("ERROR: could not open file: " + str(i))
        return -1
    
    return 0

def save():
    """Saves current changes to currently open file"""
    global buffer
    global fileSize
    buffer.flush()
    #fileSize = os.path.getsize(filePath)
    fileSize = buffer.fileSize
    
def saveAs(path):
    """Takes a string representing a file path. Creates and opens a new file, saves the current changes, closes the old file"""
    global buffer
    file = None
    try:
        file = open(path, "x+b")
    except Exception as i:
        print("Could not open file to write to")
        print(i)
        return
    for i in range(0, len(buffer)):
        if buffer[i] == None:
            file.write((0).to_bytes(1, sys.byteorder))
        else:
            file.write((buffer[i]).to_bytes(1, sys.byteorder))
    file.close()
    buffer.close()
    
    openFile(path)

def quit():
    """Closes the current session"""
    global buffer
    global debug
    print("Py3HexEditLite.py is quiting")
    buffer.close()
    del(debug)
    exit(0)
    
''' #possible future API
def find(x):
    global buffer
    pass

def trunk(x): #TODO: is this needed?
    """Saves changes, Trucates the file at x"""
    pass

def hexHelp():
    """Prints a help dialogue"""
    pass
    
def api():
    """Prints help dialogue for API the user can use for the command imput"""
    pass
'''

if __name__ == "__main__":
    debug = Debug(True)
    print("Starting Py3HexEditLite.py")
    debug.debug("Starting Py3HexEditLite.py===================================")

    print("Py3HexEditLite " + version + " has started")
    
    #globals
    curserLocation = 0.0 #A real, since in hex, a byte is represented as 2 hex chars
    screenLocation = 0 #in multiples of 16
    mode = "HEX"
    buffer = None
    filePath = None
    fileSize = None
    
    #TODO: allow passing in more the one argument
    #TODO: document args
    if (len(sys.argv) >= 2):
        openFile(sys.argv[1])
    else:
        print("program has not been passed an argument")
        
    while (buffer == None):
        #TODO: make this use a command interpriter instead, using only this is particularly limiting for the user
        filePath = input("Enter a file path:")
        print("Attempting to open file: " + filePath)
        openFile(filePath)
    
    #process keyboard input
    keyboard = Keyboard()
    window.interface()
    while (True):
        
        raw = keyboard.getch()
        
        if (raw == "UP"):
            _up()
        elif (raw == "DOWN"):
            _down()
        elif (raw == "LEFT"):
            _left()
        elif (raw == "RIGHT"):
            _right()
        elif (raw == "CTRL+E"):
            _command()
        elif (raw == "DEL"):
            buffer[int(math.floor(curserLocation))] = None
            #_write(curserLocation, None)
        elif (raw == "CTRL+S"):
            save()
        elif (raw == "CTRL+Q"):
                quit()        
        elif (len(raw) == 1):
            if (mode == "HEX") and ((chr(ord(raw)) in "1234567890abcdefABCDEF")):
                _write(curserLocation, raw)
                _right()
                debug.debug("HEX raw", raw)
            elif (mode == "TEXT") and ((chr(ord(raw))).isprintable()):
                buffer[int(math.floor(curserLocation))] = ord(raw)
                _right()
            if (chr(ord(raw)) == "\t"):
                if (mode == "HEX"):
                    mode = "TEXT"
                elif (mode == "TEXT"):
                    mode = "HEX"
        
        window.interface()
