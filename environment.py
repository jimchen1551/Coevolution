import math
import random
import numpy as np
from entity import Prey, Predator

class Environment:
    def __init__(self, width, height, num_food, num_prey, num_predators):
        self.width = width
        self.height = height
        self.num_food = num_food
        self.food_sources = [self.random_position() for _ in range(num_food)]
        self.prey_energy = 50
        self.predator_energy = 50
        self.prey_lifespan = 3  # 6
        self.predator_lifespan = 2
        self.preys = [Prey(self.random_position(), np.random.uniform(3, 5), np.random.uniform(3, 5), self.prey_energy, self.prey_lifespan) for _ in range(num_prey)]  # (1, 3), (5, 8)
        self.predators = [Predator(self.random_position(), np.random.uniform(3, 5), np.random.uniform(3, 5), self.predator_energy, self.predator_lifespan) for _ in range(num_predators)]  # (3, 5), (8, 10)
    
    def random_position(self):
        return np.array([random.uniform(0, self.width), random.uniform(0, self.height)])
    
    def update_food(self, idx):
        self.food_sources = [self.random_position() for _ in range(int(self.num_food - 0 * math.cos(math.pi * idx / 100)))]
    
    def update_entities(self):
        # Update predator movement and energy
        new_predators = []
        for predator in self.predators:
            if not predator.alive:
                continue
            for _ in range(random.randint(1, 3)):
                prey_target = predator.find_prey(self.preys)
                if prey_target:
                    predator.move_towards(prey_target.position)
                    predator.hunt(prey_target)
                else:
                    predator.energy -= 10  # Energy loss if no prey found
                    break
            predator.update()
            if predator.alive:
                for _ in range(random.randint(0, 2)):
                    offspring = predator.reproduce(self.predator_energy, self.predator_lifespan)
                    if offspring:
                        new_predators.append(offspring)
        self.predators.extend(new_predators)

        # Update prey movement and energy
        new_preys = []
        for prey in self.preys:
            if not prey.alive:
                continue
            food = prey.find_food(self.food_sources)
            if food is not None:
                prey.move_towards(food)
                if np.linalg.norm(prey.position - food) == 0:
                    prey.energy += 10  # Gain energy from food
                    self.food_sources = [f for f in self.food_sources if not np.array_equal(f, food)]
            else:
                prey.energy -= 10  # Energy loss if no food found
            prey.update()
            if prey.alive:
                for _ in range(random.randint(0, 2)):
                    offspring = prey.reproduce(self.prey_energy, self.prey_lifespan)
                    if offspring:
                        new_preys.append(offspring)
        self.preys.extend(new_preys)
        
        # Remove dead entities
        self.preys = [prey for prey in self.preys if prey.alive]
        self.predators = [predator for predator in self.predators if predator.alive]
    
    def step(self, idx):
        self.update_food(idx)
        self.update_entities()