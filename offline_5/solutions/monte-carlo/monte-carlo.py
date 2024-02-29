import numpy as np
from tqdm import tqdm

np.random.seed(13)

class MonteCarloSimulation:
  def _probability_of_i_offspring(self, i: int) -> float:
    if i < 1:
      raise ValueError("i must be greater than 0.")
    
    return self.p * (self.q ** (i - 1))
  
  def __init__(self, p, q, max_offsprings, max_population) -> None:
    """
    Initializes the Monte Carlo simulation.

    Parameters:
    ----------
    p: float
      Probability of having an offspring
    q: float
      Probability of having no offspring
    max_offsprings: int
      Maximum number of offsprings from one parent
    max_population: int
      Maximum population size of a generation
    """
    self.p = p
    self.q = q
    self.max_offsprings = max_offsprings
    self.max_population = max_population

    self.ps = [self._probability_of_i_offspring(i) for i in range(1, max_offsprings + 1)]
    self.ps.insert(0, 1 - sum(self.ps))

    print(self.ps)

  def generate_new_generation(self, n: int) -> int:
    """
    Generates a new generation of offsprings.

    Parameters:
    ----------
    n: int
      The number of offsprings in the current generation
    
    Returns:
    -------
    int
      The number of offsprings in the new generation
    """
    n_new = 0

    for _ in range(n):
      n_new += np.random.choice(range(self.max_offsprings + 1), p=self.ps)

    return n_new

  def simulate(self, generations: int, trials: int) -> float:
    self.generations = generations
    
    counts = np.zeros((generations, self.max_population + 1), dtype=int)

    for _ in tqdm(range(trials)):
      gen = 0
      n = 1

      while gen < generations:
        n = self.generate_new_generation(n)

        if n <= self.max_population:
          counts[gen, n] += 1
        
        gen += 1

    self.gen_probs = counts / trials

  def report(self, filename: str = None) -> None:
    if (self.gen_probs is None) or (self.generations is None):
      raise ValueError("You must run the simulation first.")
    
    if filename:
      with open(filename, "w") as f:
        for i in range(self.generations):
          f.write(f"Generation-{i + 1}:\n")
          for j in range(5):
            f.write(f"P[{j}] = {self.gen_probs[i, j]}\n")
          
          f.write("\n")
    else:
      for i in range(self.generations):
        print(f"Generation-{i + 1}:")
        for j in range(5):
          print(f"P[{j}] = {self.gen_probs[i, j]}")
        
        print()


if __name__ == "__main__":
  p = 0.2126
  q = 0.5893

  sim = MonteCarloSimulation(p, q, 3, 4)
  sim.simulate(10, 10000)
  sim.report("results.txt")