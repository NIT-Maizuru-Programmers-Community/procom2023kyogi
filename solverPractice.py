import math
import numpy as np
from matplotlib import pyplot as plt
import copy
import csv
from enum import Enum
import json
import alphabeta

#-1,0,1の範囲に正規化
def Normalize(n):
    return max(-1, min(n, 1))

#マップ範囲外ならTrue
def IsOutOfSize(x, y):
    if (x < 0)|(Size <= x):
        return True
    if (y < 0)|(Size <= y):
        return True
    return False

class Team(Enum):
    NONE=0
    A=1
    B=2

class Structure(Enum):
    PLANE=0
    POOL=1
    CASTLE=2

class Mason:
    x=0
    y=0
    team = Team(0)
    teamID = 0
    move=[]

    #初期化
    def __init__(self, team, x ,y, teamID):
        self.x = x
        self.y = y
        self.team = team
        self.teamID = teamID
        self.move=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
    
    #毎ターンの行動
    def Act(self,cond):
        if -1<cond<8:
            self.Move(self.move[cond][0], self.move[cond][1])
        elif 7<cond<12:
            self.Place(self.move[cond-8][0], self.move[cond-8][1])
        elif 11<cond<16:
            self.Break(self.move[cond-12][0], self.move[cond-12][1])

    #相対座標x,yに城壁設置
    def Place(self,x,y):
        if (x != 0)&(y != 0):
            return False
        x = Normalize(x)
        y = Normalize(y)
        rX = self.x+x
        rY = self.y+y
        if IsOutOfSize(rX, rY):
            return
        if not Cells[rX][rY].CanPlace(self.team):
            return
        Cells[rX][rY].Place(self.team)
    
    #相対座標x,yの城壁破壊
    def Break(self,x,y):
        if (x != 0)&(y != 0):
            return False
        x = Normalize(x)
        y = Normalize(y)
        rX = self.x+x
        rY = self.y+y
        if IsOutOfSize(rX, rY):
            return
        Cells[rX][rY].Break()
    
    #相対座標x,yに移動
    def Move(self,x,y):
        x = Normalize(x)
        y = Normalize(y)
        rX = self.x+x
        rY = self.y+y
        if IsOutOfSize(rX, rY):
            return
        if not Cells[rX][rY].CanEnter(self.team):
            return
        Cells[rX][rY].Enter(self.team, self.teamID)
        Cells[self.x][self.y].Exit()
    
    #何もしない
    def Skip():
        return

class Cell:
    x=0
    y=0
    structure = Structure(0)
    wall = Team(0)
    mason = Mason(Team.NONE, 0, 0, 0)
    __nextMason = Team(0)
    __nextMasonID = 0

    #初期化。ここ以外でIDは用いない
    def __init__(self, x, y, structures, masons):
        self.x = x
        self.y = y
        if structures == 1:
            self.structure = Structure(1)
        elif structures == 2:
            self.structure = Structure(2)
        if masons > 0:
            self.mason = Mason(Team.A, x ,y, masons)
        elif masons < 0:
            self.mason = Mason(Team.B, x, y, masons)

    #上に乗ることが出来るか
    def CanEnter(self, team):
        if self.structure == Structure.POOL:
            return False
        if (team == Team.A)&(self.wall == Team.B):
            return False
        if (team == Team.B)&(self.wall == Team.A):
            return False
        if self.mason.team != Team.NONE:
            return False
        return True
    
    #上に城壁を設置出来るか
    def CanPlace(self, team):
        if self.structure == Structure.CASTLE:
            return False
        if self.wall != Team.NONE:
            return False
        if (team == Team.A)&(self.mason.team == Team.B):
            return False
        if (team == Team.B)&(self.mason.team == Team.A):
            return False
        return True
    
    #破壊できるか
    def CanBreak(self, team):
        if (team == Team.A)&(self.wall == Team.B):
            return True
        if (team == Team.B)&(self.wall == Team.A):
            return True
        return False

    #対応する色を返す(グラフ描画用)
    def GetStructureColor(self):
        if self.structure == Structure.POOL:
            return "lightgreen"
        elif self.structure == Structure.CASTLE:
            return "gray"
        else:
            return "white"
    def GetWallColor(self):
        if self.wall == Team.A:
            return "pink"
        elif self.wall == Team.B:
            return "lightblue"
        else:
            return "clear"
    def GetMasonColor(self):
        if self.mason.team == Team.A:
            return "red"
        elif self.mason.team == Team.B:
            return "blue"
        else:
            return "clear"
    
    #毎ターン実行される
    def Act(self, p):
        if self.mason.team == Team.NONE:
            return
        if self.mason.team == Team.B:
            return
        temp = self.mason.teamID
        for _ in range(temp-1):
            p /= 16
        c = int(p % 16)
        self.mason.Act(c)

    #Actのfor文が一旦終わった後実行される
    def LateAct(self):
        if self.__nextMason == Team.NONE:
            return
        self.mason = Mason(self.__nextMason, self.x, self.y, self.__nextMasonID)
        self.__nextMason = Team(0)
        self.__nextMasonID = 0

    #自身に城壁設置
    def Place(self, team):
        self.wall = team

    #自身の城壁破壊
    def Break(self):
        self.wall = Team.NONE

    #職人が入ってくる
    def Enter(self, team, masonID):
        self.__nextMason = team
        self.__nextMasonID = masonID

    #職人が出ていく
    def Exit(self):
        self.mason = Mason(Team.NONE, 0, 0, 0)

