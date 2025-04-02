import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from simulation import Simulation

class Visualization:
    def __init__(self, simulation):
        self.sim = simulation
    
    def animate(self, save_path="results/animation.mp4"):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, self.sim.env.width)
        ax.set_ylim(0, self.sim.env.height)
        self.zero_flag = False
        
        def update(frame):
            if frame == 0:
                if self.zero_flag:
                    return
                self.zero_flag = True
                
            ax.clear()
            ax.set_xlim(0, self.sim.env.width)
            ax.set_ylim(0, self.sim.env.height)
            
            self.sim.env.step(frame)  # Advance the simulation by one step
            self.sim.record_statistics()
            print(f"Generation {frame + 1}: Preys = {len(self.sim.env.preys)}, Predators = {len(self.sim.env.predators)}")
            
            prey_positions = np.array([prey.position for prey in self.sim.env.preys if prey.alive])
            predator_positions = np.array([pred.position for pred in self.sim.env.predators if pred.alive])
            
            if len(prey_positions) > 0:
                ax.scatter(prey_positions[:, 0], prey_positions[:, 1], c='blue', label='Prey', alpha=0.5)
            if len(predator_positions) > 0:
                ax.scatter(predator_positions[:, 0], predator_positions[:, 1], c='red', label='Predator', alpha=0.5)
            
            ax.set_title(f"Generation {frame + 1}")
            ax.legend(loc='upper right')
        
        ani = animation.FuncAnimation(fig, update, frames=self.sim.generations, repeat=False)
        ani.save(save_path, writer='ffmpeg', fps=5)
        plt.close()
        self.sim.plot_statistics()
        print(f"Animation saved as {save_path}")
    
    def plot_population(self):
        generations = range(self.sim.generations)
        plt.figure(figsize=(10, 5))
        
        plt.plot(generations, self.sim.history["num_prey"], label="Prey", color='blue')
        plt.plot(generations, self.sim.history["num_predators"], label="Predator", color='red')
        plt.xlabel("Generation")
        plt.ylabel("Population Count")
        plt.title("Population Dynamics Over Generations")
        plt.legend()
        plt.savefig('results/population_dynamics.png')
    
    def plot_phase_space(self):
        prey_counts = self.sim.history["num_prey"]
        predator_counts = self.sim.history["num_predators"]
        
        plt.figure(figsize=(8, 6))
        plt.plot(prey_counts, predator_counts, marker='o', linestyle='-', color='purple')
        plt.xlabel("Prey Population")
        plt.ylabel("Predator Population")
        plt.title("Phase Space Plot: Prey vs Predator Population")
        plt.grid(True)
        plt.savefig('results/phase_space_plot.png')

if __name__ == "__main__":
    sim = Simulation()
    viz = Visualization(sim)
    viz.animate()
    viz.plot_population()
    viz.plot_phase_space()
