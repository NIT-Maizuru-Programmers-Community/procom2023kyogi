import math
import numpy as np
from matplotlib import pyplot as plt
import csv
from enum import Enum

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

class Field(Enum):
    PLANE=0
    POOL=1
    CASTLE=2

class Agent:
    x=0
    y=0
    team = Team(0)

    #初期化
    def __init__(self, team, x ,y):
        self.x = x
        self.y = y
        self.team = team
    
    #毎ターンの行動
    def Act(self):
        self.Move(-1,0)

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
        Cells[rX][rY].Enter(self.team)
        Cells[self.x][self.y].Exit()
    
    #何もしない
    def Skip():
        return

class Cell:
    x=0
    y=0
    field = Field(0)
    wall = Team(0)
    agent = Agent(Team.NONE, 0, 0)
    nextAgent = Team(0)

    #初期化。ここ以外でIDは用いない
    def __init__(self, x, y, ID):
        self.x = x
        self.y = y
        if ID == "1":
            self.field = Field(1)
        elif ID == "2":
            self.field = Field(2)
        elif ID == "a":
            self.agent = Agent(Team.A, x ,y)
        elif ID == "b":
            self.agent = Agent(Team.B, x, y)

    #上に乗ることが出来るか
    def CanEnter(self, team):
        if self.field == Field.POOL:
            return False
        if (team == Team.A)&(self.wall == Team.B):
            return False
        if (team == Team.B)&(self.wall == Team.A):
            return False
        if self.agent.team != Team.NONE:
            return False
        return True
    
    #上に城壁を設置出来るか
    def CanPlace(self, team):
        if self.field == Field.CASTLE:
            return False
        if self.wall != Team.NONE:
            return False
        if (team == Team.A)&(self.agent.team == Team.B):
            return False
        if (team == Team.B)&(self.agent.team == Team.A):
            return False
        return True
    
    #対応する色を返す(グラフ描画用)
    def GetFieldColor(self):
        if self.field == Field.POOL:
            return "lightgreen"
        elif self.field == Field.CASTLE:
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
    def GetAgentColor(self):
        if self.agent.team == Team.A:
            return "red"
        elif self.agent.team == Team.B:
            return "blue"
        else:
            return "clear"
    
    #毎ターン実行される
    def Act(self):
        if self.agent.team == Team.NONE:
            return
        self.agent.Act()

    #Actのfor文が一旦終わった後実行される
    def LateAct(self):
        if self.nextAgent == Team.NONE:
            return
        self.agent = Agent(self.nextAgent, self.x, self.y)
        self.nextAgent = Team(0)

    #自身に城壁設置
    def Place(self, team):
        self.wall = team

    #自身の城壁破壊
    def Break(self):
        self.wall = Team.NONE

    #職人が入ってくる
    def Enter(self, team):
        self.nextAgent = team

    #職人が出ていく
    def Exit(self):
        self.agent = Agent(Team.NONE, 0, 0)

#CSVからマップ読み込み
Cells = []
Size = 0
CurrentTurn = 0
with open('A11.csv') as f:
    reader = csv.reader(f)
    l = [row for row in reader]
    Size = len(l)
    for x in range(0, Size):
        subCells = []
        for y in range(0, Size):
            cell = Cell(x,y,l[x][y])
            subCells.append(cell)
        Cells.append(subCells)
#pyplotの画面を閉じる度に実行
while(1):
    CurrentTurn += 1
    plt.cla
    for x in range(0, Size):
        for y in range(0, Size):
            plt.plot(x, y, marker='s', markersize=20, c=Cells[x][y].GetFieldColor())
            if Cells[x][y].GetWallColor() != "clear":
                plt.plot(x, y, marker='s', markersize=15, c=Cells[x][y].GetWallColor())
            if Cells[x][y].GetAgentColor() != "clear":
                plt.plot(x, y, marker='s', markersize=10, c=Cells[x][y].GetAgentColor())
    plt.axis('square')
    plt.show()
    for x in range(0, Size):
        for y in range(0, Size):
            Cells[x][y].Act()
    for x in range(0, Size):
        for y in range(0, Size):
            Cells[x][y].LateAct()