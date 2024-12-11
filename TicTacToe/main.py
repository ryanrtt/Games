import pygame
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
PASTEL_GREEN = (119, 221, 119)
PASTEL_RED = (255, 182, 193) 

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

class GridSlot:
    type = None
    def __init__(self, pos, collide):
        self.pos = pos
        self.collide = collide
    
    def drawIcon(self, mousePos, playerOneTurn):
        if self.type == None:
            if self.collide.collidepoint(mousePos):
                pygame.draw.rect(screen, LIGHT_GREY, self.collide)
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
    global gameStart, lineNumber
    while lineNumber < 4:
        pygame.draw.line(screen, BLACK, lineStart[lineNumber], lineEnd[lineNumber], 10)
        pygame.display.flip()
        pygame.time.delay(250)
        lineNumber += 1
    gameStart = True

def setGrid():
    for i in range(3):
        for j in range (3):
            grid[i][j] = GridSlot((i, j), pygame.Rect((j * 200) + 110, (i * 200) + 110, 180, 180))

def checkWin():
    for i in range(3):   
        if grid[i][0].type == grid[i][1].type == grid[i][2].type: 
            if grid[i][0].type != None: return True
        if grid[0][i].type == grid[1][i].type == grid[2][i].type: 
            if grid[0][i].type != None: return True
        if grid[0][0].type == grid[1][1].type == grid[2][2].type:
            if grid[0][0].type != None: return True
        if grid[0][2].type == grid[1][1].type == grid[2][0].type:
            if grid[0][2].type != None: return True
    return False

def checkWin(slot):
    global grid
    if slot.type == None: return False
    row = slot.pos[0]
    column = slot.pos[1]

    if grid[row][0].type == grid[row][1].type == grid[row][2].type: return True
    if grid[0][column].type == grid[1][column].type == grid[2][column].type: return True

    if slot.pos in ((0, 0), (2, 0), (2, 2), (0, 2), (1, 1)) and grid[1][1].type != None:
        if grid[0][0].type == grid[1][1].type == grid[2][2].type: return True
        if grid[0][2].type == grid[1][1].type == grid[2][0].type: return True
        
    return False

def win():
    print("game won")
    input()

def main():
    global running, gameStart, playerOneTurn
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        mousePos = pygame.mouse.get_pos()

        if gameStart:
            for row in grid:
                for slot in row:
                    turn = slot.drawIcon(mousePos, playerOneTurn)
                    if turn in (True, False):
                        playerOneTurn = turn    
                        if checkWin(slot):
                            print("game won")         
        else:
            drawGrid()
            setGrid()
  
        pygame.display.flip()

main()
pygame.quit() 