import requests


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


Cells = []
Url = "http://localhost:3000/matches"  # http://172.28.0.1:8080/matches ←本番用 http://localhost:3000/matches ←練習用
Param = {"token": "maizuru98a2309fded8fd535faf506029733e9e3d030aae3c46c7c5ee8193690"}
Header = {"Content-Type": "application/json"}

Response = requests.get(Url, params=Param).json()["matches"][0]
Board = Response["board"]
MatchID = Response["id"]
Size = Board["width"]
TeamMasonCount = Board["mason"]
Url += "/" + str(MatchID)

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
