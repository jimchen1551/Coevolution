import matplotlib.pyplot as plt
import numpy as np
import time
from environment import Environment

class Simulation:
    def __init__(self, width=50, height=50, num_food=300, num_prey=200, num_predators=10, generations=200):
        self.env = Environment(width, height, num_food, num_prey, num_predators)
        self.generations = generations
        self.history = {
            "prey_speed": [], "predator_speed": [],
            "prey_vision": [], "predator_vision": [],
            "num_prey": [], "num_predators": [], 
            "age_preys": [], "age_predators": [], 
            "energy_preys": [], "energy_predators": [], 
        }
    
    def run(self):
        for gen in range(self.generations):
            self.env.step(gen)
            self.record_statistics()
            print(f"Generation {gen + 1}: Preys = {len(self.env.preys)}, Predators = {len(self.env.predators)}")
            time.sleep(0.1)  # Small delay for visualization purposes
    
    def record_statistics(self):
        self.history["prey_speed"].append([prey.speed for prey in self.env.preys])
        self.history["predator_speed"].append([predator.speed for predator in self.env.predators])
        self.history["prey_vision"].append([prey.vision for prey in self.env.preys])
        self.history["predator_vision"].append([predator.vision for predator in self.env.predators])
        self.history["num_prey"].append(len(self.env.preys))
        self.history["num_predators"].append(len(self.env.predators))
        self.history["age_preys"].append([prey.age for prey in self.env.preys])
        self.history["age_predators"].append([predator.age for predator in self.env.predators])
        self.history["energy_preys"].append([prey.energy for prey in self.env.preys])
        self.history["energy_predators"].append([predator.energy for predator in self.env.predators])
    
    def plot_statistics(self):
        fig, axes = plt.subplots(5, 2, figsize=(24, 30))
        plt.style.use("ggplot")
        
        tick_spacing = max(1, self.generations // 10)  # Show fewer ticks
        x_labels = list(range(0, self.generations, tick_spacing))
        generations = list(range(self.generations))
        
        # Boxplots for speed and vision
        axes[0, 0].boxplot(self.history["prey_speed"], positions=range(len(self.history["prey_speed"])), sym='')
        axes[0, 0].set_title("Prey Speed per Generation")
        axes[0, 0].set_xticks(x_labels)
        axes[0, 0].set_xlabel("Generation")
        axes[0, 0].set_ylabel("Speed")
        
        axes[0, 1].boxplot(self.history["predator_speed"], positions=range(len(self.history["predator_speed"])), sym='')
        axes[0, 1].set_title("Predator Speed per Generation")
        axes[0, 1].set_xticks(x_labels)
        axes[0, 1].set_xlabel("Generation")
        axes[0, 1].set_ylabel("Speed")
        
        axes[1, 0].boxplot(self.history["prey_vision"], positions=range(len(self.history["prey_vision"])), sym='')
        axes[1, 0].set_title("Prey Vision per Generation")
        axes[1, 0].set_xticks(x_labels)
        axes[1, 0].set_xlabel("Generation")
        axes[1, 0].set_ylabel("Vision")
        
        axes[1, 1].boxplot(self.history["predator_vision"], positions=range(len(self.history["predator_vision"])), sym='')
        axes[1, 1].set_title("Predator Vision per Generation")
        axes[1, 1].set_xticks(x_labels)
        axes[1, 1].set_xlabel("Generation")
        axes[1, 1].set_ylabel("Vision")

        # Boxplots for energy
        axes[2, 0].boxplot(self.history["energy_preys"], positions=range(len(self.history["energy_preys"])), sym='')
        axes[2, 0].set_title("Prey Energy per Generation")
        axes[2, 0].set_xticks(x_labels)
        axes[2, 0].set_xlabel("Generation")
        axes[2, 0].set_ylabel("Energy")

        axes[2, 1].boxplot(self.history["energy_predators"], positions=range(len(self.history["energy_predators"])), sym='')
        axes[2, 1].set_title("Predator Energy per Generation")
        axes[2, 1].set_xticks(x_labels)
        axes[2, 1].set_xlabel("Generation")
        axes[2, 1].set_ylabel("Energy")

        # Boxplots for age
        axes[3, 0].boxplot(self.history["age_preys"], positions=range(len(self.history["age_preys"])), sym='')
        axes[3, 0].set_title("Prey Age per Generation")
        axes[3, 0].set_xticks(x_labels)
        axes[3, 0].set_xlabel("Generation")
        axes[3, 0].set_ylabel("Age")

        axes[3, 1].boxplot(self.history["age_predators"], positions=range(len(self.history["age_predators"])), sym='')
        axes[3, 1].set_title("Predator Age per Generation")
        axes[3, 1].set_xticks(x_labels)
        axes[3, 1].set_xlabel("Generation")
        axes[3, 1].set_ylabel("Age")
        
        # Scatter plot for population dynamics
        prey_speeds = [np.mean(s) if s else 0 for s in self.history["prey_speed"]]
        predator_speeds = [np.mean(s) if s else 0 for s in self.history["predator_speed"]]
        prey_colors = np.array(prey_speeds) / max(prey_speeds) if max(prey_speeds) > 0 else [0] * len(prey_speeds)
        predator_colors = np.array(predator_speeds) / max(predator_speeds) if max(predator_speeds) > 0 else [0] * len(predator_speeds)
        
        scatter = axes[4, 0].scatter(generations, self.history["num_prey"], c=prey_colors, cmap='Blues', edgecolor='k')
        axes[4, 0].set_title("Prey Population Over Generations")
        axes[4, 0].set_xlabel("Generation")
        axes[4, 0].set_ylabel("Number of Prey")
        plt.colorbar(scatter, ax=axes[4, 0], label="Relative Speed")
        
        scatter = axes[4, 1].scatter(generations, self.history["num_predators"], c=predator_colors, cmap='Reds', edgecolor='k')
        axes[4, 1].set_title("Predator Population Over Generations")
        axes[4, 1].set_xlabel("Generation")
        axes[4, 1].set_ylabel("Number of Predators")
        plt.colorbar(scatter, ax=axes[4, 1], label="Relative Speed")
        
        plt.tight_layout()
        plt.savefig('results/simulation_results.png')

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    sim.plot_statistics()
