This program is a lightweight Hex Editor built in Python3, usable within the command line.
Designed to be robust and simple to start using on the spot (assuming you have python3 installed), and to have as few dependencies as possible. Also features a COMMAND mode (access to the python interpreter) allowing for customizability and quick scripting.
Status: Currently usable, still WIP

Running:
    Download and run Py3HexEditLite.py with Python3 #you can give a filepath as an arg to open
    You can also enter a filename when you open it if no args were given #path is relative to where Py3HexEditLite.py is located
    Note: use CTRL+Q in HEX mode or quit() in COMMAND mode to exit

Controls:
    Arrow keys   - move curser
    CTRL+Q       - quit program
    CTRL+S       - save
    CTRL+Z       - undo
    CTRL+Y       - redo
    TAB          - switch between editing in HEX mode and TEXT mode
    A hex number - write a byte at curser location
    ENTER        - enter python command(s)

Commands:
    quit()
    openFile(filepath)
    goto(offset)
    saveAs(filepath)
    save()
    newFile(filepath)

Features:
    Supports large files (WIP)
    Read/Edit a file in HEX or TEXT mode
    
Dependencies:
    Python3.5 (built in python 3.5.2)
    
Interface: 
This is what the interface looks like

Py3HexEditLite v0.5    File:ReadMe.txt
Buffers:  Read:0   Write:0    Undo:0
Size:    2.55 KB     Location:                     0x0/                   0xA33
          0| -4 68 69 73 20 70 72 6F| 67 72 61 6D 20 69 73 20| This program is
         10| 61 20 6C 69 67 68 74 77| 65 69 67 68 74 20 48 65| a lightweight He
         20| 78 20 45 64 69 74 6F 72| 20 62 75 69 6C 74 20 69| x Editor built i
         30| 6E 20 50 79 74 68 6F 6E| 33 2C 20 75 73 61 62 6C| n Python3, usabl
         40| 65 20 77 69 74 68 69 6E| 20 74 68 65 20 63 6F 6D| e within the com
         50| 6D 61 6E 64 20 6C 69 6E| 65 2E 0D 0A 44 65 73 69| mand line...Desi
         60| 67 6E 65 64 20 74 6F 20| 62 65 20 73 69 6D 70 6C| gned to be simpl
         70| 65 20 74 6F 20 73 74 61| 72 74 20 75 73 69 6E 67| e to start using
         80| 20 6F 6E 20 74 68 65 20| 73 70 6F 74 20 28 61 73|  on the spot (as
         90| 73 75 6D 69 6E 67 20 79| 6F 75 20 68 61 76 65 20| suming you have
         A0| 70 79 74 68 6F 6E 33 20| 69 6E 73 74 61 6C 6C 65| python3 installe
         B0| 64 29 2C 20 61 6E 64 20| 74 6F 20 68 61 76 65 20| d), and to have
         C0| 61 73 20 66 65 77 20 64| 65 70 65 6E 64 65 6E 63| as few dependenc
         D0| 69 65 73 20 61 73 20 70| 6F 73 73 69 62 6C 65 2E| ies as possible.
         E0| 0D 0A 53 74 61 74 75 73| 3A 20 43 75 72 72 65 6E| ..Status: Curren
         F0| 74 6C 79 20 61 20 75 73| 61 62 6C 65 20 70 72 6F| tly a usable pro
[HEX]
