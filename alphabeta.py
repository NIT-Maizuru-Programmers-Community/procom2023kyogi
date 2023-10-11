# -*- coding: utf-8 -*-
# ライブラリを読み込み
import numpy as np
from collections import defaultdict
import random
import networkx as nx
from queue import Queue
import sys
import math
import copy
import itertools
import calcAreaPractice
#Cells,Size,CurrentTurn,TeamMasonCount

class Game:
    def __init__(self,vertical,horizontal,number_people,field,team):
        self.number_people=number_people
        self.vertical=vertical
        self.horizontal=horizontal
        self.field = field
        self.team=team
    def boardcheck(self,s):
        p=[]
        for i in range(self.vertical):
            for j in range(self.horizontal):
                if self.field[i][j].wall==s:
                    p.append([i,j])
        return p    
    
    def context(self, p):
        if p%2==0:
            return 1
        else:
            return -1
        
    def act(self,cond,x,y,dx,dy,team,id):
        if -1<cond<8:
            self.field[x][y].Exit()
            self.field[x+dx][y+dy].Enter(team,id)
        elif 7<cond<12:
            self.field[x+dx][y+dy].Place(team)
        elif 11<cond<16:
            self.field[x+dx][y+dy].Break()


def areacalc(edge,walloriginal,Size):
    areas = 0
    #壁の端2つの全組み合わせで試行
    for pos in itertools.combinations(edge, 2):
        #補完線の折れ曲がる座標を計算
        pos1 = pos[0]
        pos2 = pos[1]
        try:
            diff = [abs(pos2[0] - pos1[0]), abs(pos2[1] - pos1[1])]
        except:
            return areas
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
            fixedWall1 = walloriginal.copy()
            for wallPos in range(pos1[0], edge1[0], 1 if pos1[0]<edge1[0] else -1):
                fixedWall1.append([wallPos,pos1[1]])
            for wallPosX, wallPosY in zip(range(edge1[0], pos2[0], 1 if edge1[0]<pos2[0] else -1),range(edge1[1], pos2[1], 1 if edge1[0]<pos2[0] else -1)):
                fixedWall1.append([wallPosX,wallPosY])
            fixedWall2 = walloriginal.copy()
            for wallPos in range(pos2[0], edge2[0], 1 if pos2[0]<edge2[0] else -1):                    
                fixedWall2.append([wallPos,pos2[1]])
            for wallPosX, wallPosY in zip(range(edge2[0], pos1[0], 1 if edge2[0]<pos1[0] else -1),range(edge2[1], pos1[1], 1 if edge2[0]<pos1[0] else -1)):
                fixedWall2.append([wallPosX,wallPosY])
        else:
            fixedWall1 = walloriginal.copy()
            for wallPos in range(pos1[1], edge1[1], 1 if pos1[1]<edge1[1] else -1):
                fixedWall1.append([pos1[0],wallPos])
            for wallPosX, wallPosY in zip(range(edge1[0], pos2[0], 1 if edge1[0]<pos2[0] else -1),range(edge1[1], pos2[1], 1 if edge1[1]<pos2[1] else -1)):
                fixedWall1.append([wallPosX,wallPosY])
            fixedWall2 = walloriginal.copy()
            for wallPos in range(pos2[1], edge2[1], 1 if pos2[1]<edge2[1] else -1):
                fixedWall2.append([pos2[0],wallPos])
            for wallPosX, wallPosY in zip(range(edge2[0], pos1[0], 1 if edge2[0]<pos1[0] else -1),range(edge2[1], pos1[1], 1 if edge2[1]<pos1[1] else -1)):
                 fixedWall2.append([wallPosX,wallPosY])
        #面積を算出
        area1 = 0
        area2 = 0
        for x in range(0,Size,1):
            flag1 = False
            flag2 = False
            subArea1 = 0
            subArea2 = 0
            for y in range(0,Size,1):
                if [x,y] in fixedWall1:
                    if flag1 == False:
                        flag1 = True
                    else:
                        flag1 = False
                        area1 += subArea1
                        subArea1 = 0
                elif flag1 == True:
                    subArea1 += 1
                if [x,y] in fixedWall2:
                    if flag2 == False:
                        flag2 = True
                    else:
                        flag2 = False
                        area2 += subArea2
                        subArea2 = 0
                elif flag2 == True:
                    subArea2 += 1
            flag1 = False
            flag2 = False
            subArea1 = 0
            subArea2 = 0
        areas += max(area1, area2)
    return areas
      
