import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox
import copy
import time
import matplotlib.pyplot as plt


width = 500
height = 500

cols = 25
rows = 20


class Node:
    def __init__(self, snake, parentSnake=None):
        self.snake = snake
        self.parentSnake = parentSnake


class cube:
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny  # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(
            surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2)
        )
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake:
    body = []
    turns = {}

    def __init__(self, color, pos):
        # pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

    def move1(self, dx, dy):
        print(f"dx = {dx} dy = {dy}")
        self.head.dirnx = dx
        self.head.dirny = dy
        print(f"self.dirnx = {self.dirnx} self.dirny = {self.dirny}")
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        print(f"self.turns = {self.turns}")
        print(f"snakeHead = {self.head.pos[:]}")
        for i, c in enumerate(self.body):
            p = c.pos[:]
            print(f"p = {p}")
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

        for j, b in enumerate(self.body):
            print(f"After={b.pos[:]}")

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redrawWindow():  # updates the window
    global win
    win.fill((0, 0, 0))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
    pass


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def Blocked(x, y, listOfSnakes):
    for currSnake in listOfSnakes:
        body = currSnake.snake.body
        for c in body:
            return False
            # print(f"Blocked Position={c.pos[0]},{c.pos[1]} and {x} {y}")
            if c.pos[0] == x and c.pos[1] == y:
                print(f"Blocked{x,y}")
                return True

    return False


def getNearestNode(x, y, listOfSnakes):
    minNode = None
    minDist = 1e9
    distx = 0
    disty = 0

    for currSnake in listOfSnakes:
        headPos = currSnake.snake.head.pos
        distx = abs(headPos[0] - x)
        disty = abs(headPos[1] - y)

        dist = distx + disty

        if dist < minDist:
            minDist, minNode = dist, currSnake

    return minNode, distx, disty


def getNearestNode2(x, y, listOfSnakes):
    minNode = None
    minDist = 1e9
    distx = 0
    disty = 0

    for currSnake in listOfSnakes:
        headPos = currSnake.snake.head.pos
        distx = abs(headPos[0] - x)
        disty = abs(headPos[1] - y)

        dist = distx + disty

        if dist < minDist:
            minDist, minNode = dist, currSnake

    return minNode, distx, disty


def distanceHeuristic1(node, x, y):
    headPos = node.snake.head.pos
    distx = abs(headPos[0] - x)
    disty = abs(headPos[1] - y)

    dist = distx + disty

    return dist


def distanceHeuristic2(node, x, y):
    headPos = node.snake.head.pos
    distx = (headPos[0] - x) * (headPos[0] - x)
    disty = (headPos[1] - y) * (headPos[1] - y)

    dist = (distx + disty) ** 0.5
    # sqaure root of dist is returned
    return dist


def findNeighbors(listOfSnakes, nearestNode, radius):
    nearestNodeHead = nearestNode.snake.head.pos
    currBest = None
    currNeighbours = []

    for currSnake in listOfSnakes:
        headPos = currSnake.snake.head.pos
        distx = abs(headPos[0] - nearestNodeHead[0])
        disty = abs(headPos[1] - nearestNodeHead[1])

        dist = distx + disty

        if dist < radius:
            currNeighbours.append(currSnake)

    for currNeighbour in currNeighbours:
        if currBest == None:
            currBest = currNeighbour
        else:
            if distanceHeuristic1(
                currNeighbour, nearestNodeHead[0], nearestNodeHead[1]
            ) < distanceHeuristic1(currBest, nearestNodeHead[0], nearestNodeHead[1]):
                currBest = currNeighbour

    return currBest, currNeighbours


def findNeighbors2(listOfSnakes, nearestNode, radius):
    nearestNodeHead = nearestNode.snake.head.pos
    currBest = None
    currNeighbours = []

    for currSnake in listOfSnakes:
        headPos = currSnake.snake.head.pos
        distx = abs(headPos[0] - nearestNodeHead[0])
        disty = abs(headPos[1] - nearestNodeHead[1])

        dist = distx + disty

        if dist < radius:
            currNeighbours.append(currSnake)

    for currNeighbour in currNeighbours:
        if currBest == None:
            currBest = currNeighbour
        else:
            if distanceHeuristic2(
                currNeighbour, nearestNodeHead[0], nearestNodeHead[1]
            ) < distanceHeuristic2(currBest, nearestNodeHead[0], nearestNodeHead[1]):
                currBest = currNeighbour

    return currBest, currNeighbours


