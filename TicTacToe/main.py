import pygame
import threading
import queue
from pygame import mixer

mixer.init()  
mixer.music.load("Assets/click.mp3")   
mixer.music.set_volume(0.7) 
  
WIDTH, HEIGHT = 800, 800
lineStart = [(300, 100), (500, 100), (100,300), (100, 500)]
lineEnd = [(300, 700), (500, 700), (700,300), (700,500)]

grid = [["" for _ in range(3)] for _ in range(3)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (211, 211, 211)
PASTEL_RED = (255, 182, 193) 
PASTEL_GREEN = (119, 221, 119)
PASTEL_BLUE = (174, 198, 207)

MAX_FPS = 60

pygame.display.set_caption("Tic Tac Toe")  
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))

nought = pygame.image.load("Assets/nought.png")
cross = pygame.image.load("Assets/cross.png")

screen = pygame.display.set_mode((WIDTH, HEIGHT))  
screen.fill(WHITE)
pygame.display.flip()

clock = pygame.time.Clock()

pygame.init()

running = True
gameStart = False
lineNumber = 0
playerOneTurn = True
gameWon = False

class GridSlot:
    type = None
    def __init__(self, pos, collide):
        self.pos = pos
        self.collide = collide
    
    def drawIcon(self, mousePos, playerOneTurn):
        if self.type == None:
            if self.collide.collidepoint(mousePos):
                if playerOneTurn:
                    crossTransparent = cross.convert_alpha()
                    crossTransparent.set_alpha(20)
                    screen.blit(crossTransparent, self.collide)
                else:
                    noughtTransparent = nought.convert_alpha()
                    noughtTransparent.set_alpha(20)
                    screen.blit(noughtTransparent, self.collide)
                if pygame.mouse.get_pressed()[0]:
                    mixer.music.play()
                    if playerOneTurn:
                        pygame.draw.rect(screen, WHITE, self.collide)
                        screen.blit(cross, self.collide)
                        self.type = 'X'                      
                    else:
                        pygame.draw.rect(screen, WHITE, self.collide)
                        screen.blit(nought, self.collide)
                        self.type = 'O' 
                    return False if playerOneTurn else True                         
            else:
                pygame.draw.rect(screen, WHITE, self.collide)

def drawGrid():
    pygame.time.delay(100)
    lineNumber = 0
    while (lineNumber < 4):
        line = threading.Thread(target = drawLineAnimation, args = (BLACK, lineStart[lineNumber], lineEnd[lineNumber], 10, 0.015))
        line.start()
        lineNumber += 1
        pygame.time.delay(250)
    pygame.time.delay(800)

def setGrid():
    for i in range(3):
        for j in range (3):
            grid[i][j] = GridSlot((i, j), pygame.Rect((j * 200) + 110, (i * 200) + 110, 180, 180))

def checkWin(slot):
    if slot.type == None: return False
    row = slot.pos[0]
    column = slot.pos[1]

    rowWin = grid[row][0].type == grid[row][1].type == grid[row][2].type
    columnWin = grid[0][column].type == grid[1][column].type == grid[2][column].type

    if rowWin:
        drawLineAnimation(LIGHT_GREY, (grid[row][0].collide[0], grid[row][0].collide[1] + 90), (grid[row][2].collide[0] + 180, grid[row][2].collide[1] + 90), 7, 0.01)
    if columnWin:
        drawLineAnimation(LIGHT_GREY, (grid[0][column].collide[0] + 90, grid[0][column].collide[1]), (grid[2][column].collide[0] + 90, grid[2][column].collide[1] + 180), 7, 0.01)

    leadingDiagonalWin = False
    antiDiagonalWin = False
    if slot.pos in ((0, 0), (2, 0), (2, 2), (0, 2), (1, 1)) and grid[1][1].type != None:
        leadingDiagonalWin = grid[0][0].type == grid[1][1].type == grid[2][2].type
        antiDiagonalWin = grid[2][0].type == grid[1][1].type == grid[0][2].type

        if leadingDiagonalWin:
            drawLineAnimation(LIGHT_GREY, (grid[0][0].collide[0], grid[0][0].collide[1]), (grid[2][2].collide[0] + 180, grid[2][2].collide[1] + 180), 7, 0.01)
        if antiDiagonalWin:
            drawLineAnimation(LIGHT_GREY, (grid[2][0].collide[0], grid[2][0].collide[1] + 180), (grid[0][2].collide[0] + 180, grid[0][2].collide[1]), 7, 0.01)
    
    return rowWin or columnWin or leadingDiagonalWin or antiDiagonalWin

def checkDraw():
    for row in grid:
        for slot in row:
            if slot.type == None:
                return False
    return True

def easeInOutCubic(p):
    return 4 * (p ** 3) if p < 0.5 else 1 - ((-2 * p + 2) ** 3) / 2

def easeInQuart(p):
    return p ** 4

def drawLineAnimation(colour, start, end, thickness, speed):
    p = 0
    while p <= 1:
        clock.tick(MAX_FPS)
        pygame.display.flip()
        pygame.draw.line(screen, colour, start, (start[0] + (end[0] - start[0]) * easeInOutCubic(p), start[1] + (end[1] - start[1]) * easeInOutCubic(p)), thickness)
        p += speed
    return True

def gameWin():
    global gameStart, gameWon
    gameStart = False
    gameWon = False

    pygame.time.delay(750)
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(WHITE)

    alpha = 0
    while (alpha <= 1):
        clock.tick(MAX_FPS)
        fade.set_alpha(easeInQuart(alpha) * 256)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        alpha += 0.005

def main():
    global running, gameStart, playerOneTurn, gameWon
    while running:
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        mousePos = pygame.mouse.get_pos()

        if gameStart and not gameWon:
            for row in grid:
                for slot in row:
                    turn = slot.drawIcon(mousePos, playerOneTurn)
                    if turn in (True, False):
                        playerOneTurn = turn    
                        gameWon = checkWin(slot) or checkDraw() 
        elif not gameWon:
            drawGrid()
            setGrid()
            gameStart = True

        pygame.display.flip()

        if gameWon:
            gameWin()
            main()

main()
pygame.quit() 