## Author: 	    Kyle Gilmore
## Date: 	    March 18, 2022
## Project: 	Maze Runner
## File: 	    pth.py
## Function: 	Main Driver of the Maze Runner Project.


try:
    import sys, os
    import pygame
    import threading
    import time
    import math
    import random
except:
    import install_requirements
    import sys, os
    import pygame
    import threading
    import time
    import math
    import random

## class for each pixel in the grid
class Pixel:
    def __init__(self, x, y):
        self.i = y
        self.j = x
        self.g = 0.0
        self.h = 0.0
        self.f = 0.0
        self.val = 1
        self.neighbors = []
        self.parent = None
        self.obscured = True
        self.isOpen = False
        self.isClosed = False
        self.mazeVal = 0

    ## adds neighbors of the processed cell if not obscured
    def addNeighbors(self, grid, i, j, row, col):
        if i - 1  > 0 and grid[i-1][j].mazeVal == 1:
            self.neighbors.append(grid[i-1][j])
        if i + 1 < row and grid[i+1][j].mazeVal == 1:
            self.neighbors.append(grid[i+1][j])
        if j - 1 > 0 and grid[i][j-1].mazeVal == 1:
            self.neighbors.append(grid[i][j-1])
        if j + 1 < col and grid[i][j+1].mazeVal == 1:
            self.neighbors.append(grid[i][j+1])
        pygame.display.update()

## fills the selected start and end cell of the grid in yellow
def select(grid, x, y, width, height):
    pygame.draw.rect(screen,(255,255,0),(x*width,y*height,width,height),0)
    pygame.display.update()

## fills the clicked cell with grey and has it block the path
def mouseClick(grid, x, y, width, height):
    pygame.draw.rect(screen,(0,0,0),(x*width,y*height,width,height),0)
    grid[y][x].mazeVal = 0
    pygame.display.update()

## calculates the heiristic from the selected cell to the end cell
def heuristic(current,end):
    return math.sqrt((current.i - end.i)**2 + (current.j - end.j)**2)

## calculates the next path closest to the end cell with the remaining open list
def aStarAlgo(start, end, count,width,height):

    if len(openList) == 0:
        return 0
    if len(openList) > 0:
        count = 0
        lowestI = 0
        
        ## draws each cell of the closed list in blue
        ##for node in closedList:
        ##    pygame.draw.rect(screen,(0, 0, 255),(node.i*height,node.j*width,height,width),0)
        
        ## lowest value of the open list is found and popped from the list to be used by the algorithm
        for node in openList:
            if openList[lowestI].f > node.f:
                lowestI = count
            count = count + 1
        count = 0
        currentNode = openList.pop(lowestI)
        closedList.append(currentNode)
        neighbors = currentNode.neighbors

        ## if the current node reaches the end, the path is found and is calculated
        if currentNode == end:
            print("Goal Reached!")
            while(currentNode != start):
                if currentNode.g - currentNode.parent.g == 1:
                    count = count + 1
                    currentNode = currentNode.parent
                    pygame.draw.rect(screen,(0, 255, 0),(currentNode.i*height,currentNode.j*width,height,width),0)
            pygame.display.update()
            print("The path length is: " + str(count))
            time.sleep(5)
            exit()

        ## each neighbor of the current cell has their heiristic and G value calculated and compared for the shortest
        ## A neighbor's parent is set to the current node
        for neighbor in neighbors:
            neighbor.h = heuristic(neighbor,end)
            if neighbor not in closedList:
                newG = currentNode.g + currentNode.val
                if neighbor in openList:
                    if newG < neighbor.g:
                        neighbor.g = newG
                else:
                    neighbor.g = newG
                    openList.append(neighbor)
            neighbor.f = neighbor.g + neighbor.h
            if neighbor.parent == None:
                neighbor.parent = currentNode

        ## draws each cell of the open list in red
        for it in openList:
            pygame.draw.rect(screen,(0, 0, 255),(it.i*width,it.j*height,height,width),0)

        ## draws each cell of the closed list in blue
        for it in closedList:
            if it != start:
                pygame.draw.rect(screen,(255, 0, 0),(it.i*width,it.j*height,height,width),0)
        currentNode.closed = True

def initializeMaze(): 
    for i in range(row):
        maze[i] = [0 for j in range(col)]

    for i in range(row):
        for j in range(col):
            maze[i][j] = Pixel(i,j)

    for i in range(row):
        for j in range(col):
            pygame.draw.rect(screen,(0,0,0),(j*height,i*height,width,height),0)
            pygame.display.update()

    randRow = random.randint(0,row)
    randCol = random.randint(0,col)

    while randRow % 2 == 0:
        randRow = random.randint(0,row)

    while randCol % 2 == 0:
        randCol = random.randint(0,col)

    beginSquare = maze[randRow][randCol]
    beginSquare.mazeVal = 1
    recursion(randRow,randCol)

    for i in range(row):
        for j in range(col):
            if maze[i][j].mazeVal == 0:
                pygame.draw.rect(screen,(0,0,0),(j*width,i*height,width,height),0)
            if maze[i][j].mazeVal == 1:
                pygame.draw.rect(screen,(255,255,255),(j*width,i*height,width,height),0)
    pygame.display.update()

    ##pygame.draw.rect(screen,(0,0,0),(randRow*height,randCol*width,width,height),0)
    ##pygame.display.update()


