env = None
try:
    import tty #linux specific operations
    import termios #linux specific operations
    import sys
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
    
if __name__ == "__main__":
    #To help figure out the keymappings to Windows and Linux
    print("input 20 characters")
    i = 20
    while(i>0):
        i -= 1
        temp = getch()
        print(str(temp))
        print(":" + str(ord(temp)))
        print(str(hex(ord(temp))))
