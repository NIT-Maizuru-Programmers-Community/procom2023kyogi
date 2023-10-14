def IsOutOfSize(x, y, Size):
    if (x < 0)|(Size <= x):
        return True
    if (y < 0)|(Size <= y):
        return True
    return False

def CanEnter(field):
    return ((field.structure != 1) and (field.wall != 2) and (field.mason == 0))

def CanPlace(field):
    return ((field.structure != 2) and (field.wall == 0) and (field.mason == 0) and (field.territory != 1))

def CanBreak(field):
    return (field.wall == 2)

def randomplay(field,x,y,size):
    move=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
    p = []
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
                    p.append(i)
        except:
            continue
    print(p)
    return p