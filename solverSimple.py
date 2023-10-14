import requests
import time
import threading
from matplotlib import pyplot as plt
import randomplay


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


def GetTerritoryColor(id):  # 領地
    if id == 1:
        return "brown"
    elif id == 2:
        return "navy"
    elif id == 3:
        return "gold"
    else:
        return "clear"


class Cell:
    x = 0
    y = 0
    structure = 0
    mason = 0
    wall = 0
    territory = 0

    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.structure = board["structures"][x][y]
        self.mason = board["masons"][x][y]

    def Set(self, board):
        self.mason = board["masons"][self.x][self.y]
        self.wall = board["walls"][self.x][self.y]
        self.territory = board["territories"][self.x][self.y]

    def Action(self):
        if self.mason > 0:
            type, dir = randomplay.randomplay(Cells, self.x, self.y, Size)
            Actions.append(
                {
                    "type": type,
                    "dir": dir,
                }
            )


# 定義類
Url = "http://localhost:3000/matches"  # http://172.28.0.1:8080/matches ←本番用 http://localhost:3000/matches ←練習用
Param = {"token": "maizuru98a2309fded8fd535faf506029733e9e3d030aae3c46c7c5ee8193690"}
Header = {"Content-Type": "application/json"}

# 最初期読み込み
Response = requests.get(Url, params=Param).json()["matches"][0]
Board = Response["board"]
MatchID = Response["id"]
IsFirst = Response["first"]
Size = Board["width"]
TeamMasonCount = Board["mason"]
Url += "/" + str(MatchID)
print(Response)

# セル生成
Cells = []
for y in range(0, Size):
    subCells = []
    for x in range(0, Size):
        cell = Cell(x, y, Board)
        subCells.append(cell)
    Cells.append(subCells)

# BoardとCellsの座標系一致確認用
"""for x in range(0, Size):
    for y in range(0, Size):
        print(str(Cells[x][y].x) + "," + str(Cells[x][y].y) + " ", end="")
    print("\n")"""

# 初期処理
CurrentTurn = 1

# ループ処理
def Process():
    global CurrentTurn
    global Response
    while True:
        if CurrentTurn > 2:
            while Response["turn"] <= CurrentTurn:
                with requests.get(Url, params=Param).json() as Response:
                    time.sleep(0.01)
            Board = Response["board"]
            for x in range(0, Size):
                for y in range(0, Size):
                    Cells[x][y].Set(Board)
        print("Get: ", Response)

        CurrentTurn += 1

        Actions.clear()
        for x in range(0, Size):
            for y in range(0, Size):
                Cells[x][y].Action()
        json_data = {
            "turn": CurrentTurn,
            "actions": Actions,
        }
        responsePost = requests.post(Url, params=Param, headers=Header, json=json_data)
        while responsePost.text == "TooEarly":
            with requests.post(Url, params=Param, headers=Header, json=json_data) as responsePost:
                time.sleep(0.01)
        print("Post: ", responsePost)

        CurrentTurn += 1


def ShowCells():
    while True:
        for x in range(0, Size):
            for y in range(0, Size):
                plt.plot(
                    x,
                    Size - 1 - y,
                    marker="s",
                    markersize=20,
                    c=GetStructureColor(Board["structures"][y][x]),
                )
                if CurrentTurn > 2:
                    if GetTerritoryColor(Board["territories"][y][x]) != "clear":
                        plt.plot(
                            x,
                            Size - 1 - y,
                            marker="s",
                            markersize=10,
                            c=GetTerritoryColor(Board["territories"][y][x]),
                        )
                    if GetWallColor(Board["walls"][y][x]) != "clear":
                        plt.plot(
                            x,
                            Size - 1 - y,
                            marker="s",
                            markersize=10,
                            c=GetWallColor(Board["walls"][y][x]),
                        )
                if GetMasonColor(Board["masons"][x][y]) != "clear":
                    plt.plot(
                        x,
                        Size - 1 - y,
                        marker="s",
                        markersize=5,
                        c=GetMasonColor(Board["masons"][y][x]),
                    )
        plt.axis("square")
        plt.pause(0.1)


# Thread1 = threading.Thread(target=Process)
Thread2 = threading.Thread(target=ShowCells)
# Thread1.start()
Thread2.start()
