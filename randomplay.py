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
    if ((field.structure != 2) and (field.wall != 1) and (field.mason == 0)):
        return True
    else:
        return False

def CanBreak(field):
    return (field.wall == 2)

def TypeJudge(p):
    if 3 < p < 8:
        return 1
    if 7 < p < 12:
        return 2
    if 11 < p < 16:
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
            if 3 < i < 8:
                if (CanEnter(field[x+move[i][0]][y+move[i][1]])) and (IsOutOfSize(x+move[i][0],y+move[i][1],size)==False):
                    p.append(i)
            if 7 < i < 12:
                print(field[x+move[i-8][0]][y+move[i-8][1]].wall,x+move[i-8][0],y+move[i-8][1])
                if (CanPlace(field[x+move[i-8][0]][y+move[i-8][1]])) and (IsOutOfSize(x+move[i-8][0],y+move[i-8][1],size)==False):
                    for _ in range(3):
                        p.append(i)
            if 11 < i < 16:
                if (CanBreak(field[x+move[i-12][0]][y+move[i-12][1]])) and (IsOutOfSize(x+move[i-12][0],y+move[i-12][1],size)==False):
                    return [i]
        except:
            continue
    print(p)
    a = random.choice(p)
    type = TypeJudge(a)
    print(a)
    if 3 < a < 8:
        dir = vec2dir(move[a][0],move[a][1])
        print(type,move[a][0],move[a][1])
    elif 7 < a < 12:
        dir = vec2dir(move[a-8][0],move[a-8][1])
        print(type,move[a-8][0],move[a-8][1])
    elif 11 < a < 16:
        dir = vec2dir(move[a-12][0],move[a-12][1])
    return type, dir

def superrandom():
    type=[1,2]
    dir=[1,2,3,4,5,6,7,8]
    k=random.choice(type)
    if k == 1:
        u=random.choice(dir)
    else:
        u=random.choice(dir[0:4])
    return k,u