dx_dy=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
#kが1味方-1敵            
#城壁の端を探索
def wall_dfs(t,G):
    if t==1:
        k=1
    if t==2:
        k=2
    u=0
    temp=[]
    cent=[]
    p=G.boardcheck(k)
    if not p:
        return cent,cent
    kx,ky=p[0]##城壁の端
    length=len(p)
    count=[]##城壁の端の配列
    stack=[[kx,ky]]
    visited=[[0 for i in range(G.horizontal)]for j in range(G.vertical)]##訪れたかどうか
    visited[kx][ky]=1
    while u < length:
        point=[]
        temp=[]
        while stack:
            x,y=stack.pop()
            t=0
            for i in range(8):
                wx,wy=x+dx_dy[i][0],y+dx_dy[i][1]
                if 0 <= wx < G.vertical and 0 <= wy < G.horizontal and np.all(visited[wx][wy] == 0) and (np.all(G.field[wx][wy].wall==k)):
                    visited[wx][wy]=1
                    stack.append([wx,wy])
                if 0 <= wx < G.vertical and 0 <= wy < G.horizontal and np.all(G.field[wx][wy].wall==k):
                    t=t+1
                if t==1 and i==7:
                    point.append([x,y]) 
                else:
                    temp.append([x,y])
        if not stack:
            count.append(point)
            cent.append(temp)
        while u<length:
            px,py=p[u]
            if visited[px][py]==0:
                kx,ky=p[u]##城壁の端
                stack=[[kx,ky]]
                visited[kx][ky]=1
                break
            u+=1
    return count, cent #三次元
        
def wallbreak(game,x,y,mason):
    a,b=wall_dfs(mason.Team,game)
    for i in range(len(b)):
        if [x,y] in b[i]:
            p=i
            break
    else:
        for i in range(len(a)):
            if [x,y] in a[i]:
                p=i
                break
        else:
            return -float('inf')
    area = areacalc(a[p],b[p],game.horizontal)
    return area
    
def wallbuild(game,x,y,mason):
    if mason.Team==1:
        k=1
    else:
        k=2
    if not twentyfourcheck(x,y,game,k):
        return 0
    else:
        c,d=twentyfourcheck(x,y,game,k)
        a,b=wall_dfs(mason.Team,game)
        for i in range(len(b)):
            if [c,d] in b[i]:
                p=i
                break
        else:
            for i in range(len(a)):
                if [c,d] in a[i]:
                    p=i
                    break
            else:
                return -float('inf')
    return areacalc(a[p],b[p],game.horizontal)

castle_xy=[[2,0],[2,1],[2,2],[2,-1],[2,-2],[1,2],[1,-2],[0,2],[0,-2],[-1,2],[-1,-2],[-2,0],[-2,1],[-2,2],[-2,-1],[-2,-2]]
def twentyfourcheck(x,y,game,b):
    for i in range(8):
        if game.field[x+dx_dy[i][0]][y+dx_dy[i][1]].structure==b:
            return x+dx_dy[i][0],y+dx_dy[i][1]
    for j in range(16):
        if game.field[x+castle_xy[j][0]][y+castle_xy[j][1]].structure==b:
            return x+castle_xy[j][0],y+castle_xy[j][1]
    return False

move=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]

def temporary_evaluator(Game,cond,mason):
    evaluation=0
    moving=1
    building=1
    breaking=1
    castlepoint =1
    e,c=wall_dfs(1,Game)
    area = areacalc(e,c,Game.horizontal)
    if -1<cond<8:
        if not Game.field[mason.x+move[cond][0]][mason.y+move[cond][1]].CanEnter(mason.team):
            return -10000000
        evaluation+=moving
    if 7<cond<12:
        evaluation = 100
        if not Game.field[mason.x+move[cond-8][0]][mason.y+move[cond-8][1]].CanPlace(mason.team):
            return -10000000
        if twentyfourcheck(move[cond-8][0],move[cond-8][1],Game,2):
            evaluation += castlepoint
        evaluation += wallbuild(Game,mason.x+move[cond][0],mason.y+move[cond][1],mason)*building

    if 11<cond<16:
        if not Game.field[mason.x+move[cond-12][0]][mason.y+move[cond-12][1]].Canbreak(mason.team):
            return -10000000
        evaluation += wallbreak()*breaking
    evaluation+=area
    return evaluation
##行動できないときの返り値は？
    
def evaluator_main(Game,depth,movement,num_per,alpha,beta, mikatamason,tekimason,best_move):
    p=0
    if(movement<depth):
        t=Game.context(movement)
        for i in range(16**num_per):
            G_temp=copy.deepcopy(Game)
            bm=[0]*num_per
            c = i
            for k in range(num_per):
                bm = int(c % 16)
                o = bm
                c //= 16
                if 7<bm<12:
                    o = bm - 8
                elif 11<bm<16:
                    o = bm - 12
                if (movement%2==0):
                    G_temp.act(i,mikatamason[k].x,mikatamason[k].y,move[o][0],move[o][1],1,k)
                else:
                    G_temp.act(i,tekimason[k].x,tekimason[k].y,move[o][0],move[o][1],2,k)
            temp=evaluator_main(G_temp, depth, movement+1, num_per, alpha, beta, mikatamason,tekimason,best_move)
            if t==1:
                if (temp>=beta):
                    return temp
                elif temp>alpha:
                    alpha=temp
                    p=i
            elif t==-1:
                if temp<=alpha:
                    return temp
                elif temp>beta:
                    beta=temp
                    p=i
    else:
        fin=0
        for j in range(num_per):
            c=p
            bm = c % 16
            c /= 16
            fin += temporary_evaluator(Game, bm, mikatamason[j])
        return fin
    if ((depth - movement) >= 2):
        return p
    if (movement%2==0):
        return alpha
    else:
        return beta
        
def evaluator(Game,movement,num_per,mikata,teki):
    return evaluator_main(Game,movement+2,movement,num_per,-100000,100000,mikata,teki,0)