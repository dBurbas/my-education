import pygame
import sys
from core.game import Game

pygame.init()

screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Python Fall Block Game")

clock = pygame.time.Clock()

dark_blue = (44, 44, 127)
pygame.key.set_repeat(200, 50)
game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.game_over:
                game.game_over = False
                game.reset()
            else:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_RIGHT:
                    game.move_right()
                if event.key == pygame.K_DOWN:
                    game.move_down()
                if event.key == pygame.K_UP:
                    game.rotate()
        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()

    screen.fill(dark_blue)
    game.draw(screen)

    # if j < 10 and i < 20:
    #     if j > 0:
    #         grid._grid[i][j - 1] = 0
    #     grid._grid[i][j] = random.choice(range(8))
    # elif i < 20:
    #     i += 1
    #     j = 0
    # j += 1
    pygame.display.update()
    clock.tick(120)
