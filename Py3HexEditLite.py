import os

version = "v0.1"

def getch():
    import msvcrt #windows specific operations
    return msvcrt.getch()

def _interface(data, curserLocation):
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
    text = "Py3HexEditLite v0.0                    File: ReadMe.txt                         " + "\n"
    text += "Size:50000Bytes   Buffer:0050/1000  Location:1234567890ABCDEF.8/1234567890ABCDEF" + "\n"
    for i in range(0,16):
        temp = hex(i)[2:].zfill(12) + "|"
        for j in range(0,8):
            if i*16+j >= len(data):
                temp += " __"
            else:
                temp += " " + hex(data[i*16+j])[2:].zfill(2)
        temp += "|"
        for j in range(8,16):
            if i*16+j >= len(data):
                temp += " __"
            else:
                temp += " " + hex(data[i*16+j])[2:].zfill(2)
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
    text += "Command Arg Arg Arg?"
    print(text)

class WriteBuffer:
    pass

class ReadBuffer:
    pass

def up(x):
    return max(0,x-16)
def down(x):
    return x+16
def left(x):
    return max(0,x-0.5)
def right(x):
    return x+0.5

if __name__ == "__main__":
    filePath = None
    try:
        filePath = sys.argv[1]
    except:
        print("file has not been passed to argument")
        filePath = ""
        while (os.path.exists(filePath) == False):
            filePath = input("Enter a file path:")
    
    curserLocation = 0.0 #A real, since in hex, a byte is represented as 2 hex chars
    screenLocation = 0 #in multiples of 16
    
    print("End Program, press key to continue")
    getch()