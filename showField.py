import math
import numpy as np
from matplotlib import pyplot as plt
import csv

while(1):
    plt.cla
    with open('A11.csv') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        for x in range(0, len(l)):
            for y in range(0, len(l)):
                color = "white"
                if l[x][y] == "1":
                    color = "lightblue"
                elif l[x][y] == "2":
                    color = "gray"
                elif l[x][y] == "a":
                    color = "blue"
                elif l[x][y] == "b":
                    color = "red"
                else:
                    color = "white"
                plt.plot(x, y, marker='s', markersize=20, c=color)
    plt.axis('square')
    plt.show()
    
