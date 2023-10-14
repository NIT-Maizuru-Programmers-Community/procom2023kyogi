def IsOutOfSize(x, y, Size):
    if (x < 0)|(Size <= x):
        return True
    if (y < 0)|(Size <= y):
        return True
    return False

def randomplay(field,x,y,size,temp):
    move=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
    p = []
    for i in range(4,8):
        try:
            if IsOutOfSize(x+move[i][0],y+move[i][1],size):
                continue
            if field[x+move[i][0]][y+move[i][1]].CanEnter(1):
                for _ in range(2):
                    p.append(i)
            #if (temp == 8) or (temp == 9) or (temp == 10) or (temp == 11):
                #for t in range(4,8):
                    #try:
                        #if IsOutOfSize(x+move[i][0],y+move[i][1],size):
                            #continue
                        #if field[x+move[i][0]][y+move[i][1]].CanEnter(1):
                         #   p.append(i)
                    #except:
                     #   continue
                #return p
        except:
            continue
    for j in range(8,12):
        try:
            if (IsOutOfSize(x+move[j-8][0],y+move[j-8][1],size)) or (field[x+move[j-8][0]][y+move[j-8][1]].isTerritoryA == True) or (field[x+move[j-8][0]][y+move[j-8][1]].CanPlace(1) == False) or j == temp:
                continue
            if (field[x+move[j-8][0]][y+move[j-8][1]].CanPlace(1) == True):
                for _ in range(4):
                    p.append(j)
        except:
            continue
    for k in range(12,16):
        if IsOutOfSize(x+move[k-12][0],y+move[k-12][1],size):
            continue
        try:
            if (field[x+move[k-12][0]][y+move[k-12][1]].CanBreak(1)):
                return [k] 
        except:
            continue
    print(p)
    return p