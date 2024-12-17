import pygame
import random
from enum import Enum
from typing import List

WIDTH: int = 1280
HEIGHT: int = 720

CELL_WIDTH: int = 32
CELL_HEIGHT: int = 32

NUM_COLUMNS: int 
NUM_ROWS: int

WHITE: tuple = (255, 255, 255)
BLACK: tuple = (0, 0, 0)

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
    -1 : 8,
    0 : 9,
    1 : 0,
    2 : 1,
    3 : 2,
    4 : 3,
    5 : 4, 
    6 : 5,
    7 : 6,
    8 : 7,
    'F' : 10,
    'M': 13
}

class Difficulty(Enum): 
    EASY: tuple = ((9, 9), 10)
    MEDIUM: tuple = ((16, 16), 40)
    HARD: tuple = ((30, 16), 99)

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

        x = self.coordinate[0]
        y = self.coordinate[1]

        for dir in DIRECTIONS:
            if x + dir[0] > -1 and x + dir[0] < NUM_COLUMNS and y + dir[1] > -1 and y + dir[1] < NUM_ROWS:
                if grid[y + dir[1]][x + dir[0]].type == 'M': count += 1  
        return count

screen: pygame.surface
clock: pygame.time = pygame.time.Clock()
board: List[List[Cell]] 
tiles_sheet = pygame.image.load('Assets/tiles.png')
tiles: List[pygame.Surface] = []
mines: List[Cell] = []

running: bool = True

def initDisplay() -> None:
    global screen
    pygame.init()
    pygame.display.set_caption("Minesweeper")
    pygame.display.set_icon(pygame.image.load('Assets' + '/icon.webp'))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    pygame.display.flip()

    getTileSprites()

def getTileSprites() -> None:
    global tiles
    for i in range(1, -1, -1):
        for j in range(8):
            select = pygame.Rect(j * 16, i * 16, 16, 16)

            tile = tiles_sheet.subsurface(select)
            tiles.append(pygame.transform.smoothscale_by(tile, 2))

def setupGame(difficulty: str) -> None:
    global grid, NUM_ROWS, NUM_COLUMNS
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

    NUM_ROWS = size[1]
    NUM_COLUMNS = size[0]

    position: tuple = ((WIDTH - (NUM_COLUMNS * CELL_WIDTH)) / 2, (HEIGHT - (NUM_ROWS * CELL_HEIGHT)) / 2)

    grid = [[Cell((cell, row), pygame.Rect((cell * CELL_WIDTH) + position[0], (row * CELL_HEIGHT) + position[1], CELL_WIDTH, CELL_HEIGHT)) for cell in range(NUM_COLUMNS)] for row in range(NUM_ROWS)]    
    setMines(size, mines)
    
    for row in grid:
        for cell in row:
            if cell.type != 'M':
                cell.type = cell.countMines()

    for row in grid:
        print(" ".join(f"{str(cell.type):<2}" for cell in row))

def setMines(size: tuple, nunMines: int):
    for m in range(nunMines):
        random_x = random.randrange(0, size[0])
        random_y = random.randrange(0, size[1])
        random_cell = grid[random_y][random_x]
        
        if random_cell.type != 'M':
            random_cell.type = 'M'
            mines.append(random_cell)

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

def floodFill(coordinate: tuple) -> None:
    x_cord: int = coordinate[0]
    y_cord: int = coordinate[1]
    if x_cord <= -1 or x_cord >= NUM_COLUMNS: return
    if y_cord <= -1 or y_cord >= NUM_ROWS: return

    if grid[y_cord][x_cord].flagged: return
    if grid[y_cord][x_cord].revealed: return
    if grid[y_cord][x_cord].type not in range(9): return 

    grid[y_cord][x_cord].revealed = True

    floodFill((x_cord + 1, y_cord))
    floodFill((x_cord - 1, y_cord)) 
    floodFill((x_cord, y_cord + 1))
    floodFill((x_cord, y_cord - 1))

def autoFill(coordinate: tuple) -> None:
    pass

def main() -> None:
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_a:
                    for row in grid:
                        for cell in row:
                            cell.revealed = True if not cell.revealed else False
        updateBoard()
    

if __name__ == '__main__':
    initDisplay()
    setupGame('M')
    main()