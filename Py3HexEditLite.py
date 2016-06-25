import os

def getch():
    import msvcrt #windows specific operations
    return msvcrt.getch()


if __name__ == "__main__":
    filePath = None
    try:
        filePath = sys.argv[1]
    except:
        print("file has not been passed to argument")
        filePath = ""
        while (os.path.exists(filePath) == False):
            filePath = input("Enter a file path:")
    
    
    print("End Program, press key to continue")
    getch()
