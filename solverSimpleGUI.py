import requests
import time
import threading
from matplotlib import pyplot as plt
import randomplay
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
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
print("PrimaryGet: ", Response)

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
Masons = [(0, 0)] * TeamMasonCount
for x in range(0, Size):
    for y in range(0, Size):
        if Cells[x][y].mason > 0:
            Masons[Cells[x][y].mason - 1] = (x, y)

CurrentTurn = 0
Actions = []


# 毎ターン処理
def Process():
    global CurrentTurn
    global Response

    while True:
        if CurrentTurn > 1:
            ResponseGet = requests.get(Url, params=Param)
            while ResponseGet.json()["turn"] < CurrentTurn:
                with requests.get(Url, params=Param) as ResponseGet:
                    time.sleep(0.01)
            Response = ResponseGet.json()
            Board = Response["board"]
            for x in range(0, Size):
                for y in range(0, Size):
                    Cells[x][y].Set(Board)
            # print("Get: ", Response)

        CurrentTurn += 1

        Actions.clear()
        for masonX, masonY in Masons:
            type, dir = randomplay.randomplay(Cells, masonX, masonY, Size)
            Actions.append(
                {
                    "type": type,
                    "dir": dir,
                }
            )
        json_data = {
            "turn": CurrentTurn,
            "actions": Actions,
        }
        print(json_data)
        responsePost = requests.post(Url, params=Param, headers=Header, json=json_data)
        while responsePost.text == "TooEarly":
            with requests.post(Url, params=Param, headers=Header, json=json_data) as responsePost:
                time.sleep(0.01)
        print("Post: ", responsePost)

        CurrentTurn += 1


# グラフ描画処理
def ShowCells():
    global CurrentTurn
    global Response

    fig = Figure()
    plt = fig.add_subplot(111)
    lines = []
    for _ in range(0, Size):
        for _ in range(0, Size):
            line = plt.plot([], [], lw=2, label="line")
            lines.append(line)

    def _quit():
        root.quit()
        root.destroy()

    def init():
        for line in lines:
            line.set_data([], [])
        return tuple(lines)

    def animate(i):
        # plt.cla()
        Board = Response["board"]
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

        # line.set_ydata(np.sin(x + i))  # update the data.
        # return (line,)

    root = tkinter.Tk()
    root.wm_title("Embedding in Tk anim")

    # FuncAnimationより前に呼ぶ必要がある
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

    # x = np.arange(0, 3, 0.01)  # x軸(固定の値)
    l = np.arange(0, 8, 0.01)  # 表示期間(FuncAnimationで指定する関数の引数になる)

    # plt.set_ylim([-1.1, 1.1])
    # (line,) = plt.plot(x, np.sin(x))

    ani = animation.FuncAnimation(
        fig,
        animate,
        l,
        # init_func=init,
        interval=10,
        # blit=True,
    )

    toolbar = NavigationToolbar2Tk(canvas, root)
    canvas.get_tk_widget().pack()
    button = tkinter.Button(master=root, text="Quit", command=_quit)
    button.pack()
    tkinter.mainloop()

    """while True:
        Board = Response["board"]
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
        plt.cla()"""


Thread1 = threading.Thread(target=Process)
Thread1.start()
# ShowCells()
while True:
    board = Response["board"]
    print("--------------------------------------------")
    for x in range(0, Size):
        for y in range(0, Size):
            print(str(Board["masons"][x][y]) + " ", end="")
        print("\n")
    print("--------------------------------------------")
    time.sleep(6)
