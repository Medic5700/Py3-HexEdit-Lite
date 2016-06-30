This program is a lightweight Hex Editor built in Python3, usable within the command line.
IE: Stop prepairing to hex edit, just hex edit

Status: Currently a usable prototype (IE: Alpha)

Running:
    Run Py3HexEditLite.py with Python3 #you can give a file name for an arg to open
    You can also enter a filename when you open it if no args were given
    Note: CTRL+C will not exit, use CTRL+A (a temporary placeholder)
Controls:
    Arrow keys   - move curser
    CTRL+A       - quit program (a temperary placeholder binding)
    CTRL+S       - save
    DEL          - deletes a byte
    A hex number - write a byte at curser location

Features:
    Open arbitrary sized files #should be able to
    Read/Write to/from files

Interface: This is what it looks like
Py3HexEditLite v0.3    File:ReadMe.txt
Size:  715.00  B Buffer:XXX%|XXX% Location:               0x0/             0x2CB
000000000000| -4 68 69 73 20 70 72 6F| 67 72 61 6D 20 69 73 20| This program is
000000000010| 61 20 6C 69 67 68 74 77| 65 69 67 68 74 20 48 65| a lightweight He
000000000020| 78 20 45 64 69 74 6F 72| 20 62 75 69 6C 74 20 69| x Editor built i
000000000030| 6E 20 50 79 74 68 6F 6E| 33 2C 20 75 73 61 62 6C| n Python3, usabl
000000000040| 65 20 77 69 74 68 69 6E| 20 74 68 65 20 63 6F 6D| e within the com
000000000050| 6D 61 6E 64 20 6C 69 6E| 65 2E 0D 0A 49 45 3A 20| mand line...IE:
000000000060| 53 74 6F 70 20 70 72 65| 70 61 69 72 69 6E 67 20| Stop prepairing
000000000070| 74 6F 20 68 65 78 20 65| 64 69 74 2C 20 6A 75 73| to hex edit, jus
000000000080| 74 20 68 65 78 20 65 64| 69 74 0D 0A 0D 0A 53 74| t hex edit....St
000000000090| 61 74 75 73 3A 20 43 75| 72 72 65 6E 74 6C 79 20| atus: Currently
0000000000A0| 61 20 75 73 61 62 6C 65| 20 70 72 6F 74 6F 74 79| a usable prototy
0000000000B0| 70 65 20 28 49 45 3A 20| 41 6C 70 68 61 29 0D 0A| pe (IE: Alpha)..
0000000000C0| 0D 0A 55 73 69 6E 67 3A| 0D 0A 20 20 20 20 52 75| ..Using:..    Ru
0000000000D0| 6E 20 50 79 33 48 65 78| 45 64 69 74 4C 69 74 65| n Py3HexEditLite
0000000000E0| 2E 70 79 20 77 69 74 68| 20 50 79 74 68 6F 6E 33| .py with Python3
0000000000F0| 20 23 79 6F 75 20 63 61| 6E 20 67 69 76 65 20 61|  #you can give a
[Hex]
