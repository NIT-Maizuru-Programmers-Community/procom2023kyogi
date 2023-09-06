# -*- coding: utf-8 -*-
# ライブラリを読み込み
import numpy as np
from collections import defaultdict
import random
import networkx as nx
from queue import Queue
import sys
import math

import solver
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
        for i in range(vertical):
            for j in range(horizontal):
                if self.field[i][j].wall==Team.A:
                    p.append([i,j])
        return p    
    
    def context(self, p):
        if p%2==0:
            return 1
        else:
            return -1
        
        
#kが1味方-1敵            
#城壁の端を探索
def wall_dfs(t,G):
    if t==1:
        k=1
    if t==-1:
        k=2
    u=0
    temp=[]
    cent=[]
    dx_dy=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    p=G.boardcheck(k)
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
        

def temporary_evaluator(Game,cond,area):
    evaluation=0
    moving=1
    building=1
    breaking=1
    
    return evaluation
    
def evaluator_main(Game,depth,movement,num_per,alpha,beta, per, mason): 
    best_move_arr=[0]*num_per
    for k in range(num_per):
        if(movement<depth):
            t=Game.context(movement)
            G_temp=Game
            mason.Act
            max=evaluator_main(G_temp, depth, movement+1, num_per, alpha, beta, per,mason)
            best_move=0
            for i in range(15):
                G_temp=Game
                
                temp=evaluator_main(G_temp, depth, movement+1, num_per, alpha, beta, per,mason)
                if t==1:
                    if (temp>=beta):
                        return temp
                    elif temp>alpha:
                        best_move=i
                        alpha=temp
                elif t==-1:
                    if temp<=alpha:
                        return temp
                    elif temp>beta:
                        best_move=i
                        beta=temp
        elif depth==movement:
            return temporary_evaluator(Game, best_move)
        if t==1:
            best_move_arr.append(best_move)
            return alpha
        elif t==-1:
            best_move_arr.append(best_move)
            return beta
        
def evaluator(Game,depth,movement):
    return evaluator_main(Game,depth,movement)
    
vertical=15
horizontal=15
number_people=3
field = solver.Cells
Team = solver.Team
G=Game(vertical, horizontal, number_people,field,Team)
Ma=solver.mason