def recursion(randRow, randCol):

    dirs = []

    for i in range(4):
        dirs.append(i+1)
    random.shuffle(dirs)

    for i in dirs:
        if i == 1:
            if randRow - 2 <= 0:
                continue
            if maze[randRow - 2][randCol].mazeVal == 0:
                maze[randRow - 2][randCol].mazeVal = 1
                maze[randRow - 2][randCol].obscured = False
                maze[randRow - 1][randCol].mazeVal = 1
                maze[randRow - 1][randCol].obscured = False
                recursion(randRow - 2, randCol)
        elif i == 2:
            if randRow + 2 >= row - 1:
                continue
            if maze[randRow + 2][randCol].mazeVal == 0:
                maze[randRow + 2][randCol].mazeVal = 1
                maze[randRow + 2][randCol].obscured = False
                maze[randRow + 1][randCol].mazeVal = 1
                maze[randRow + 1][randCol].obscured = False
                recursion(randRow + 2, randCol)
        elif i == 3:
            if randCol - 2 <= 0:
                continue
            if maze[randRow][randCol - 2].mazeVal == 0:
                maze[randRow][randCol - 2].mazeVal = 1
                maze[randRow][randCol - 2].obscured = False
                maze[randRow][randCol - 1].mazeVal = 1
                maze[randRow][randCol - 1].obscured = False
                recursion(randRow, randCol - 2)
        elif i == 4:
            if randCol + 2 >= col - 1:
                continue
            if maze[randRow][randCol + 2].mazeVal == 0:
                maze[randRow][randCol + 2].mazeVal = 1
                maze[randRow][randCol + 2].obscured = False
                maze[randRow][randCol + 1].mazeVal = 1
                maze[randRow][randCol + 1].obscured = False
                recursion(randRow, randCol + 2)

## main function of the program
def main():
    initializeMaze()
    count = 0
    print("")
    print("Welcome to the Maze Runner!")
    print("")
    print("Select your starting point.")
    sLoop = True

    ## start cell is selected
    while(sLoop):
        ev = pygame.event.get()
        for event in ev:
            if pygame.mouse.get_pressed()[0]:
                startCoords = pygame.mouse.get_pos()
                sI = startCoords[1] // height;
                sJ = startCoords[0] // width;
                if sI < 0 or sI > row - 1 or sJ < 0 or sJ > col - 1 or maze[sI][sJ].mazeVal == 0:
                    print("Not a valid selection.")
                    time.sleep(1)
                    break
                select(maze,sJ,sI,width,height)
                start = maze[sI][sJ]
                sLoop = False
                break
        if sLoop == False:
            time.sleep(1)

    ## end cell is selected
    print("")
    print("Select your ending point.")
    print("")
    eLoop = True
    while(eLoop):
        ev = pygame.event.get()
        for event in ev:
            if pygame.mouse.get_pressed()[0]:
                endCoords = pygame.mouse.get_pos()
                sI = endCoords[1] // height;
                sJ = endCoords[0] // width;
                if sI < 0 or sI > row - 1 or sJ < 0 or sJ > col - 1 or maze[sI][sJ].mazeVal == 0:
                    print("Not a valid selection.")
                    print("")
                    time.sleep(1)
                    break
                select(maze,sJ,sI,width,height)
                end = maze[sI][sJ]
                eLoop = False
        if eLoop == False:
            time.sleep(1)

    ## if the left mouse button is pressed, obscuring blocks can be drawn
    ## if the right mouse button is pressed, the pathfinding algorithm starts
    print("Press the left mouse button to draw.") 
    print("Press the right mouse button to find the goal.")
    print("")
    openList.append(start)
    while(True):
        ev = pygame.event.get()
        for event in ev:
            if pygame.mouse.get_pressed()[0]:
                coords = pygame.mouse.get_pos()
                x = coords[0] // width
                y = coords[1] // height
                mouseClick(maze,x,y,width,height)
            if pygame.mouse.get_pressed()[2]:
                for i in range(row):
                    for j in range(col):
                            maze[i][j].addNeighbors(maze,i,j,row,col)    
                while(True):
                    if aStarAlgo(start, end, count, width, height) == 0:
                        print("No goal reached!")
                        time.sleep(5)
                        exit()
                    pygame.display.update()
 
pygame.init()

## the screen is displayed here
screenHeight = 1000
screenWidth = 1000
screen = pygame.display.set_mode((screenHeight,screenWidth))

## grid and algorithm variables are initialized here
openList = []
closedList = []
width = 20
height = 20
row = screenHeight // height
col = screenWidth // width

maze = [0 for i in range(row)]

main()