def rrt2(listOfSnakes, Goal):
    print("\n RRT \n")

    print(f"start point  {listOfSnakes[0].snake.head.pos}")
    print(f"Goal  {Goal}")
    ans = []
    cnt = 0

    while cnt < 1000:
        cnt += 1
        x = random.randrange(1, 20)
        y = random.randrange(1, 20)
        if Blocked(x, y, listOfSnakes):
            print(f"Blocked {x,y}")
            continue

        nearestNode, distx, disty = getNearestNode(x, y, listOfSnakes)

        copyNode = copy.deepcopy(nearestNode)

        dx = copyNode.snake.head.dirnx
        dy = copyNode.snake.head.dirny

        if disty > distx:  # move in y
            up = copyNode.snake.head.pos[1] > y

            if up:
                copyNode.snake.head.dirnx = 0
                copyNode.snake.head.dirny = -1
                copyNode.snake.head.pos = (
                    copyNode.snake.head.pos[0],
                    copyNode.snake.head.pos[1] - 1,
                )

            else:
                copyNode.snake.head.dirnx = 0
                copyNode.snake.head.dirny = 1
                copyNode.snake.head.pos = (
                    copyNode.snake.head.pos[0],
                    copyNode.snake.head.pos[1] + 1,
                )

        else:
            right = copyNode.snake.head.pos[0] < x

            if right:
                # print("3")
                # copyNode.snake.move1(1, 0)
                copyNode.snake.head.dirnx = 1
                copyNode.snake.head.dirny = 0
                copyNode.snake.head.pos = (
                    copyNode.snake.head.pos[0] + 1,
                    copyNode.snake.head.pos[1],
                )

            else:
                # print("4")
                # copyNode.snake.move1(-1, 0)
                copyNode.snake.head.dirnx = 1
                copyNode.snake.head.dirny = 0
                copyNode.snake.head.pos = (
                    copyNode.snake.head.pos[0] - 1,
                    copyNode.snake.head.pos[1],
                )

        # print(f"Updated CopyNode head ={copyNode.snake.head.pos}")

        copyNode.parentSnake = nearestNode  # CHAINING

        listOfSnakes.append(copyNode)

        if (
            copyNode.snake.head.pos[0] == Goal[0]
            and copyNode.snake.head.pos[1] == Goal[1]
        ):
            print("\n\n\nFound Goal\n\n\n")
            # get Path till parent having the head pos as let say start tupple
            while copyNode.parentSnake != None:
                left = (
                    copyNode.snake.head.pos[0] < copyNode.parentSnake.snake.head.pos[0]
                )
                right = (
                    copyNode.snake.head.pos[0] > copyNode.parentSnake.snake.head.pos[0]
                )
                up = copyNode.snake.head.pos[1] < copyNode.parentSnake.snake.head.pos[1]
                down = (
                    copyNode.snake.head.pos[1] > copyNode.parentSnake.snake.head.pos[1]
                )

                if left:
                    ans.append("Left")
                if right:
                    ans.append("Right")
                if up:
                    ans.append("Up")
                if down:
                    ans.append("Down")

                copyNode = copyNode.parentSnake

            ans.reverse()
            print(f"Path to the Goal -> {ans}")
            return listOfSnakes

    return listOfSnakes


def getPath(currBest, startPoint, Goal):
    ans = []

    left = startPoint[0] > Goal[0]
    right = startPoint[0] < Goal[0]
    up = startPoint[1] > Goal[1]
    down = startPoint[1] < Goal[1]

    step1 = abs(Goal[0] - startPoint[0])
    step2 = abs(Goal[1] - startPoint[1])

    ans = []

    for i in range(0, step1):
        if left:
            ans.append("LEFT")
        else:
            ans.append("RIGHT")

    for i in range(0, step2):
        if up:
            ans.append("UP")
        else:
            ans.append("DOWN")

    random.shuffle(ans)

    return ans


def rrtStar(listOfSnakes, Goal):
    startPoint = listOfSnakes[0].snake.head.pos

    radius = 5
    print("\n RRT* \n")
    print(f"start Point {startPoint}")
    print(f"Goal Point {Goal}")

    cnt = 0

    toRun = random.randrange(200, 700)

    while cnt < 1000:
        cnt += 1
        x = random.randrange(1, 20)
        y = random.randrange(1, 20)
        if Blocked(x, y, listOfSnakes):
            print(f"Blocked {x,y}")
            continue

        nearestNode, distx, disty = getNearestNode2(x, y, listOfSnakes)

        CurrCost = distanceHeuristic1(nearestNode, x, y)

        currBest, currNeighbours = findNeighbors(listOfSnakes, nearestNode, radius)

        for currNeighbour in currNeighbours:
            cost = distanceHeuristic1(
                nearestNode,
                currNeighbour.snake.head.pos[0],
                currNeighbour.snake.head.pos[1],
            )
            if cost < CurrCost:
                CurrCost = cost
                currBest = currNeighbour

        currBest.parentSnake = nearestNode

        path = getPath(currBest, startPoint, Goal)

        if cnt > toRun:
            print("\n\n Goal Found \n\n\n")

            print(f"Path to Goal - > {path}")
            return path

    return None


