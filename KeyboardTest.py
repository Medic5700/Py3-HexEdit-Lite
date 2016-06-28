#!/usr/bin/env python3
'''A quick script to test/develop keyboard inputs'''

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

# https://docs.python.org/3/library/readline.html#line-buffer

if __name__ == "__main__":
    env = None
    try:
        import tty #linux specific operations
        import sys
        import termios #linux specific operations
        env = "UNIX"
    except:
        print("Machine is not Unix")
    try:
        import msvcrt #windows specific operations
        env = "WIN"
    except:
        print("Machine is not Windows")
    print(env)

    #while (True):
    #    test = input("test:")
    #    print(str(test))
    i = 20
    while(i>0):
        i -= 1
        temp = getch()
        print(str(temp))
        print(":" + str(ord(temp)))
