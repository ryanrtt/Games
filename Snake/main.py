import pygame
import random
from typing import List
from collections import deque

# Display constants
WIDTH: int = 900
HEIGHT: int = 600
NUM_COLUMNS: int = 30
NUM_ROWS: int = 20
CELL_WIDTH: int = WIDTH / NUM_COLUMNS
CELL_HEIGHT: int = HEIGHT / NUM_ROWS
PADDING: int = 5

# Colours
WHITE: tuple = (255, 255, 255)
LIGHT_GREY: tuple = (211, 211, 211)
ORANGE: tuple = (255, 165, 0)
BLACK: tuple = (0, 0, 0)
RED: tuple = (255, 0, 0)
CELL_COLOUR = {
    None : BLACK,
    'F' : ORANGE,
    'S' : WHITE,
    'X' : RED
}

# Movement
MOVES = {
    pygame.K_w : (0, -1),
    pygame.K_a : (-1, 0),
    pygame.K_s : (0, 1),
    pygame.K_d : (1, 0)
}
REVERSE_MOVES = {
    pygame.K_w : pygame.K_s,
    pygame.K_a : pygame.K_d,
    pygame.K_s : pygame.K_w,
    pygame.K_d : pygame.K_a,
    None: None
}

# Class declaration for each cell within the grid
class Cell:
    type: str = None
    position: pygame.Rect
    coordinate: tuple 

    def __init__(self, coordinate: tuple, position: tuple):
        self.coordinate = coordinate
        self.position = position

# Global variables
screen: pygame.surface
clock: pygame.time = pygame.time.Clock()
grid: List[List[Cell]] = [[Cell((j, i), pygame.Rect((j * CELL_WIDTH) + PADDING, (i * CELL_HEIGHT) + PADDING, CELL_WIDTH - (2 * PADDING), CELL_HEIGHT - (2 * PADDING))) for j in range(NUM_COLUMNS)] for i in range(NUM_ROWS)]

running: bool = True
alive: bool = True
foodSpawned: bool = False
lastMove: pygame.key = None
snake: deque[Cell] = deque()

def initDisplay() -> None:
    global screen
    pygame.display.set_caption("Snake")
    pygame.display.set_icon(pygame.image.load('Assets/snake.png'))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BLACK)
    pygame.display.flip()

def initSnake() -> None:
    head: Cell = grid[random.randrange(3, NUM_ROWS - 3)][random.randrange(3, NUM_COLUMNS - 3)]
    head.type = 'S'
    snake.append(head)
        
def setupGame() -> None:
    pygame.init()
    initDisplay()
    initSnake()
    pygame.display.flip()

def endGame() -> None:
    while len(snake):
        snake.popleft().type = 'X'
        updateBoard()
        pygame.time.delay(250)

def resetGame() -> None:
    for row in grid:
        for cell in row:
            cell.type = None
    snake.clear()
    updateBoard()

def spawnFood() -> None:
    global foodSpawned
    while True:
        food: Cell = grid[random.randrange(0, NUM_ROWS)][random.randrange(0, NUM_COLUMNS)]
        if food.coordinate not in [body.coordinate for body in snake]:
            break
    food.type = 'F'
    foodSpawned = True

def updateBoard() -> None:
    for row in grid:
        for cell in row:
            pygame.draw.rect(screen, CELL_COLOUR[cell.type], cell.position)
    pygame.display.flip()

def updateSnake(direction: pygame.event) -> None:
    global alive, foodSpawned

    head: Cell = snake[0]
    headCoord: tuple = head.coordinate
    new_head_x: int = headCoord[0] + MOVES[direction][0]
    new_head_y: int = headCoord[1] + MOVES[direction][1]

    if new_head_x <= -1 or new_head_x >= NUM_COLUMNS or new_head_y <= -1 or new_head_y >= NUM_ROWS:
        head.type = 'X'
        alive = False
        return
    
    nextCell: Cell = grid[new_head_y][new_head_x]

    if nextCell.type == 'F':
        nextCell.type = 'S'
        snake.appendleft(nextCell)      
        foodSpawned = False
        return
    
    if nextCell.type == 'S':
        nextCell.type = 'X'
        snake[len(snake) - 1].type = None
        alive = False

    if nextCell.type == None:
        nextCell.type = 'S'
        snake.appendleft(nextCell)     

    snake.pop().type = None

def main() -> None:
    global running, foodSpawned, lastMove
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break 

            if event.type == pygame.KEYDOWN and event.key != REVERSE_MOVES[lastMove]:
                if event.key in [key for key in MOVES]:
                    lastMove = event.key
                    break
        
        if lastMove != None:   
            updateSnake(lastMove)
            pygame.time.delay(100)
        
        if not alive:
            running = False
            break
        
        if not foodSpawned: 
            spawnFood()

        updateBoard()

if __name__ == '__main__':
    setupGame()
    main()
    if not alive: endGame()
    resetGame()