import os
import math

version = "v0.1"

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

def getch():
    global debug
    if (env == "WIN"):
        return msvcrt.getch()
    if (env == "UNIX"):
        terminalFD = sys.stdin.fileno()
        oldSetting = termios.tcgetattr(terminalFD)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        except:
            debug.debug("Error reading input")
        finally:
            termios.tcsetattr(terminalFD, termios.TCSADRAIN, oldSetting)
        return ch

def _interface(data, curserLocation, screenLocation):
    """Prints file name, size of file, buffer status, and the hex editing interface"""
    #test interface
    text = "Py3HexEditLite " + version.ljust(8, " ") + "File:" + filePath.ljust(52," ") + "\n"
    text += "Size:" + str(fileSize).rjust(8," ") + " B   Buffer:XXX%|XXX%  Location:" + hex(math.floor(curserLocation))[2:].upper().rjust(16, " ") + "."
    if (math.floor(curserLocation) == curserLocation): #adds the hex decimal location, May have to correct for endienness
        text += "0"
    else:
        text += "8"
    text += "/" + hex(fileSize)[2:].upper().rjust(16, " ") + "\n"
    for i in range(screenLocation//16,screenLocation//16 + 16): #TODO: this is a shortcut, fix it
        temp = hex(i*16)[2:].zfill(12) + "|"
        for j in range(0,8):
            temp += " "
            if (curserLocation == i*16+j): #large 4 bits
                temp += "-"
            elif (len(data) <= i*16+j):
                temp += "_"
            else:
                temp += hex(data[i*16+j] // 16)[2:]
            
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

class WriteBuffer:
    pass

class ReadBuffer:
    pass

def up(x,y):
    if (y > x - 16):
        temp = max(0, y - 16)
    else:
        temp = y
    if (x < 16):
        temp2 = x
    else:
        temp2 = x - 16
    return temp2, temp
def down(x,y):
    if (((x + 16)// 16) * 16 - y) >= 256:
        temp = y + 16
    else:
        temp = y        
    return x+16, temp
def left(x,y):
    if (y > x - 0.5):
        temp = max(0, y - 16)
    else:
        temp = y    
    return max(0,x-0.5), temp
def right(x,y):
    if (((x + 0.5)// 16) * 16 - y) >= 256:
        temp = y + 16
    else:
        temp = y
    return x+0.5, temp

def save():
    pass

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
                            "DEL"     :{"L":0x1B5B33  ,"W":0xE053    } #"L" should be 0x1B5B337E, but I'll ignore the 4th chr for simplicity
                            #"ESC"     :{"L":0x1B      ,"W":0x1B      } #problimatic since 0x1B is the linux escape character (I think?)
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


if __name__ == "__main__":
    debug = Debug(True)
    print("Starting Py3HexEditLite.py")
    debug.debug("START PROGRAM================================================")

    filePath = None
    try:
        filePath = sys.argv[1]
    except:
        print("file has not been passed to argument")
        filePath = ""
        while (os.path.exists(filePath) == False):
            filePath = input("Enter a file path:")
        
    print("Py3HexEditLite " + version + " has started")
    print("Attempting to Open file: " + filePath)
    
    file = open(filePath,'rb')
    data = file.read()
    
    fileSize = os.path.getsize(filePath)
    fileName = filePath #TODO:include file name, excluding the path
    curserLocation = 0.0 #A real, since in hex, a byte is represented as 2 hex chars
    screenLocation = 0 #in multiples of 16
    mode = "Hex"
    
    _interface(data, curserLocation, screenLocation)
    
    keyboard = Keyboard()
    #Keyboard input
    while (True):
        raw = keyboard.getch()
        if (raw == "UP"):
            curserLocation, screenLocation = up(curserLocation, screenLocation)
        elif (raw == "DOWN"):
            curserLocation, screenLocation = down(curserLocation, screenLocation)
        elif (raw == "LEFT"):
            curserLocation, screenLocation = left(curserLocation, screenLocation)
        elif (raw == "RIGHT"):
            curserLocation, screenLocation = right(curserLocation, screenLocation)
        elif (raw == "CTRL+Q"):
            if (mode == "Hex"):
                mode = "Text"
            elif (mode == "Text"):
                mode = "Hex"
            else:
                mode = "Hex"            
        elif (raw == "CTRL+E"):
            mode = "Input"
        #elif (chr(temp) in "1234567890abcdefABCDEF"):
        #    pass
        
        _interface(data, curserLocation, screenLocation)
