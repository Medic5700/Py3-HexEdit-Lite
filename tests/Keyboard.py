'''This is used to test the Keyboard class during development.'''

class Keyboard:
    """A small class for handling AND parsing single character keyboard input"""
    #NOTE: Keeping this instatiated also keeps this class moduler
    env = None #The detected environment, either "W" for windows, or "L" for linux
    
    #This detects what input method would would work (windows or linux) based on what imports work/fail
    try:
        #Windows
        import msvcrt #windows specific operation
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
        self.specialKeys = {"CTRL+A"   :{"L":0x01        ,"W":0x01      },
                            "CTRL+B"   :{"L":0x02        ,"W":0x02      },
                            "CTRL+C"   :{"L":0x03        ,"W":0x03      },
                            "CTRL+D"   :{"L":0x04        ,"W":0x04      },
                            "CTRL+E"   :{"L":0x05        ,"W":0x05      },
                            "CTRL+F"   :{"L":0x06        ,"W":0x06      },
                            "CTRL+G"   :{"L":0x07        ,"W":0x07      },
                            #"CTRL+H"   :{"L":0x08        ,"W":0x08      }, #Same as BACKSPACE
                            #"CTRL+I"   :{"L":0x09        ,"W":0x09      }, #Same as \t
                            #"CTRL+J"   :{"L":0x0A        ,"W":0x0A      }, #same as \n
                            "CTRL+K"   :{"L":0x0B        ,"W":0x0B      },
                            "CTRL+L"   :{"L":0x0C        ,"W":0x0C      },
                            #"CTRL+M"   :{"L":0x0D        ,"W":0x0D      }, #This is the same as ENTER
                            "CTRL+N"   :{"L":0x0E        ,"W":0x0E      },
                            "CTRL+O"   :{"L":0x0F        ,"W":0x0F      },
                            "CTRL+P"   :{"L":0x10        ,"W":0x10      },
                            "CTRL+Q"   :{"L":0x11        ,"W":0x11      },
                            "CTRL+R"   :{"L":0x12        ,"W":0x12      },
                            "CTRL+S"   :{"L":0x13        ,"W":0x13      },
                            "CTRL+T"   :{"L":0x14        ,"W":0x14      },
                            "CTRL+U"   :{"L":0x15        ,"W":0x15      },
                            "CTRL+V"   :{"L":0x16        ,"W":0x16      },
                            "CTRL+W"   :{"L":0x17        ,"W":0x17      },
                            "CTRL+X"   :{"L":0x18        ,"W":0x18      },
                            "CTRL+Y"   :{"L":0x19        ,"W":0x19      },
                            "CTRL+Z"   :{"L":0x1A        ,"W":0x1A      },
                            "ENTER"    :{"L":0x0D        ,"W":0x0D      }, #This is the same as CTRL+M
                            "UP"       :{"L":0x1B5B41    ,"W":0xE048    },
                            "DOWN"     :{"L":0x1B5B42    ,"W":0xE050    },
                            "LEFT"     :{"L":0x1B5B44    ,"W":0xE04B    },
                            "RIGHT"    :{"L":0x1B5B43    ,"W":0xE04D    },
                            "CTRL+UP"  :{"L":0x1B5B313B3541,"W":0xE08D    }, #TOO LONG
                            "CTRL+DOWN":{"L":0x1B5B313B3542,"W":0xE091    }, #TOO LONG
                            "CTRL+LEFT":{"L":0x1B5B313B3544,"W":0xE073    }, #TOO LONG
                            "CTRL+RIGHT":{"L":0x1B5B313B5343,"W":0xE074    }, #TOO LONG                            
                            #"ESC"      :{"L":0x1B        ,"W":0x1B      } #problimatic since 0x1B is the linux escape character (I think?)
                            "DEL"      :{"L":0x1B5B33    ,"W":0xE053    }, #"L":0x1B5B337E
                            "PAGEUP"   :{"L":0x1B5B35    ,"W":0xE049    }, #"L":0x1B5B357E
                            "PAGEDOWN" :{"L":0x1B5B36    ,"W":0xE051    }, #"L":0x1B5B367E
                            "INSERT"   :{"L":0x1B5B32    ,"W":0xE052    }, #"L":0x1B5B327E
                            "HOME"     :{"L":0x1B5B48    ,"W":0xE047    },
                            "END"      :{"L":0x1B5B46    ,"W":0xE04F    },
                            "BACKSPACE":{"L":0x7F        ,"W":0x08      }, #Same as CTRL+H
                            #"F1"       :{"L": None       ,"W":0x003B    }, #F1 captured by ubuntu terminal
                            #"F2"       :{"L":0x1B4F51    ,"W":0x003C    },
                            #"F3"       :{"L":0x1B4F52    ,"W":0x003D    },
                            #"F4"       :{"L":0x1B4F53    ,"W":0x003E    },
                            #"F5"       :{"L":0x1B5B31357E,"W":0x003F    }, #TOO LONG
                            #"F6"       :{"L":0x1B5B31377E,"W":0x0040    }, #TOO LONG
                            #"F7"       :{"L":0x1B5B31387E,"W":0x0041    }, #TOO LONG
                            #"F8"       :{"L":0x1B5B31397E,"W":0x0042    }, #TOO LONG
                            #"F9"       :{"L":0x1B5B32307E,"W":0x0043    }, #TOO LONG
                            #"F10"      :{"L":0x1B5B32317E,"W":0x0044    }, #TOO LONG
                            #"F11"      :{"L": None       ,"W":0xE085    }, #F11 captured by ubuntu terminal
                            "F12"      :{"L":0x1B5B32347E,"W":0xE086    } #TOO LONG
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
    
    #start new code for overhaul
    def __BiggestByte(self, i):
        """takes a number, and returns the most significant BYTE"""
        while i > 255:
            i = i >> 8
        return i
    
    def __RemoveBiggestByte(self, i):
        """takes a number, returns number without most significant BYTE"""
        j = i
        k = 0
        while j > 255:
            j = j >> 8
            k = k + 8
        return (j << k) ^ i
    
    class node:
        def __init__(self, parent):
            self.parent = parent #only None for root
            self.children = None #a dictionary
            self.value = None #The key
            #iff value != None and chilfren != None then error
    
    def __insertCode(self, node, code, value):
        #is biggestByte of code in node.children? 
        #    true->recersive call with shifted code to child node
        #    false->create child node, recursive call with shifted code to child node
        #if code == 0 then value = value
        if code == 0:
            node.value = value
            return
        if node.children == None:
            node.children = {}
        if not(self.__BiggestByte(code) in list(node.children.keys())):
            node.children[self.__BiggestByte(code)] = self.node(node)
        self.__insertCode(node.children[self.__BiggestByte(code)], self.__RemoveBiggestByte(code), value)
        return
    
    def _constructSearchTree_test(self):
        """constructs a search tree, based on special keys
        IE: look up hex code in tree, iff leaf it's that character, iff it's another dictionary keep looking, iff Null then escape
        """
        self.keyTree = self.node(None)
        for i in list(self.specialKeys.keys()):
            self.__insertCode(self.keyTree, self.specialKeys[i][self.env], i)
            
    def getch_test(self):
        #just an initial test
        """pasrses keyboard input, returns a tuple such that (parsed character if applicable, single character if applicable, raw byte stream)
        EX: ('TAB', '\t', 0x09)
        """
        
        raw = self._getch()
        
if __name__ == "__main__":
    keyboard = Keyboard()
    print(keyboard.specialKeys)
    keyboard._constructSearchTree_test()
    print(keyboard.keyTree)