def CopyCells():
    copied = []
    for x in range(0, Size):
        subCopied = []
        for y in range(0, Size):
            cellCopied = Cell
            cellCopied.x=x
            cellCopied.y=y
            cellCopied.structure = Cells[x][y].structure
            cellCopied.wall = Cells[x][y].wall
            cellCopied.mason = Mason(Cells[x][y].mason.team, x, y, Cells[x][y].mason.teamID)
            subCopied.append(cellCopied)
        copied.append(subCopied)
    return copied

#jsonからマップ読み込み
Cells = []
Size = 0
CurrentTurn = 0
TeamMasonCount = 0
with open(r'C:\procom\kyogi\procom2023\server\sample.conf.txt', encoding="utf-8") as f:
    load = json.load(f)
    l = load["match"]["board"]
    Size = len(l["structures"])
    TeamMasonCount = l["mason"]
    for x in range(0, Size):
        subCells = []
        for y in range(0, Size):
            cell = Cell(x,y,l["structures"][x][y],l["masons"][x][y])
            subCells.append(cell)
        Cells.append(subCells)

field = copy.deepcopy(Cells)
G=alphabeta.Game(Size, Size, TeamMasonCount,field,Team)
myMa=[]
myMacoor=[]
tekiMa=[]
tekiMacoor=[]
for i in range(Size):
    for j in range(Size):
        if Cells[i][j].mason.team == Team.A:
            myMacoor.append([i,j])
        elif Cells[i][j].mason.team == Team.B:
            tekiMacoor.append([i,j])
for i in range(TeamMasonCount):
    myMa.append(Mason(1,myMacoor[i][0],myMacoor[i][1],i))
    tekiMa.append(Mason(2,tekiMacoor[i][0],tekiMacoor[i][1],i))

#pyplotの画面を閉じる度に実行
while(1):
    CurrentTurn += 1
    plt.cla
    for x in range(0, Size):
        for y in range(0, Size):
            plt.plot(x, y, marker='s', markersize=20, c=Cells[x][y].GetStructureColor())
            if Cells[x][y].GetWallColor() != "clear":
                plt.plot(x, y, marker='s', markersize=15, c=Cells[x][y].GetWallColor())
            if Cells[x][y].GetMasonColor() != "clear":
                plt.plot(x, y, marker='s', markersize=10, c=Cells[x][y].GetMasonColor())
    plt.axis('square')
    plt.show()
    p = alphabeta.evaluator(G,CurrentTurn,TeamMasonCount,myMa,tekiMa)
    print(p,CurrentTurn)
    for x in range(0, Size):
        for y in range(0, Size):
            Cells[x][y].Act(p)
    for x in range(0, Size):
        for y in range(0, Size):
            Cells[x][y].LateAct()