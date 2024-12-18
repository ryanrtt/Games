import pygame
import random
import sys
from pygame import mixer
from enum import Enum
from typing import List

WIDTH: int 
HEIGHT: int 

NUM_COLUMNS: int 
NUM_ROWS: int
NUM_MINES : int

CELL_WIDTH: int = 32
CELL_HEIGHT: int = 32

DIRECTIONS = (
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1)
)

TILES = {
    -1 : 8, # unrevealed square
    0 : 9, # revealed square
    1 : 0, # 1 cell
    2 : 1, # 2 cell
    3 : 2, # 3 cell
    4 : 3, # 4 cell
    5 : 4, # 5 cell
    6 : 5, # 6 cell
    7 : 6, # 7 cell
    8 : 7, # 8 cell
    'F' : 10, # flagged
    'M': 13, # mine
    '!M' : 14, # clicked mine 
    'XM' : 15 # incorrect mine
}

class Difficulty(Enum): 
    EASY: tuple = ((9, 9), 10)
    MEDIUM: tuple = ((16, 16), 40)
    HARD: tuple = ((30, 16), 99)
    EXTREME: tuple = ((30, 30), 199)

class Cell:
    revealed: bool = False
    flagged: bool = False
    type: str = None
    position: pygame.Rect
    coordinate: tuple 

    def __init__(self, coordinate: tuple, position: pygame.Rect):
        self.coordinate = coordinate
        self.position = position

    def countMines(self) -> int:
        count: int = 0

        x: int = self.coordinate[0]
        y: int = self.coordinate[1]

        for dir in DIRECTIONS:
            if not outOfBounds(x + dir[0], y + dir[1]):
                if grid[y + dir[1]][x + dir[0]].type == 'M': count += 1  
        return count
    
    def countFlags(self) -> int:
        count: int = 0

        x: int = self.coordinate[0]
        y: int = self.coordinate[1]

        for dir in DIRECTIONS:
            if not outOfBounds(x + dir[0], y + dir[1]):
                if grid[y + dir[1]][x + dir[0]].flagged: count += 1  
        return count

screen: pygame.surface
board: List[List[Cell]] 
gameStart: bool
tiles_sheet: pygame.surface
tiles: List[pygame.Surface] 
safe_tiles: List[Cell] 
mines: List[Cell] 
flags: List[Cell]
running: bool
alive : bool

click: str
lose: str
win: str

def initVariables() -> None:
    global tiles_sheet, gameStart, running, alive, tiles, safe_tiles, mines, flags, click, win, lose

    tiles_sheet = pygame.image.load('Assets/tiles.png')

    gameStart = False
    running = True
    alive = True
    
    tiles = []
    safe_tiles = []
    mines = []
    flags = []

    click = 'Assets/click.mp3'  
    win = 'Assets/win.mp3'
    lose = 'Assets/explosion.wav'

def setupGame(difficulty: str) -> None:
    global grid, NUM_ROWS, NUM_COLUMNS, NUM_MINES, WIDTH, HEIGHT

    mixer.init() 
    mixer.music.set_volume(0.7)

    mines: int
    size: tuple

    if difficulty == 'E':
        size = Difficulty.EASY.value[0]
        mines = Difficulty.EASY.value[1]
    elif difficulty == 'M':
        size = Difficulty.MEDIUM.value[0]
        mines = Difficulty.MEDIUM.value[1]
    elif difficulty == 'H':
        size = Difficulty.HARD.value[0]
        mines = Difficulty.HARD.value[1]
    elif difficulty == 'EX':
        size = Difficulty.EXTREME.value[0]
        mines = Difficulty.EXTREME.value[1]
    else:
        raise ValueError("Invalid Difficulty")

    NUM_ROWS = size[1]
    NUM_COLUMNS = size[0]
    NUM_MINES = mines

    WIDTH = CELL_WIDTH * NUM_COLUMNS    
    HEIGHT = CELL_HEIGHT * NUM_ROWS  
 
    grid = [[Cell((cell, row), pygame.Rect(cell * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)) for cell in range(NUM_COLUMNS)] for row in range(NUM_ROWS)]  

    initVariables()
    initDisplay()

def initDisplay() -> None:
    global screen

    pygame.init()
    pygame.display.set_caption("Minesweeper")
    pygame.display.set_icon(pygame.image.load('Assets/icon.webp'))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    getTileSprites()

def getTileSprites() -> None:
    global tiles
    for i in range(1, -1, -1):
        for j in range(8):
            select = pygame.Rect(j * 16, i * 16, 16, 16)

            tile = tiles_sheet.subsurface(select)
            tiles.append(pygame.transform.scale_by(tile, 2))

