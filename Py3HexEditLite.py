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
    import msvcrt #windows specific operations
    return msvcrt.getch()

def _interface(data, curserLocation, screenLocation):
    """Prints file name, size of file, buffer status, and the hex editing interface"""
    #test interface
    prototype = """
Py3HexEditLite v0.0                    File: ReadMe.txt                         
Size:50000Bytes   Buffer:0050/1000  Location:1234567890ABCDEF.8/1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF FF FF FF FF| 1234567890ABCDEF
1234567890AB| FF FF FF FF FF FF FF FF| FF FF FF FF*FF*FF*FF*FF| 1234567890ABCDEF
1234567890AB| FF FF __ __ __ __ __ __| __ __ __ __ __ __ __ __| 12
Command Arg Arg Arg?
    """
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
    if (x <= 16):
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

if __name__ == "__main__":
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
    #import curses
    '''
    up = 224+72
    down = 224+80
    left = 224+75
    right = 224+77
    '''
    #getch()
    
    while True:
        temp = ord(getch())
        if (temp == 224):
            temp2 = ord(getch())
            if (temp2 == 72):
                curserLocation, screenLocation = up(curserLocation, screenLocation)
            if (temp2 == 80):
                curserLocation, screenLocation = down(curserLocation, screenLocation)
            if (temp2 == 75):
                curserLocation, screenLocation = left(curserLocation, screenLocation)
            if (temp2 == 77):
                curserLocation, screenLocation = right(curserLocation, screenLocation)
            print(temp2)
        print(temp)
        _interface(data, curserLocation, screenLocation)
        
