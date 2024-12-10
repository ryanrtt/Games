import pygame

WIDTH, HEIGHT = 800, 800

def main():
    pygame.init()

    img = pygame.image.load('TicTacToe/icon.png')
    pygame.display.set_icon(img)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))  
    pygame.display.set_caption("Tic Tac Toe")  

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        screen.fill((255, 255, 255))

        pygame.display.flip()

    pygame.quit() 









main()