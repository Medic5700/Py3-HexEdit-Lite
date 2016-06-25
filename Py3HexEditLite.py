import os

def getch():
    import msvcrt #windows specific operations
    return msvcrt.getch()

if __name__ == "__main__":
    file = None
    try:
        file = sys.argv[1]
    except:
        print("file has not been passed to argument")
        file = ""
        while (os.path.exists(file) == False):
            file = input("Enter a file path:")
    print("End Program, press key to continue")
    getch()
