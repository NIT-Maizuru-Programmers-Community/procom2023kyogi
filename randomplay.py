def randomplay(field,x,y):
    move=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
    p = []
    for i in range(8):
        try:
            if field[x+move[i][0]][y+move[i][1]].CanEnter(1):
                p.append(i)
        except:
            continue
    for j in range(8,12):
        try:
            if field[x+move[j-8][0]][y+move[j-8][1]].CanPlace(1):
                for _ in range(3):
                    p.append(j)
                flag = field[x][y].GetStructureColor()
                if flag == "gray":
                    p = [j]
                    return p

        except:
            continue
    for k in range(12,16):
        try:
            if field[x+move[k-12][0]][y+move[k-12][1]].CanBreak(1):
                for _ in range(5):
                    p.append(k)
        except:
            continue
    print(p)
    return p