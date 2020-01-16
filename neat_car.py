import pygame
import os
import neat
import pickle

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NEAT Car")



def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    
    X_POSITION = 50
    Y_POSITION = 50
    RADIUS = 10
    VELOCITY = 5
    COLOR = (0, 255, 0)

    RECT_POSITION = (150, 200, 20, 20)
    WIN_CIRCLE_POSITION = (250, 100)

    RUN = True
    while RUN:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
        
        COLOR = (0, 255, 0)

        if Y_POSITION - RADIUS < RECT_POSITION[1] + RECT_POSITION[3] and Y_POSITION + RADIUS > RECT_POSITION[1]:
            if X_POSITION + RADIUS > RECT_POSITION[0] and X_POSITION - RADIUS < RECT_POSITION[0] + RECT_POSITION[2]:
                COLOR = (255, 0, 0)
        
        if X_POSITION == WIN_CIRCLE_POSITION[0] and Y_POSITION == WIN_CIRCLE_POSITION[1]:
            print('win')

        KEYS = pygame.key.get_pressed()

        if KEYS[pygame.K_LEFT]:
            X_POSITION -= VELOCITY

        if KEYS[pygame.K_RIGHT]:
            X_POSITION += VELOCITY

        if KEYS[pygame.K_UP]:
            Y_POSITION -= VELOCITY

        if KEYS[pygame.K_DOWN]:
            Y_POSITION += VELOCITY

        if X_POSITION > SCREEN_WIDTH - RADIUS:
            X_POSITION = SCREEN_WIDTH - RADIUS
        elif X_POSITION < 0 + RADIUS:
            X_POSITION = 0 + RADIUS

        if Y_POSITION > SCREEN_WIDTH - RADIUS:
            Y_POSITION = SCREEN_WIDTH - RADIUS
        elif Y_POSITION < 0 + RADIUS:
            Y_POSITION = 0 + RADIUS

        WIN.fill((255, 255, 255))
        pygame.draw.circle(WIN, COLOR, (X_POSITION, Y_POSITION), RADIUS)
        pygame.draw.rect(WIN, (0, 0, 255), RECT_POSITION)
        pygame.draw.circle(WIN, (0, 255, 0), WIN_CIRCLE_POSITION, RADIUS)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)