def vec2dir(x,y):
    if (x,y) == (-1,1):
        return 1
    if (x,y) == (0,1):
        return 2
    if (x,y) == (1,1):
        return 3
    if (x,y) == (1,0):
        return 4
    if (x,y) == (1,-1):
        return 5
    if (x,y) == (0,-1):
        return 6
    if (x,y) == (-1,-1):
        return 7
    if (x,y) == (-1,0):
        return 8
    else:
        return 0
    
def method2act():
    return 0