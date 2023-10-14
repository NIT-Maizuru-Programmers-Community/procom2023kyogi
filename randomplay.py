import random

def IsOutOfSize(x, y, Size):
    if (x < 0)|(Size <= x):
        return True
    if (y < 0)|(Size <= y):
        return True
    return False

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

def CanEnter(field):
    return ((field.structure != 1) and (field.wall != 2) and (field.mason == 0))

def CanPlace(field):
    return ((field.structure != 2) and (field.wall == 0) and (field.mason == 0) and (field.territory != 1))

def CanBreak(field):
    return (field.wall == 2)

def TypeJudge(p):
    if 3 < p < 8:
        return 1
    if 8 < p < 12:
        return 2
    if 12 < p < 16:
        return 3
    
def OnCastle(field):
    return (field.structure == 2)

def randomplay(field,x,y,size):
    move=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
    p = []
    a = 0
    type = 0
    dir = 0
    for i in range(4,16):
        try:
            if IsOutOfSize(x+move[i][0],y+move[i][1],size):
                continue
            if 3 < i < 8:
                if (CanEnter(field[x+move[i][0]][y+move[i][1]])):
                    p.append(i)
            if 8 < i < 12:
                if (CanPlace(field[x+move[i][0]][y+move[i][1]])):
                    for _ in range(3):
                        p.append(i)
            if 12 < i < 16:
                if (CanBreak(field[x+move[i][0]][y+move[i][1]])):
                    return [i]
        except:
            continue
    print(p)
    a = random.choice(p)
    type = TypeJudge(a)
    dir = vec2dir([x+move[i][0]],[y+move[i][1]])
    return type , dir