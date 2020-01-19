import pygame
import random
import os
import neat
import math
import pickle

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

CAR_RADIUS = 10
WIN_CIRCLE_POSITION = (475, 25)

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NEAT Car")

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))

    def get_distance_top(self):
        if (self.x <= 100):
            return self.y - CAR_RADIUS - 400
        elif (self.x <= 200):
            return self.y - CAR_RADIUS - 300
        elif (self.x <= 300):
            return self.y - CAR_RADIUS - 200
        elif (self.x <= 400):
            return self.y - CAR_RADIUS - 100
        else:
            return self.y - CAR_RADIUS

    def get_distance_right(self):
        if (self.y <= 50):
            return 500 - (self.x + CAR_RADIUS)
        elif (self.y <= 150):
            return 450 - (self.x + CAR_RADIUS)
        elif (self.y <= 250):
            return 350 - (self.x + CAR_RADIUS)
        elif (self.y <= 350):
            return 250 - (self.x + CAR_RADIUS)
        elif (self.y <= 450):
            return 150 - (self.x + CAR_RADIUS)
        else:
            return 50 - (self.x + CAR_RADIUS)
    
    def get_distance_bottom(self):
        if (self.x <= 50):
            return 500 - self.y + CAR_RADIUS
        elif (self.x <= 150):
            return 400 - self.y + CAR_RADIUS
        elif (self.x <= 250):
            return 300 - self.y + CAR_RADIUS
        elif (self.x <= 350):
            return 200 - self.y + CAR_RADIUS
        elif (self.x <= 450):
            return 100 - self.y + CAR_RADIUS
        else:
            return self.y + CAR_RADIUS
    
    def get_distance_left(self):
        if (self.y <= 50):
            return self.x - CAR_RADIUS - 350
        elif (self.y <= 150):
            return self.x - CAR_RADIUS - 250
        elif (self.y <= 250):
            return self.x - CAR_RADIUS - 150
        elif (self.y <= 350):
            return self.x - CAR_RADIUS - 50
        else:
            return self.x - CAR_RADIUS
    
    def get_distance_to_finish(self):
        return math.sqrt(((self.x - WIN_CIRCLE_POSITION[0])**2) + ((self.y - WIN_CIRCLE_POSITION[1])**2))

    def is_too_slow(self, score):
        if self.x < score:
            return True
        
        if self.y > (500 - score):
            return True
        
        return False

def test_genomes(gens, config):
    global WIN
    win = WIN

    rect_position = (150, 200, 20, 20)
    
    velocity = 5

    networks = []
    cars = []
    genomes = []

    for genome_id, genome in gens:
        genome.fitness = 0

        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)

        cars.append(Car(25, 475))

        genomes.append(genome)

    score = 0

    keep_running = True
    while keep_running and len(cars) > 0:
        score += 1
        pygame.time.delay(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_running = False
                pygame.quit()
                quit()
                break
        
        for index, car in enumerate(cars):
            distance_top = car.get_distance_top()
            distance_right = car.get_distance_right()
            distance_bottom = car.get_distance_bottom()
            distance_left = car.get_distance_left()
            distance_to_finish = car.get_distance_to_finish()

            if distance_top < 0 or distance_right < 0 or distance_bottom < 0 or distance_left < 0 or car.is_too_slow(score):
                cars.pop(index)
                genomes[index].fitness = 1000 - distance_to_finish
                genomes.pop(index)
                networks.pop(index)
                continue

            output = networks[index].activate((distance_top, distance_right, distance_bottom, distance_left, distance_to_finish))
            
            # UP
            if output[0] > .5:
                car.y -= velocity
            
            # RIGHT
            if output[1] > .5:
                car.x += velocity

            # DOWN
            if output[2] > .5:
                car.y += velocity

            # LEFT
            if output[3] > .5:
                car.x -= velocity

            if car.y - CAR_RADIUS < rect_position[1] + rect_position[3] and car.y + CAR_RADIUS > rect_position[1]:
                if car.x + CAR_RADIUS > rect_position[0] and car.x - CAR_RADIUS < rect_position[0] + rect_position[2]:
                    color = (255, 0, 0)
            
            if car.x == WIN_CIRCLE_POSITION[0] and car.y == WIN_CIRCLE_POSITION[1]:
                print('SOLUTION FOUND')
                pickle.dump(networks[0], open("best.pickle", "wb"))
                cars.pop(index)
                genomes[index].fitness = 1000 - distance_to_finish
                genomes.pop(index)
                networks.pop(index)

        win.fill((255, 255, 255))
        
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 100, 400))
        pygame.draw.rect(win, (0, 0, 0), (100, 0, 100, 300))
        pygame.draw.rect(win, (0, 0, 0), (200, 0, 100, 200))
        pygame.draw.rect(win, (0, 0, 0), (300, 0, 100, 100))

        pygame.draw.rect(win, (0, 0, 0), (50, 450, 100, 50))
        pygame.draw.rect(win, (0, 0, 0), (150, 350, 100, 150))
        pygame.draw.rect(win, (0, 0, 0), (250, 250, 100, 250))
        pygame.draw.rect(win, (0, 0, 0), (350, 150, 100, 350))
        pygame.draw.rect(win, (0, 0, 0), (450, 50, 100, 450))

        pygame.draw.circle(win, (0, 255, 0), WIN_CIRCLE_POSITION, CAR_RADIUS)

        for index, car in enumerate(cars):
            pygame.draw.circle(win, car.color, (car.x, car.y), CAR_RADIUS)

        pygame.display.update()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    pop = neat.Population(config)
    
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(test_genomes, 10000)

    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)