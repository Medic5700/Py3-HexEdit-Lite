#!/usr/bin/env python3

import code #for using/acessing the interpriter (IE: COMMAND mode)
import math
import os
import sys
import traceback #for error handling in interpriter (IE: COMMAND mode)

version = "v0.5"

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
    # Keeping this instatiated also keeps this class moduler
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
        self.file = open(path, 'r+b') #does not handle exceptions here, so calling function can handle raised exceptions
        self.fileSize = self.file.seek(0,2)
        
        self._readBuffer = {} #contains blocks of data from the open file, stored as {Offset:[array of int 0<=x<=255 or None]}
        self._writeBuffer = {} #contains blocks of data to be writen to file, stored as {Offset:[array of int 0<=x<=255 or None]}
        self._blockSize = 4096 #Size the data block loaded from files
        self._bufferSize = 8 #maximum number of read blocks to hold in memory
        
        self._actionQueue = [] #contains actions as an ordered list of tuples (offset, data)
        self._redoStack = [] #contains actions as stack of tuples (offset, data)
        self._undoSize = 16 #maximum number of undo actions allowed
        
    def __del__(self):
        """Deconstructor, deletes variables in current instance of buffer"""
        # https://docs.python.org/3/reference/datamodel.html#object.__del__
        del(self._actionQueue[:])
        del(self._redoStack[:])
        del(self._readBuffer)
        del(self._writeBuffer)
        self.file.close()
        
        del(self._blockSize)
        del(self._bufferSize)
        del(self._undoSize)
        
        del(self.filePath)
        del(self.file)
        del(self.fileSize)
        
    '''
    def __delitem__(self, index):
        # currently unsuported until deleting a byte is properly thought out
        # https://docs.python.org/3/reference/datamodel.html#object.__delitem__
        self._actionQueue.append((index, None))
        #TODO: change this to also shift bytes when needed
    '''
    
    def __getitem__(self, key):
        """returns array of ints and Nones (NOT BYTES)
        
        will return array of ints, or None in cases where beyond EOF
        DO NOT itterate over directly with a 'for' loop, IndexError will not be raised, thus the for loop will NOT terminate
        """
        # https://docs.python.org/3/reference/datamodel.html#object.__getitem__
        if (isinstance(key, slice)): #it's a slice
            step = 1
            start = 0
            stop = self.__len__()
            if (key.step != None):
                step = key.step
            if (key.start != None):
                start = key.start
            if (key.stop != None):
                stop = key.stop
                
            i = start
            result = []
            #TODO: improve effiency
            while (i < stop): #Goes through _readBuffer
                if not ((i // self._blockSize) * self._blockSize in self._readBuffer.keys()):
                    self._cacheMiss(i)
                result.append(self._readBuffer[(i // self._blockSize) * self._blockSize][i - (i // self._blockSize) * self._blockSize])
                i += step

            i = start
            #TODO: improve effiency
            while (i < stop): #Goes through _writeBuffer
                if (i // self._blockSize) * self._blockSize in self._writeBuffer.keys():
                    if self._writeBuffer[(i // self._blockSize) * self._blockSize][i - (i // self._blockSize) * self._blockSize] != None:
                        result[i - start] = self._writeBuffer[(i // self._blockSize) * self._blockSize][i - (i // self._blockSize) * self._blockSize]
                i += step
            
            for i in self._actionQueue: #Goes through _actionQueue
                if ((i[0] >= start) and (i[0] < stop) and (i[0] % step == start % step)):
                    result[(i[0] - start) // step] = i[1]
                    
            return result
        
        else: #it's a regular int
            if not (isinstance(5, int)):
                raise TypeError
            
            if not ((key // self._blockSize) * self._blockSize in self._readBuffer.keys()):
                self._cacheMiss(key)
            result = self._readBuffer[(key // self._blockSize) * self._blockSize][key - (key // self._blockSize) * self._blockSize]
            if (key // self._blockSize) * self._blockSize in self._writeBuffer.keys():
                if self._writeBuffer[(key // self._blockSize) * self._blockSize][key - (key // self._blockSize) * self._blockSize] != None:
                    result = self._writeBuffer[(key // self._blockSize) * self._blockSize][key - (key // self._blockSize) * self._blockSize]
            for i in self._actionQueue:
                if (i[0] == key):
                    result = i[1]
            return result
        
    def __len__(self):
        """Returns length equal to the last last byte available/altered"""
        # https://docs.python.org/3/reference/datamodel.html#object.__len__
        length = self.fileSize
        if len(self._writeBuffer) != 0:
            lastKey = sorted(self._writeBuffer.keys())[-1]
            for i in range(self._blockSize - 1, -1, -1):
                if self._writeBuffer[lastKey][i] != None:
                    if lastKey + i + 1> length:
                        length = lastKey + i + 1
                    break
        
        for i in self._actionQueue:
            if (i[0] + 1 > length):
                length = i[0] + 1
        
        return length
    
    def __setitem__(self, index, value):
        """Write value at index to buffer"""
        # https://docs.python.org/3/reference/datamodel.html#object.__setitem__
        if not (isinstance(index, int)):
            raise TypeError
        if (value < 0) or (value > 255):
            raise ValueError
        if len(self._actionQueue) >= self._undoSize:
            poppedAction = self._actionQueue.pop(0)
            self.__pushWrite(poppedAction[0], poppedAction[1])
            self._actionQueue.append((index, value))
        else:
            self._actionQueue.append((index, value))
        
    def __pushWrite(self, index, value):
        """Write value at index to _writeBuffer"""
        #debug.debug("__pushWrite", index, value)
        if ((index // self._blockSize) * self._blockSize in self._writeBuffer.keys()):
            self._writeBuffer[(index // self._blockSize) * self._blockSize][index - ((index // self._blockSize) * self._blockSize)] = value
        else:
            self._writeBuffer[(index // self._blockSize) * self._blockSize] = [None for i in range(0, self._blockSize)]
            self._writeBuffer[(index // self._blockSize) * self._blockSize][index - ((index // self._blockSize) * self._blockSize)] = value
    
    def _cacheMiss(self, offset):
        """loads a block of the file into memeory"""
        #Assumes the block being added to the _readBuffer is not already in the _readBuffer
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
        
        Evicts furthest block from current block
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
        text = ""
        text += "Read:" + "{0:7.2f}".format(len(self._readBuffer) / self._bufferSize)
        text += "   Write:" + "{0:8}".format(len(self._writeBuffer) * self._blockSize) 
        text += "    Undo:" + "{0:7.2f}".format(len(self._actionQueue) / self._undoSize)
        return text
    
    def mask(self, key):
        """Returns bool signifying which bytes have been changed when stop == None
        Returns array of bool when stop != None"""
        result = False
        if (key // self._blockSize) * self._blockSize in self._writeBuffer.keys():
            if self._writeBuffer[(key // self._blockSize) * self._blockSize][key - (key // self._blockSize) * self._blockSize] != None:
                result = True
        for i in self._actionQueue:
            if (i[0] == key):
                result = True
        return result
    
    def close(self):
        """Closes buffer WITHOUT writing changes to file"""
        #remember to delete all the buffers
        del(self._actionQueue[:])
        del(self._redoStack[:])
        del(self._readBuffer)
        del(self._writeBuffer)
        self.file.close()
        
    def flush(self):
        """Writes buffer contents to file"""
        #TODO: if editied file is smaller then original, create a copy to resize
        for i in sorted(self._writeBuffer.keys()): #goes through _writeBuffer
            for j in range(0, self._blockSize):
                if self._writeBuffer[i][j] != None:
                    self.file.seek(i + j)
                    self.file.write(self._writeBuffer[i][j].to_bytes(1, sys.byteorder))
        
        for i in self._actionQueue: #goes through _actionQueue
            self.file.seek(i[0])
            if (i[1] == None):
                self.file.write((0).to_bytes(1, sys.byteorder))
            else:
                self.file.write((i[1]).to_bytes(1, sys.byteorder))
                
        self.file.flush()
        self.fileSize = self.file.seek(0, 2) #resets fileSize
        
        del(self._actionQueue[:])
        del(self._redoStack[:])
        for i in list(self._readBuffer.keys()):
            del(self._readBuffer[i])
        for i in list(self._writeBuffer.keys()):
            del(self._writeBuffer[i])
            
    def refresh(self):
        """refreshes all buffers without writing/updating file"""
        self.fileSize = self.file.seek(0, 2) #resets fileSize
        del(self._actionQueue[:])
        del(self._redoStack[:])
        for i in list(self._readBuffer.keys()):
            del(self._readBuffer[i])
        for i in list(self._writeBuffer.keys()):
            del(self._writeBuffer[i])

class window:
    """Handles printing and formating the interface"""
    #initilization code at end of class definition
    #keep to 39 characters in window width, in case displaying on different sized console windows
    
    def _sanityCheck():
        """varifies if variables have sane/acceptable values, raises appropriate errors"""
        if not isinstance(window.curser, int):
            raise TypeError("window.curser not int")
        if window.curser < 0:
            raise ValueError("window.curser not > 0")
        if not isinstance(window.screen, int):
            raise TypeError("window.screen not int")
        if window.screen < 0:
            raise ValueError("window.screen not > 0")
        if (window.screen % 16 != 0):
            raise ValueError("window.screen not multiple of 16")
        if not isinstance(window.halfbyte, bool):
            raise TypeError("window.halfbyte not bool")
        if buffer == None: 
            raise TypeError("buffer not initialized or missing") #TODO: is this the right error to raise
        if abs(window.screen - window.curser) > 256: #auto-sets screen to curser if curser is out of screen range
            window.screen = (window.curser // 16) * 16
        
    def interface():
        """Prints the interface window"""
        try:
            window._sanityCheck()
            text = ""
            text += window.header()
            text += window.body()
            text += window.footer()
            print(text, end="")
        except Exception as i:
            print("ERROR: Unable to print interface")
            traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    
    def _header():
        """Returns String representing the first 4 lines of interface window, newline terminated"""
        global filePath
        global fileSize
        global buffer
        
        text = ""
        text += "Py3HexEditLite " + version.ljust(8, " ") + "File:" + filePath[-52:].ljust(52," ") + "\n"
        
        text += "Buffers:  " + buffer.status() + "\n"
        
        if fileSize > 0:
            text += "Size: " + "{0:7.2f}".format(fileSize / int(1024 ** math.floor(math.log(fileSize, 1024)))) + " "
            try: #Just in case 2**10 years in the future, someone decides to open the entirety of the internet worth of a file in this hex editor...
                text += " KMGTPEZY?????????????????????"[int(math.floor(math.log(fileSize, 1024)))] + "B"
            except IndexError:
                text += "?B"
        else:
            text += "Size: " + "{0:7.2f}".format(fileSize)
            text += " B"
        
        text += "     Location:" + ("0x" + hex(window.curser)[2:].upper()).rjust(24, " ")
        text += "/" + ("0x" + hex(fileSize)[2:].upper()).rjust(24, " ")
        
        return text + "\n"
    
    def _body():
        """Returns String representing 16 lines where you can edit stuff, newline terminated"""
        global buffer
        
        text = ""
        line = ""
        
        temp = buffer[window.screen:window.screen + 256]
        for i in range(0, 16):
            line = hex(window.screen + i * 16)[2:][max(-(len(hex(window.screen + i * 16))), -11):].upper().rjust(11, " ")
            line += "|"
            for j in range(0, 16):
                if (j == 8): #prints column sperater at the 8 Byte mark
                    line += "|"
                
                if buffer.mask(window.screen + i * 16 + j): #prints indicator for changed byte
                    line += "*"
                else:
                    line += " "
                
                
                if ((window.curser == window.screen + i * 16 + j) and (mode == "HEX") and (window.halfbyte == False)): #large 4 bits
                    line += "-"
                elif (temp[i * 16 + j] == None):
                    line += "_"
                else:
                    line += hex(temp[i * 16 + j] // 16)[2:].upper()
                
                if ((window.curser == window.screen + i * 16 + j) and (mode == "HEX") and (window.halfbyte == True)): #small 4 bits
                    line += "-"
                elif (temp[i * 16 + j] == None):
                    line += "_"
                else:
                    line += hex(temp[i * 16 + j] % 16)[2:].upper()

            line += "| "
            for j in range(0, 16): #prints ASCII version of bytes
                if ((window.curser == window.screen + i * 16 + j) and (mode == "TEXT")):
                    line += "-"
                elif (temp[i * 16 + j] == None):
                    line += " "
                elif chr(temp[i * 16 + j]).isprintable():
                    line += chr(temp[i * 16 + j])
                else:
                    line += "."
            
            text += line + "\n"
        return text
    
    def _footer():
        """Returns String 4 lines max with any additional information needed, newline terminated"""
        global mode
        return "[" + mode + "]" + "\n"
    
    #gets around having to instatiate this class (thus easier to modify) by putting initilization code at the end of class definition
    curser = 0
    screen = 0 #in multiples of 16
    halfbyte = False    
    header = _header
    body = _body
    footer = _footer

#control functions, not inteneded to be directly accesable to the user
def _command():
    """prompts and execute commands within the current python3 environement"""
    #TODO: handle keyboard escape (IE: CTRL-C)
    compiledCode = None
    userCode = ""
    line = ""
    
    while True:
        line = input(">>>") #get first line in a multiline codeblock
        if line == "":
            break
        userCode += line

        try:
            compiledCode = code.compile_command(userCode) #if first line compiles, the codeblock was a one liner, skip to executing it
            while compiledCode == None: #get lines until codeblock compiles, syntax error is raised, or "" is entered
                line = input("...")
                if line == "":
                    userCode += "\n"
                else:
                    userCode += line
                compiledCode = code.compile_command(userCode)
        except Exception:
            compiledCode = None
            userCode = ""
            line = ""
            
            traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
            #traceback.print_last() #NOTE: will not work, raises an exception while printing an exception
                
        if compiledCode != None: # execute codeblock iff compiles, incase codeblock raises an error in compiliation resulting in compiledCode == None
            try:
                exec(compiledCode, globals())
            except Exception:
                traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
                #traceback.print_last() #NOTE: will not work, raises an exception while printing an exception
            finally:
                compiledCode = None
                userCode = ""
                line = ""
    
def _down(x = 16):
    """Move curser down, sets curser Location, adjusts screen location as needed"""
    move = (x // 16) * 16
    if (((window.curser + move)// 16) * 16 - window.screen) >= 256:
        window.screen = window.screen + move
    window.curser = window.curser + move
    
def _left():
    """Move curser left, sets curser Location, adjusts screen location as needed"""
    global mode
    
    oldCurser = window.curser
    if (mode == "HEX"):
        if window.halfbyte == False:
            moveAmount = 1
        else:
            moveAmount = 0
    elif (mode == "TEXT"):
        moveAmount = 1
    
    if (window.screen > window.curser - moveAmount):
        window.screen = max(0, window.screen - 16)
    window.curser = max(0, window.curser - moveAmount)
    
    if not ((oldCurser == 0) and (window.halfbyte == False)):
        window.halfbyte = not window.halfbyte
    
def _right():
    """Move curser right, sets curser Location, adjusts screen location as needed"""
    global mode
    
    if (mode == "HEX"):
        if window.halfbyte == True:
            moveAmount = 1
        else:
            moveAmount = 0
    elif (mode == "TEXT"):
        moveAmount = 1
    
    if (((window.curser + moveAmount)// 16) * 16 - window.screen) >= 256:
        window.screen = window.screen + 16
    window.curser = window.curser + moveAmount
    window.halfbyte = not window.halfbyte
    

def _up(x = 16):
    """Move curser up, sets curser Location, adjusts screen location as needed"""
    move = (x // 16) * 16
    if (window.screen > window.curser - move):
        window.screen = max(0, window.screen - move)
    if (window.curser >= move):
        window.curser = window.curser - move
    
def _write(halfbyte):
    """Write a single half-byte to the current curser Location, use only when in HEX mode"""
    number = int(halfbyte,16)
    if (window.halfbyte == False):
        if (buffer[window.curser] == None):
            buffer[window.curser] = 0
        buffer[window.curser] = number * 16 + (buffer[window.curser] % 16)
    elif (window.halfbyte == True):
        if (buffer[window.curser] == None):
            buffer[window.curser] = 0
        buffer[window.curser] = (buffer[window.curser] // 16) * 16 + number

''' API, accessable by user in 'COMMAND' mode
They return values for success, can print directly to the console, can raise errors (depending on how 'user friendly' vs 'part of a function' it's ment to be
'''
#keep these function names lowercase for usability

readme = """Py3HexEditLite.py quick help

Controls:
Arrow Keys    = Move Curser
"""

api = """A list of accessable variables/functions/etc in this program
Buffer:
window:

buffer

readme
api

goto(x)
newfile(path)
openfile(path)
save()
saveas(path)
quit()
"""

def goto(x):
    """Moves curser to x, adjusts screen location accordingly"""
    if (not (type(x) == int)):
        raise TypeError
    elif (x < 0):
        raise ValueError
    
    window.curser = x
    window.screen = int(x // 16) * 16
    return 0
    
def newfile(path):
    """Creates a new empty file"""
    global buffer
    if (type(path) != str):
        raise TypeError
    
    print("Attempting to open file: " + str(path))
    try:
        file = open(path, "x+b")
        file.close()
    except Exception as i:
        print("ERROR: Could not open file to write to: " + str(i))
        return -1

    openFile(path)
    goto(0)
    return 0

def openfile(path):
    """opens a file for editing"""
    # https://docs.python.org/3/library/os.path.html#os.path.isfile
    '''#some stuff on direct drive access
    # https://support.microsoft.com/en-ca/kb/100027
    # http://blog.lifeeth.in/2011/03/reading-raw-disks-with-python.html
    # http://stackoverflow.com/questions/6522644/how-to-open-disks-in-windows-and-read-data-at-low-level
    
    \\.\PhysicalDriveN  #Windows direct access on disk N
    \\.\X               #Windows direct access on drive X
    /dev/sdb            #Linux?
    '''
    global buffer
    global fileSize
    global filePath
    
    if (os.path.exists(path) == False):
        print("ERROR: path invalid")
        return -1   
    if os.path.islink(path):
        print("Attemtping to open a sumbolic link")    
    if os.path.isdir(path):
        #print("Attempting to open a directory")
        print("ERROR: path is a directory")
        return -1
    if (os.path.ismount(path) == True):
        print("Attempting to open a mount point")
    '''
    if (os.path.isfile(path) == False): #this does not allow opening a drive (as a block device)
        #raise IsADirectoryError
        print("ERROR: Path Not File")
        return -1
    '''
    
    tempBuffer = None
    try:
        tempBuffer = Buffer(path)
        fileSize = tempBuffer.fileSize #os.path.getsize(path) returns incorrect value when opening a drive (as a block device)
        filePath = path
        print("Successfully opened file: " + path)
    except PermissionError:
        print("ERROR: permission denied")
        return -1
    except Exception as i:
        print("ERROR: could not open file: " + str(i))
        return -1
    
    if (buffer != None) and (tempBuffer != None):
        print("Closing previously open file")
        buffer.close()
        buffer = tempBuffer
    else:
        #debug.debug("assinging tempbuffer to buffer")
        buffer = tempBuffer
    
    goto(0)
    return 0

def save():
    """Saves current changes to currently open file"""
    global buffer
    global fileSize
    
    buffer.flush()
    fileSize = buffer.fileSize
    return 0
    
def saveas(path):
    """Takes a string representing a file path. Creates and opens a new file, saves the current changes, closes the old file"""
    global buffer
    
    file = None
    try:
        file = open(path, "x+b")
    except Exception as i:
        print("ERROR: Could not open file to write to: " + str(i))
        return -1
    for i in range(0, len(buffer)):
        if buffer[i] == None:
            file.write((0).to_bytes(1, sys.byteorder))
        else:
            file.write((buffer[i]).to_bytes(1, sys.byteorder))
    file.close()
    
    buffer.close()
    buffer = None
    
    openFile(path)
    return 0

def quit():
    """Closes the current session"""
    global buffer
    
    print("Py3HexEditLite.py is quiting")
    buffer.close()
    exit(0)
    
''' #possible future API
def find(x):
    global buffer
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
    
    #globals
    mode = "HEX"
    buffer = None
    filePath = None
    fileSize = None
    
    #TODO: allow passing in more the one argument
    #TODO: document args
    if (len(sys.argv) >= 2):
        openFile(sys.argv[1])
    else:
        print("program has not been passed an argument, Opening interpriter")
        
    while (buffer == None):
        print("Please use openFile(\"filePath\") to open a file to edit")
        _command()
    
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
        elif (raw == "ENTER"):
            _command()
        elif (raw == "PAGEUP"):
            _up(256)
        elif (raw == "PAGEDOWN"):
            _down(256)
        elif (raw == "CTRL+S"):
            save()
        elif (raw == "CTRL+Q"):
            quit()        
        elif (len(raw) == 1): #single character input
            if (mode == "HEX") and ((chr(ord(raw)) in "1234567890abcdefABCDEF")):
                _write(raw)
                _right()
            elif (mode == "TEXT") and ((chr(ord(raw))).isprintable()):
                buffer[int(math.floor(window.curser))] = ord(raw)
                _right()
            if (chr(ord(raw)) == "\t"):
                if (mode == "HEX"):
                    mode = "TEXT"
                elif (mode == "TEXT"):
                    mode = "HEX"
        
        window.interface()
