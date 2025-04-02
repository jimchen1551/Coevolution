import numpy as np

class Entity:
    def __init__(self, position, speed, vision, energy, lifespan):
        self.position = np.array(position)
        self.speed = speed
        self.speed_ = speed
        self.vision = vision
        self.vision_ = vision
        self.energy = energy
        self.lifespan = lifespan
        self.age = 0
        self.alive = True
    
    def move_towards(self, target):
        direction = target - self.position
        distance = np.linalg.norm(direction)
        if distance > 0:
            step = (direction / distance) * min(self.speed, distance)
            self.position += step
    
    def update(self):
        self.age += 1
        if self.age/self.lifespan > 0.33:
            self.speed *= 0.9  # Speed decay
            self.vision *= 0.9  # Vision decay
        if self.age >= self.lifespan or self.energy <= 0:
            self.alive = False

class Prey(Entity):
    def __init__(self, position, speed, vision, energy, lifespan):
        super().__init__(position, speed, vision, energy, lifespan)
    
    def find_food(self, food_sources):
        visible_food = [food for food in food_sources if np.linalg.norm(food - self.position) <= self.vision]
        return min(visible_food, key=lambda food: np.linalg.norm(food - self.position), default=None)

    def reproduce(self, energy_, lifespan_):
        if self.energy > 40:  # Energy threshold for reproduction
            self.energy -= 20  # Energy cost for reproduction
            new_speed = np.random.normal(self.speed_, 2)
            new_vision = np.random.normal(self.vision_, 2)
            new_energy = energy_
            new_lifespan = max(np.random.normal(lifespan_, 1), 1) 
            return type(self)(self.position.copy(), new_speed, new_vision, new_energy, new_lifespan)
        return None

class Predator(Entity):
    def __init__(self, position, speed, vision, energy, lifespan):
        super().__init__(position, speed, vision, energy, lifespan)
    
    def find_prey(self, preys):
        visible_prey = [prey for prey in preys if np.linalg.norm(prey.position - self.position) <= self.vision and prey.alive]
        return min(visible_prey, key=lambda prey: np.linalg.norm(prey.position - self.position), default=None)
    
    def hunt(self, prey):
        if np.all(self.position == prey.position) and prey.alive: #  and (self.speed >= prey.speed)
            prey.alive = False
            self.energy += 10# prey.energy * 0.1  # Gain energy from hunting
    
    def reproduce(self, energy_, lifespan_):
        if self.energy > 30:  # Energy threshold for reproduction
            self.energy -= 20  # Energy cost for reproduction
            new_speed = np.random.normal(self.speed_, 2) # self.speed * 0.1
            new_vision = np.random.normal(self.vision_, 2) # self.vision * 0.1
            new_energy = energy_
            new_lifespan = max(np.random.normal(lifespan_, 1), 1) 
            return type(self)(self.position.copy(), new_speed, new_vision, new_energy, new_lifespan)
        return None