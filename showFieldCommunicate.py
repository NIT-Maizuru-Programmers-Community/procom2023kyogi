import requests
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import numpy as np

# 対応する色を返す(グラフ描画用)
def GetStructureColor(id):  # 構造物
    if id == 1:
        return "lightgreen"
    elif id == 2:
        return "gray"
    else:
        return "white"

def GetWallColor(id):  # 城壁
    if id == 1:
        return "pink"
    elif id == 2:
        return "lightblue"
    else:
        return "clear"

def GetMasonColor(id):  # 職人
    if id > 0:
        return "red"
    elif id < 0:
        return "blue"
    else:
        return "clear"

def GetterritoryColor(id):
    if id == 1:
        return "brown"
    elif id == 2:
        return "navy"
    elif id == 3:
        return "gold"
    else:
        return "clear"

headers = {'Content-Type': 'application/json'}

Size = 0
# サーバーのURL
url = 'http://localhost:3000/matches'  # http://172.28.0.1:8080/matches ←本番用 http://localhost:3000/matches ←練習用
# クエリパラメータ
params = {'token': 'maizuru98a2309fded8fd535faf506029733e9e3d030aae3c46c7c5ee8193690'}
# GETリクエストを送信
response = requests.get(url, params=params)
print(response)
print("レスポンス内容:", response.text)

load = response.json()
l = load["matches"][0]["board"]
Size = len(l["structures"])
url += "/"
url += str(load["matches"][0]["id"])

CurrentTurn = 1

# グラフの初期化
fig = plt.figure(figsize=(Size, Size))
xline = []  # X軸のデータを格納するリスト
yline = []  # Y軸のデータを格納するリスト

def _update(frame):
    global l, CurrentTurn, x, y  # グローバル変数を使用

    plt.cla()

    for x in range(0, Size):
        for y in range(0, Size):
            plt.plot(x, y, marker='s', markersize=20, c=GetStructureColor(l["structures"][x][y]))
            if CurrentTurn > 1:
                if GetterritoryColor(l["territories"][x][y]) != "clear":
                    plt.plot(x, y, marker='s', markersize=10, c=GetterritoryColor(l["territories"][x][y]))
                if GetWallColor(l["walls"][x][y]) != "clear":
                    plt.plot(x, y, marker='s', markersize=10, c=GetWallColor(l["walls"][x][y]))
                if GetMasonColor(l["masons"][x][y]) != "clear":
                    plt.plot(x, y, marker='s', markersize=5, c=GetMasonColor(l["masons"][x][y]))
            plt.axis('square')

    CurrentTurn += 1
    responseTurn = requests.get(url, params=params)
    while responseTurn.json()["turn"] < CurrentTurn - 1:
        with requests.get(url, params=params) as responseTurn:
            time.sleep(0.01)

    print(responseTurn)
    loadTurn = responseTurn.json()
    l = loadTurn["board"]
    xline.append(frame)  # X軸データを追加
    yline.append(frame)  # Y軸データを追加
    plt.plot(x, y)

def main():
    # 描画するデータ (最初は空っぽ)
    params = {
        'fig': fig,
        'func': _update,  # グラフを更新する関数
        'interval': 10,  # 更新間隔 (ミリ秒)
        'frames': np.arange(0, 10),  # フレームの範囲
        'repeat': False,  # 繰り返さない
    }
    anime = FuncAnimation(**params)
    # グラフを表示する
    plt.show()

if __name__ == '__main__':
    main()
