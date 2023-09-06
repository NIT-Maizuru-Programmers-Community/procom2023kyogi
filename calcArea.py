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
        for pos in itertools.combinations(self.terminal(), 2):
            pos1 = pos[0]
            pos2 = pos[1]
            diff = [pos2[0] - pos1[0], pos2[1] - pos1[1]]
            if diff[0] > diff[1]:
                edge = [pos1[0] + diff[0] - diff[1], pos1[1]]
            else:
                edge = [pos1[0], pos1[1] + diff[1] - diff[0]]
            plt.plot(pos1[0], pos1[1], marker='s', markersize=20, c="red")
            plt.plot(pos2[0], pos2[1], marker='s', markersize=20, c="blue")
            plt.plot(edge[0], edge[1], marker='s', markersize=20, c="green")
            plt.axis('square')
            plt.xlim(0,10)
            plt.ylim(10,0)
            plt.xticks( np.arange(0, 12, 1))
            plt.yticks( np.arange(0, 12, 1))
            plt.show()

CalcWall = Wall(0)
CalcWall.area()