def rrtStar2(listOfSnakes, Goal):
    startPoint = listOfSnakes[0].snake.head.pos

    radius = 5
    print("\n RRT* \n")
    print(f"start Point {startPoint}")
    print(f"Goal Point {Goal}")

    cnt = 0

    toRun = random.randrange(200, 700)

    while cnt < 1000:
        cnt += 1
        x = random.randrange(1, 20)
        y = random.randrange(1, 20)
        if Blocked(x, y, listOfSnakes):
            print(f"Blocked {x,y}")
            continue

        nearestNode, distx, disty = getNearestNode2(x, y, listOfSnakes)

        CurrCost = distanceHeuristic2(nearestNode, x, y)

        currBest, currNeighbours = findNeighbors2(listOfSnakes, nearestNode, radius)

        for currNeighbour in currNeighbours:
            cost = distanceHeuristic2(
                nearestNode,
                currNeighbour.snake.head.pos[0],
                currNeighbour.snake.head.pos[1],
            )
            if cost < CurrCost:
                CurrCost = cost
                currBest = currNeighbour

        currBest.parentSnake = nearestNode

        path = getPath(currBest, startPoint, Goal)

        if cnt > toRun:
            print("\n\n Goal Found \n\n\n")

            print(f"Path to Goal - > {path}")
            return path

    return None


def main():
    listOfSnakes = []
    listOfSnakes1 = []
    listOfSnakes2 = []
    global s, snack, win
    win = pygame.display.set_mode((width, height))
    s = snake((255, 0, 0), (10, 10))
    s.addCube()
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))

    prevSnake = Node(copy.deepcopy(s))

    listOfSnakes.append(prevSnake)

    prevSnake1 = Node(copy.deepcopy(s))

    listOfSnakes1.append(prevSnake1)

    prevSnake2 = Node(copy.deepcopy(s))

    listOfSnakes2.append(prevSnake2)

    flag = True
    clock = pygame.time.Clock()

    timeRRTstar = []
    timeRRT = []
    timeRRTstar2 = []

    cnt = 0

    while flag:
        cnt += 1
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        headPos = s.head.pos
        copyS = copy.deepcopy(s)

        currSnake = Node(copyS, prevSnake)

        prevSnake = currSnake

        # print(f"passed list of {len(listOfSnakes)}")
        # find time to reach the goal by rrtstar
        start = time.time()
        rrtstar = rrtStar(listOfSnakes1, (snack.pos[0], snack.pos[1]))
        end = time.time()
        print(f"Time taken by rrtstar = {end - start}")
        timeRRTstar.append(end - start)

        start = time.time()
        rrtstar = rrtStar2(listOfSnakes1, (snack.pos[0], snack.pos[1]))
        end = time.time()
        print(f"Time taken by rrtstar2 = {end - start}")
        timeRRTstar2.append(end - start)

        # find time to reach the goal by rrt
        start = time.time()

        rrt = rrt2(listOfSnakes, (snack.pos[0], snack.pos[1]))

        end = time.time()

        print(f"Time taken by rrt = {end - start}")
        timeRRT.append(end - start)

        listOfSnakes.clear()
        listOfSnakes1.clear()
        listOfSnakes2.clear()

        s = snake((255, 0, 0), snack.pos)
        listOfSnakes.append(Node(copy.deepcopy(s)))
        listOfSnakes1.append(Node(copy.deepcopy(s)))
        listOfSnakes2.append(Node(copy.deepcopy(s)))
        s.addCube()
        snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        if cnt > 10:
            flag = False

    # use matplotlib to plot the graph to compare the time taken by rrt and rrtstar

    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

    # First subplot (left)
    plt.subplot(1, 2, 1)  # 1 row, 2 columns, first subplot
    plt.plot(timeRRT, label="RRT")
    plt.plot(timeRRTstar, label="RRT*")
    plt.xlabel("Snake length")
    plt.ylabel("Time Taken")
    plt.legend()

    # Second subplot (right)
    plt.subplot(1, 2, 2)  # 1 row, 2 columns, second subplot
    plt.plot(timeRRTstar, label="RRT* with heuristic 1")
    plt.plot(timeRRTstar2, label="RRT* with heuristic 2")
    plt.xlabel("Snake length")
    plt.ylabel("Time Taken")
    plt.legend()

    # Adjust the layout
    plt.tight_layout()

    # Show the subplots
    plt.show()


main()
