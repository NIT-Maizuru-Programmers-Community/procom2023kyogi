# -*- coding: utf-8 -*-
# ライブラリを読み込み
import numpy as np
from collections import defaultdict
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.animation import FuncAnimation
from queue import Queue
import sys
import math

class Game:
        #field[x][y][0]について
        #2敵城壁3中立4味方城壁
        #field[x][y][1]について
        #0誰もいない1味方職人2敵職人3城4池

    def __init__(self,vertical,horizontal,number_people,field=None):
        self.number_people=number_people
        self.vertical=vertical
        self.horizontal=horizontal
        self.field=np.zeros(shape=(vertical,horizontal,2))
    ##field[x][y][0]がsの座標を探す 
    def boardcheck(self,s):
        p=[]
        for i in range(15):
            for j in range(15):
                if self.field[i][j][0]==s:
                    p.append([i,j])
        return p    
    
    def context(self, p):
        if p%2==0:
            return 1
        else:
            return -1
    #行動を処理
    #fieldはG.fieldを渡す
    #moveは行動．0移動1建築2破壊
    #rlは右なら1,左なら-1
    #udは上なら-1,下なら1
    def conduct(self,x,y,cond,contex):
        movement=[[0,0,1],[0,1,1],[0,1,0],[0,0,-1],[0,-1,-1],[0,-1,0],[0,1,-1],[0,-1,1],
              [1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[2,1,1],[2,1,-1],[2,-1,1],[2,-1,-1]]
        move=movement[cond][0]
        rl=movement[cond][1]
        ud=movement[cond][2]
        try:
            if move==0:
                x+=rl
                y+=ud
                p=[x,y]
            elif move==1:
                if (self.field[x+rl][y+ud][1]==0 or 
                    self.field[x+rl][y+ud][1]==4):
                    if (self.field[x+rl][y+ud][0]==3 or
                        self.field[x+rl][y+ud][0]==6):
                        self.field[x+rl][y+ud][0]+=contex
                    if (self.field[x+rl][y+ud][0]==8 or
                        self.field[x+rl][y+ud][0]==9):
                        self.field[x+rl][y+ud][0]=3+contex
            elif move==2:
                if (self.field[x+rl][y+ud][0]==2 or 
                    self.field[x+rl][y+ud][0]==4 or
                    self.field[x+rl][y+ud][0]==5 or 
                    self.field[x+rl][y+ud][0]==7):
                    self.field[x+rl][y+ud][0]+=contex
            return p
        #フィールドの外にアクセスしたとき         
        except IndexError as e:
            return e

class Person:
    def __init__(self,x,y,contex):
        self.x=x #職人のx座標
        self.y=y #職人のy座標
        self.contex=contex #職人の属性(1or-1)
    #他職人との距離を計算
    def distance(self,p):
        distance=[]
        for k in G.number_people:
            for i in G.horizontal:
                for j in G.vertical:
                    if G.field[i][j][1]==p:
                        distance.append(dis=math.sqrt(pow((self.x-j),2)+pow((self.y-i),2)))
        return distance
    #行動を処理
    #fieldはG.fieldを渡す
    #moveは行動．0移動1建築2破壊
    #rlは右なら1,左なら-1
    #udは上なら-1,下なら1
    def conduct(self,Game,cond):
        self.x,self.y=Game.conduct(self.x,self.y,cond,self.contex)

#kが1味方-1敵            
def wall_dfs(x,y,t,G):
    if t==1:
        k=4
        s=7
    if t==-1:
        k=2
        s=5
    u=0
    dx_dy=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    kx,ky=G.boardcheck(k)[0]##城壁の端
    length=len(G.boardcheck(k))+len(G.boardcheck(s))
    count=[]##城壁の端の配列
    stack=[[kx,ky]]
    visited=[[0 for i in range(G.horizontal)]for j in range(G.vertical)]##訪れたかどうか
    visited[kx][ky]=1
    while u < length:
        point=[]
        while stack:
            x,y=stack.pop()
            t=0
            for i in range(8):
                wx,wy=x+dx_dy[i][0],y+dx_dy[i][1]
                if 0 <= wx < G.vertical and 0 <= wy < G.horizontal and np.all(visited[wx][wy] == 0) and (np.all(G.field[wx][wy]==k)or np.all(G.field[wx][wy]==s)):
                    visited[wx][wy]=1
                    stack.append([wx,wy])
                if 0 <= wx < G.vertical and 0 <= wy < G.horizontal and np.all(G.field[wx][wy]==k):
                    t=t+1
                if t==1 and i==7:
                    point.append([x,y]) 
        if not stack:
            count.append(point)
        while u<length:
            px,py=G.boardcheck(k)[u]
            if visited[px][py]==0:
                kx,ky=G.boardcheck(k)[u]##城壁の端
                stack=[[kx,ky]]
                visited[kx][ky]=1
                break
            u+=1
    return count #三次元
        
#p場所属性sターン属性
def areacalc(p,s,G):
    castle=False
    dem = inf
    dm=[]
    area=0
    ar=[]
    kx,ky=0,0
    fin=[]
    s=[]
    count=wall_dfs(G.vertical, G.horizontal, p)
    a=0
    #最短経路を求める
    for k in range(len(count)):
        for i in range(len(count[k])):
            px,py=count[i]
            for j in range(len(count[k])):
                if i!=j:
                    wx,wy=count[k][j]
                    d=math.sqrt(pow((px-wx),2)+pow((py-wy),2))
                    if dem>d:
                        dem=d
                        f=j
            dm.append(dem)
            dem=inf
            s.append(count[k][f],f)
        fin.append(s)
        s=[]
    j=0
    while count:
        i=0
        while count[j]:
                
                temp=[]
                tx,ty=count[j][i]
                gx,gy,n=fin[j][i]   
                pdx=np.sign(tx-gx)
                pdy=np.sign(ty-gy)
                tdx=abs(tx-gx)
                tdy=abs(ty-gy)
                if tempdx>tempdy:
                    c=0
                    s1=math.ceil((tdx-tdy)/2)
                    s2=math.floor((tdx-tdy)/2)
                    fx=tx
                    fy=ty
                    while s1>0:
                        fx+=pdx
                        temp.append(fx,fy)
                        s1-=1
                    while tdy>0:
                        fx+=pdx
                        fy+=pdy
                        temp.append(fx,fy)
                        tdy-=1
                        centx,centy=fx,fy
                    while s2>0:
                        fx+=pdx
                        temp.append(fx,fy)
                        s1-=1
                elif tempdx<tempdy:
                    c=1
                    s1=math.ceil((tempdy-tempdx)/2)
                    s2=math.floor((tempdy-tempdx)/2)
                    fx=tx
                    fy=ty
                    while s1>0:
                        fy+=pdy
                        temp.append(fx,fy)
                        s1-=1
                    while tdx>0:
                        fx+=pdx
                        fy+=pdy
                        temp.append(fx,fy)
                        tdx-=1
                        centx,centy=fx,fy
                    while s2>0:
                        fy+=pdy
                        temp.append(fx,fy)
                        s1-=1
                elif tempdx==tempdy:
                    c=2
                    while tdx>0:
                        fx+=pdx
                        fy+=pdy
                        temp.append(fx,fy)
                        tdx-=1
                        if tdx == (abs(tx-gx))/2:
                            centx,centy=fx,fy
                po=0
                while (centx<G.horizontal and centx>0):
                    centx+=1
                    po+=1
                    if G.field[centx][centy][0]==3+teki and G.field[centx][centy][0]==6+teki:
                        dx_dy=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
                        kx,ky=G.boardcheck(k)[0]
                        length=len(G.boardcheck(k))+len(G.boardcheck(s))
                        count=[]##城壁の端の配列
                        stack=[[kx,ky]]
                        visited=[[0 for i in range(G.horizontal)]for j in range(G.vertical)]##訪れたかどうか
                        visited[kx][ky]=1
                        while u < length:
                            point=[]
                            while stack:
                                x,y=stack.pop()
                                t=0
                                for i in range(8):
                                    wx,wy=x+dx_dy[i][0],y+dx_dy[i][1]
                                    if 0 <= wx < G.vertical and 0 <= wy < G.horizontal and np.all(visited[wx][wy] == 0) and (np.all(G.field[wx][wy]==k)or np.all(G.field[wx][wy]==s)):
                                        visited[wx][wy]=1
                                        stack.append([wx,wy])
                                    if 0 <= wx < G.vertical and 0 <= wy < G.horizontal and np.all(G.field[wx][wy]==k):
                                        t=t+1
                                    if t==1 and i==7:
                                        for o in range(len(count[j])):
                                            if count[j][o]==[x,y]:
                                                break
                                        else:
                                            continue
                                        break
                                else:
                                    continue
                                break
                            else:
                                continue
                            break
                        else:
                            continue
                        break
                else:
                    po=0
                    while (centx<G.horizontal and centx>0):
                        centx+=1
                        po+=1
                        if G.field[centx][centy][0]==3+teki and G.field[centx][centy][0]==6+teki:
                            dx_dy=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
                            kx,ky=G.boardcheck(k)[0]
                            length=len(G.boardcheck(k))+len(G.boardcheck(s))
                            count=[]##城壁の端の配列
                            stack=[[kx,ky]]
                            visited=[[0 for i in range(G.horizontal)]for j in range(G.vertical)]##訪れたかどうか
                            visited[kx][ky]=1
                            while u < length:
                                point=[]
                                while stack:
                                    x,y=stack.pop()
                                    t=0
                                    for i in range(8):
                                        wx,wy=x+dx_dy[i][0],y+dx_dy[i][1]
                                        if 0 <= wx < G.vertical and 0 <= wy < G.horizontal and np.all(visited[wx][wy] == 0) and (np.all(G.field[wx][wy]==k)or np.all(G.field[wx][wy]==s)):
                                            visited[wx][wy]=1
                                            stack.append([wx,wy])
                                        if 0 <= wx < G.vertical and 0 <= wy < G.horizontal and np.all(G.field[wx][wy]==k):
                                            t=t+1
                                        if t==1 and i==7:
                                            for o in range(len(count[j])):
                                                if count[j][o]==[x,y]:
                                                    break
                                            else:
                                                continue
                                            break
                                    else:
                                        continue
                                    break
                                else:
                                    continue
                                break
                            else:
                                continue
                            break
                    else:
                        continue
                    break
                area+=po*po*1.5
                i+=1 
        j+=1

def temporary_evaluator(Game,Pers,cond,cont,area):
    evaluation=0
    moving=1
    building=1
    breaking=1
    point=0
    dis=Pers.distance(cont)
    if cond == 0:
        
    if cond == 1:
        if Game.field[][][]
            area=areacalc
            point = 100
            point += area*building
    if cond == 2:
        if 
    return evaluation
    
def evaluator_main(Game,depth,movement,num_per,Per,alpha,beta):
    #movement=[[0,0,1],[0,1,1],[0,1,0],[0,0,-1],[0,-1,-1],[0,-1,0],[0,1,-1],[0,-1,1],
              #[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[2,1,1],[2,1,-1],[2,-1,1],[2,-1,-1]]    
    best_move_arr=[0]*num_per
    for k in range(num_per):
        if(movement<depth):
            t=Game.context(movement)
            G_temp=Game
            Per_temp=Per[k]
            Per_temp.conduct(G_temp,0)
            max=evaluator_main(G_temp, depth, movement+1, num_per, Per, alpha, beta)
            best_move=0
            for i in range(16):
                G_temp=Game
                Per_temp=Per
                Per_temp.conduct(G_temp,i)
                temp=evaluator_main(G_temp, depth, movement+1, num_per, Per, alpha, beta)
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
    
if __name__ == "__main__":
    vertical=15
    horizontal=15
    number_people=3
    G=Game(vertical, horizontal, number_people)