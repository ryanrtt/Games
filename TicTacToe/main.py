import pygame
from gridslot import GridSlot
    
WIDTH, HEIGHT = 800, 800
lineStart = [(300, 100), (500, 100), (100,300), (100, 500)]
lineEnd = [(300, 700), (500, 700), (700,300), (700,500)]
grid = [
    [0,1,2],
    [3,4,5],
    [6,7,8]
]

pygame.display.set_caption("Tic Tac Toe")  
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))

screen = pygame.display.set_mode((WIDTH, HEIGHT))  
screen.fill((255, 255, 255))

clock = pygame.time.Clock()

for i in range(3):
    for j in range (3):
        grid[i][j] = GridSlot((i, j), pygame.Rect((j * 200) + 110, (i * 200) + 110, 180, 180))

pygame.init()

running = True
gameStart = False
lineNumber = 0

grid[0][0].type = "LOl"

def main():
    global running, lineNumber
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        if lineNumber < 4:
            pygame.draw.line(screen, (0, 0, 0), lineStart[lineNumber], lineEnd[lineNumber], 10)
            lineNumber += 1
            pygame.time.delay(250)
            gameStart = False
        else:
            gameStart = True

        mousePos = pygame.mouse.get_pos()
    
        if gameStart:
            for row in grid:
                for slot in row:
                    if slot.collide.collidepoint(mousePos) and slot.type == None:
                        pygame.draw.rect(screen, (211, 211, 211), slot.collide)
                    else:
                        pygame.draw.rect(screen, (255, 255, 255), slot.collide)

        pygame.display.flip()

main()
pygame.quit() 