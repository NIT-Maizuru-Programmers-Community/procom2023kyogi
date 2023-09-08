import itertools
import numpy as np

terminal1 = [[0,1],[5,7],[9,2]]
terminal2 = [[10,8],[7,9]]
wall1 = [[0,1],[1,1],[2,1],[3,2],[4,3],[5,4],[5,5],[5,6],[5,7],[6,3],[7,2],[8,2],[9,2]]
wall2 = [[10,8],[9,8],[8,8],[7,8],[7,9]]

Terminals = [terminal1,terminal2]
Walls = [wall1, wall2]

Size = 11

class Wall:
    id=0
    def __init__(self, id):
        self.id=id
    def wall(self):
        return Walls[self.id]
    def terminal(self):
        return Terminals[self.id]
    def area(self):
        areas = []
        #壁の端2つの全組み合わせで試行
        for pos in itertools.combinations(self.terminal(), 2):
            #補完線の折れ曲がる座標を計算
            pos1 = pos[0]
            pos2 = pos[1]
            diff = [abs(pos2[0] - pos1[0]), abs(pos2[1] - pos1[1])]
            if diff[0] > diff[1]:
                if pos2[0] > pos1[0]:
                    sign = 1
                else:
                    sign = -1
                edge1 = [pos1[0] + sign * (diff[0] - diff[1]), pos1[1]]
                edge2 = [pos2[0] - sign * (diff[0] - diff[1]), pos2[1]]
            else:
                if pos2[1] > pos1[1]:
                    sign = 1
                else:
                    sign = -1
                edge1 = [pos1[0], pos1[1] + sign * (diff[1] - diff[0])]
                edge2 = [pos2[0], pos2[1] - sign * (diff[1] - diff[0])]
            #補完線を計算
            if diff[0] > diff[1]:
                fixedWall1 = self.wall().copy()
                for wallPos in range(pos1[0], edge1[0], 1 if pos1[0]<edge1[0] else -1):
                    fixedWall1.append([wallPos,pos1[1]])
                for wallPosX, wallPosY in zip(range(edge1[0], pos2[0], 1 if edge1[0]<pos2[0] else -1),range(edge1[1], pos2[1], 1 if edge1[0]<pos2[0] else -1)):
                    fixedWall1.append([wallPosX,wallPosY])
                fixedWall2 = self.wall().copy()
                for wallPos in range(pos2[0], edge2[0], 1 if pos2[0]<edge2[0] else -1):
                    fixedWall2.append([wallPos,pos2[1]])
                for wallPosX, wallPosY in zip(range(edge2[0], pos1[0], 1 if edge2[0]<pos1[0] else -1),range(edge2[1], pos1[1], 1 if edge2[0]<pos1[0] else -1)):
                    fixedWall2.append([wallPosX,wallPosY])
            else:
                fixedWall1 = self.wall().copy()
                for wallPos in range(pos1[1], edge1[1], 1 if pos1[1]<edge1[1] else -1):
                    fixedWall1.append([pos1[0],wallPos])
                for wallPosX, wallPosY in zip(range(edge1[0], pos2[0], 1 if edge1[0]<pos2[0] else -1),range(edge1[1], pos2[1], 1 if edge1[1]<pos2[1] else -1)):
                    fixedWall1.append([wallPosX,wallPosY])
                fixedWall2 = self.wall().copy()
                for wallPos in range(pos2[1], edge2[1], 1 if pos2[1]<edge2[1] else -1):
                    fixedWall2.append([pos2[0],wallPos])
                for wallPosX, wallPosY in zip(range(edge2[0], pos1[0], 1 if edge2[0]<pos1[0] else -1),range(edge2[1], pos1[1], 1 if edge2[1]<pos1[1] else -1)):
                    fixedWall2.append([wallPosX,wallPosY])
            #面積を算出
            area = [0,0]
            for time in [0,1]:
                checkerCell = []

                class CheckerCell:
                    x = 0
                    y = 0
                    chunkID = 0
                    wall = False
                    def __init__(self, x, y, wall):
                        self.x=x
                        self.y=y
                        self.wall = wall

                    def CanRegist(self):
                        return (self.chunkID == 0)&(self.wall == False)

                    def Regist(self, ID, nextCells):
                        self.chunkID = ID
                        if (self.x - 1 >= 0):
                            if (checkerCell[self.x - 1][self.y].CanRegist()):
                                if [self.x - 1, self.y] in nextCells:
                                    return
                                nextCells.append([self.x - 1, self.y])
                        if (self.x + 1 < Size):
                            if (checkerCell[self.x + 1][self.y].CanRegist()):
                                if [self.x + 1, self.y] in nextCells:
                                    return
                                nextCells.append([self.x + 1, self.y])
                        if (self.y - 1 >= 0):
                            if (checkerCell[self.x][self.y - 1].CanRegist()):
                                if [self.x, self.y - 1] in nextCells:
                                    return
                                nextCells.append([self.x, self.y - 1])
                        if (self.y + 1 < Size):
                            if (checkerCell[self.x][self.y + 1].CanRegist()):
                                if [self.x, self.y + 1] in nextCells:
                                    return
                                nextCells.append([self.x, self.y + 1])

                #壁の有無を記したマップを作成
                for x in range(0,Size,1):
                    subCells = []
                    for y in range(0,Size,1):
                        if time == 0:
                            subCells.append(CheckerCell(x,y,[x,y] in fixedWall1))
                        else:
                            subCells.append(CheckerCell(x,y,[x,y] in fixedWall2))
                    checkerCell.append(subCells)
                #連なった非壁セルのチャンクをIDで分類
                currentID = 1
                for x in range(0,Size,1):
                    for y in range(0,Size,1):
                        if not checkerCell[x][y].CanRegist():
                            continue
                        currentCells = [[x,y]]
                        nextCells = []
                        while(len(currentCells) > 0):
                            while(len(currentCells) > 0):
                                cellPos = currentCells.pop()
                                checkerCell[cellPos[0]][cellPos[1]].Regist(currentID, nextCells)
                            currentCells = nextCells.copy()
                            nextCells.clear()
                        currentID += 1
                #端に触れているチャンクIDを分析
                invalidID = set()
                def appendInvalidID(x,y):
                    invalidID.add(checkerCell[x][y].chunkID)
                for x in range(0,Size,1):
                    appendInvalidID(x,0)
                for x in range(0,Size,1):
                    appendInvalidID(x,Size - 1)
                for y in range(0,Size,1):
                    appendInvalidID(0,y)
                for y in range(0,Size,1):
                    appendInvalidID(Size - 1, y)
                #有効なIDのセルのみカウント
                for x in range(0,Size,1):
                    for y in range(0,Size,1):
                        if not checkerCell[x][y].chunkID in invalidID:
                            area[time] += 1
            areas.append(max(area[0], area[1]))
        return areas

CalcWall = Wall(0)
for area in CalcWall.area():
    print(area)