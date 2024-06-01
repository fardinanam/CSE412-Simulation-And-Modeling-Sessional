import sys 
import numpy as np
from tqdm import tqdm

if len(sys.argv) != 2:
  print("Usage: python secretary-problem.py n")
  sys.exit(1)

n = int(sys.argv[1])

if n < 1:
  print("n must be greater than 0.")
  sys.exit(1)

def success_rate_m(n: int, m: int, s: int, trials: int) -> float:
  """
    Calculates the success rate (in percentage) of the secretary problem for a given number of candidates, sample size, and success threshold.

    Parameters:
    ----------
    n: int
      The number of candidates
    m: int
      sample size (number of candidates to interview before making a decision)
    s: int
      Success threshold

    Returns:
    -------
    float
      The success rate (in percentage)
  """
  successes = 0
  for _ in range(trials):
    ranks = np.random.permutation(n)
    best = 0 if m == 0 else ranks[:m].min()

    chosen = ranks[-1]
    for i in range(m, n):
      if ranks[i] < best:
        chosen = ranks[i]
        break

    if chosen <= s:
      successes += 1

  return (successes / trials) * 100

def plot_success_rates(success_rates: list, n: int, s: int):
  """
    Plots the success rates for different sample sizes.

    Parameters:
    ----------
    success_rates: list
      A list of success rates for different sample sizes
    n: int
      The number of candidates
    s: int
      Success threshold
  """
  import matplotlib.pyplot as plt

  plt.plot(range(n), success_rates)
  plt.ylim(0, 100)
  plt.xlabel("Sample Size")
  plt.ylabel("Success Rate (%)")
  plt.title(f"Success Rates for n = {n} and s = {s}")
  plt.savefig(f"plots/n_{n}_s_{s}.png")
  plt.close()

if __name__ == "__main__":
  n = int(sys.argv[1])

  for s in [1, 3, 5, 10]:
    success_rates = []
    for m in tqdm(range(n)):
      success_rates.append(success_rate_m(n, m, s, 10000))

    plot_success_rates(success_rates, n, s)

  