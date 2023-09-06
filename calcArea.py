import itertools
from matplotlib import pyplot as plt
import numpy as np

terminal1 = [[0,1],[5,7],[9,2]]
terminal2 = [[10,8],[7,9]]
wall1 = [[0,1],[1,1],[2,1],[3,2],[4,3],[5,4],[5,5],[5,6],[5,7],[6,3],[7,2],[8,2],[9,2]]
wall2 = [[10,8],[9,8],[8,8],[7,8],[7,9]]

Terminals = [terminal1,terminal2]
Walls = [wall1, wall2]

class Wall:
    id=0
    def __init__(self, id):
        self.id=id
    def wall(self):
        return Walls[self.id]
    def terminal(self):
        return Terminals[self.id]
    def area(self):
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
            plt.plot(pos1[0], pos1[1], marker='s', markersize=20, c="red")
            plt.plot(pos2[0], pos2[1], marker='s', markersize=20, c="blue")
            plt.plot(edge1[0], edge1[1], marker='s', markersize=20, c="green")
            plt.plot(edge2[0], edge2[1], marker='s', markersize=20, c="yellow")
            for wallPos in self.wall():
                plt.plot(wallPos[0], wallPos[1], marker='s', markersize=15, c="gray")
            #補完線を計算
            if diff[0] > diff[1]:
                fixedWall1 = []#self.wall().copy()
                for wallPos in range(pos1[0], edge1[0], 1 if pos1[0]<edge1[0] else -1):
                    fixedWall1.append([wallPos,pos1[1]])
                for wallPosX, wallPosY in zip(range(edge1[0], pos2[0], 1 if edge1[0]<pos2[0] else -1),range(edge1[1], pos2[1], 1 if edge1[0]<pos2[0] else -1)):
                    fixedWall1.append([wallPosX,wallPosY])
                fixedWall2 = []#self.wall().copy()
                for wallPos in range(pos2[0], edge2[0], 1 if pos2[0]<edge2[0] else -1):
                    fixedWall2.append([wallPos,pos2[1]])
                for wallPosX, wallPosY in zip(range(edge2[0], pos1[0], 1 if edge2[0]<pos1[0] else -1),range(edge2[1], pos1[1], 1 if edge2[0]<pos1[0] else -1)):
                    fixedWall2.append([wallPosX,wallPosY])
            else:
                fixedWall1 = []#self.wall().copy()
                for wallPos in range(pos1[1], edge1[1], 1 if pos1[1]<edge1[1] else -1):
                    fixedWall1.append([pos1[0],wallPos])
                for wallPosX, wallPosY in zip(range(edge1[0], pos2[0], 1 if edge1[0]<pos2[0] else -1),range(edge1[1], pos2[1], 1 if edge1[1]<pos2[1] else -1)):
                    fixedWall1.append([wallPosX,wallPosY])
                fixedWall2 = []#self.wall().copy()
                for wallPos in range(pos2[1], edge2[1], 1 if pos2[1]<edge2[1] else -1):
                    fixedWall2.append([pos2[0],wallPos])
                for wallPosX, wallPosY in zip(range(edge2[0], pos1[0], 1 if edge2[0]<pos1[0] else -1),range(edge2[1], pos1[1], 1 if edge2[1]<pos1[1] else -1)):
                    fixedWall2.append([wallPosX,wallPosY])
            for wallPos in fixedWall1:
                plt.plot(wallPos[0], wallPos[1], marker='s', markersize=10, c="lightgreen")
            for wallPos in fixedWall2:
                plt.plot(wallPos[0], wallPos[1], marker='s', markersize=10, c="lightyellow")
            #補完線をグラフに描画
            plt.axis('square')
            plt.xlim(0,10)
            plt.ylim(10,0)
            plt.xticks( np.arange(0, 12, 1))
            plt.yticks( np.arange(0, 12, 1))
            plt.show()

CalcWall = Wall(0)
CalcWall.area()