def setMines(numMines: int) -> None:
    for _ in range(numMines):
        random_x: int = random.randrange(0, NUM_COLUMNS)
        random_y: int = random.randrange(0, NUM_ROWS)
        random_cell: Cell = grid[random_y][random_x]
        
        if random_cell.type != 'M' and random_cell not in safe_tiles:
            random_cell.type = 'M'
            mines.append(random_cell)

def setGrid() -> None:
    setMines(NUM_MINES)
    for row in grid:
        for cell in row:
            if cell.type != 'M':
                cell.type = cell.countMines()

def mouseClick(mousePos: tuple, button: int) -> None:
    global gameStart
    mouse_x = (mousePos[0] - (WIDTH - (NUM_COLUMNS * CELL_WIDTH)) // 2) // CELL_WIDTH
    mouse_y = (mousePos[1] - (HEIGHT - (NUM_ROWS * CELL_HEIGHT)) // 2) // CELL_HEIGHT

    cell = grid[mouse_y][mouse_x]

    if button == 1 and not cell.flagged:   
        if not gameStart:
            firstClick(cell)
            gameStart = True

        if cell.type == 0: floodFill((mouse_x, mouse_y))
        elif cell.type == 'M':          
            cell.type = '!M'
            endGame()
        elif cell.type in range(1, 9) and cell.type == cell.countFlags(): autoFill((mouse_x, mouse_y))
        cell.revealed = True
    
    elif button == 3 and not cell.revealed:
        if not cell.flagged:
            cell.flagged = True
            flags.append(cell)
        else:
            cell.flagged = False
            flags.pop()

def outOfBounds(x: int, y: int) -> bool:
    return x < 0 or x > NUM_COLUMNS - 1 or y < 0 or y > NUM_ROWS - 1

def firstClick(cell: Cell) -> None:
    cell.type = 0
    x: int = cell.coordinate[0]
    y: int = cell.coordinate[1]

    for dir in DIRECTIONS:
        if not outOfBounds(x + dir[0], y + dir[1]):
            safe_tiles.append(grid[y + dir[1]][x + dir[0]])
    
    safe_tiles.append(grid[y][x])
    setGrid()

def floodFill(coordinate: tuple) -> None:
    x: int = coordinate[0]
    y: int = coordinate[1]
    if outOfBounds(x, y): return

    cell = grid[y][x]

    if cell.flagged: return  
    if cell.revealed: return
    if cell.type == 'M': return 

    grid[y][x].revealed = True

    if cell.type in range(1, 9): return

    for dir in DIRECTIONS:
        floodFill((x + dir[0], y + dir[1]))

def autoFill(coordinate: tuple) -> None:
    x: int = coordinate[0]
    y: int = coordinate[1]

    for dir in DIRECTIONS:
        if not outOfBounds(x + dir[0], y + dir[1]):
            cell = grid[y + dir[1]][x + dir[0]]
            if not cell.flagged:
                if cell.type == 0: floodFill((x + dir[0], y + dir[1]))
                cell.revealed = True
            if cell.type == 'M' and not cell.flagged:
                cell.type = '!M'
                endGame()
                return

def updateBoard() -> None:
    for row in grid:
        for cell in row:
            if cell.flagged:
                screen.blit(tiles[TILES['F']], cell.position)
            elif not cell.revealed:
                screen.blit(tiles[TILES[-1]], cell.position)
            else:
                screen.blit(tiles[TILES[cell.type]], cell.position)
    pygame.display.flip()

def printBoard() -> None:
    for row in grid:
        print(" ".join(f"{str(cell.type):<2}" for cell in row))

def gameWin() -> bool:
    for row in grid:
        for cell in row:
            if cell.type in range(9) and not cell.revealed: return False
    return True
   
def endGame() -> None:
    global alive

    for cell in flags:
        if cell.flagged and cell.type != 'M':
            cell.flagged = False
            cell.type = 'XM'
            cell.revealed = True

    for mine in mines:
        mine.revealed = True

    alive = False

    pygame.mixer.music.load(lose)
    mixer.music.play()

def main() -> None:
    global running, alive

    while running:
        mousePos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    sys.exit()
 
            if event.type == pygame.MOUSEBUTTONUP and alive:
                mouseClick(mousePos, event.button)
                if gameWin() and alive:
                    alive = False
                    pygame.mixer.music.load(win)
                    mixer.music.play()

        updateBoard()
      
if __name__ == '__main__':
    setupGame('M')
    main()