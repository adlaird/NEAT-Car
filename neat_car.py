import pygame
import os
import neat
# import pickle

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NEAT Car")

class Car:

    def __init__(self, x, y):
        self.x = x
        self.y = y

def test_genomes(gens, config):
    global WIN
    win = WIN

    rect_position = (150, 200, 20, 20)
    radius = 10
    velocity = 5
    win_circle_position = (250, 100)
    x_position = 50
    y_position = 5

    networks = []
    cars = []
    genomes = []

    for genome_id, genome in gens:
        genome.fitness = 0

        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)

        cars.append(Car(50, 50))

        genomes.append(genome)

    score = 0

    keep_running = True
    while keep_running and len(cars) > 0:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_running = False
                pygame.quit()
                quit()
                break
        
        for index, car in enumerate(cars):
            genomes[index].fitness += 1

            distance_top = 5
            distance_right = 5
            distance_bottom = 5
            distance_left = 7
            distance_to_finish = 8

            output = networks[index].activate((distance_top, distance_right, distance_bottom, distance_left, distance_to_finish))

            # UP
            if output[0] == 1:
                car.y -= velocity
            
            # RIGHT
            if output[1] == 1:
                car.x += velocity

            # DOWN
            if output[2] == 1:
                car.y += velocity

            # LEFT
            if output[3] == 1:
                car.x -= velocity
        
            color = (0, 255, 0)

            if car.y - radius < rect_position[1] + rect_position[3] and car.y + radius > rect_position[1]:
                if car.x + radius > rect_position[0] and car.x - radius < rect_position[0] + rect_position[2]:
                    color = (255, 0, 0)
            
            if car.x == win_circle_position[0] and car.y == win_circle_position[1]:
                print('win')

            if car.x > SCREEN_WIDTH - radius or car.x < 0 + radius or car.y > SCREEN_WIDTH - radius or car.y < 0 + radius:
                cars.pop(index)
                genomes.pop(index)
                networks.pop(index)

        win.fill((255, 255, 255))
        
        pygame.draw.rect(win, (0, 0, 255), rect_position)
        pygame.draw.circle(win, (0, 255, 0), win_circle_position, radius)

        for index, car in enumerate(cars):
            pygame.draw.circle(win, color, (car.x, car.y), radius)

        pygame.display.update()
    # COLOR = (0, 255, 0)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    pop = neat.Population(config)
    
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(test_genomes, 2)

    # print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)