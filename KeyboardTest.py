
def getch():
    import msvcrt #windows specific operations
    return msvcrt.getch()

# https://docs.python.org/3/library/readline.html#line-buffer

#while (True):
#    test = input("test:")
#    print(str(test))
while(True):
    temp = getch()
    print(str(temp))
    print(":" + str(ord(temp)))
