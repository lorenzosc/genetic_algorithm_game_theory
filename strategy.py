from __future__ import annotations
import numpy as np

class Strategy:
    idx: int
    points: int
    distribution: np.ndarray
    fitness: float

    def __init__ (
        self, idx: int, points: int, distribution: np.ndarray
    ) -> None:
        self.idx = idx
        self.points = points
        self.distribution = distribution.copy()

    def mutation (self, odds: float = 0.05) -> None:
        """
            Generate mutation in a strategy by changing points distribution

            :param odds: odd for each chromossome to mutate, defaults to 0.05
        """
        villains = set(range(len(self.distribution)))
        villains.remove(self.idx)
        mutable = villains.copy()

        while len(villains) != 0:
            villain = np.random.choice(villains)
            villains.remove(villain)

            chance = np.random.random()
            if chance <= odds:
                villain2 = np.random.choice(mutable)
                self.change_distribution(villain, villain2)

                mutable.remove(villain)
                mutable.remove(villain2)
                villains.discard(villain2)

    def change_distribution (self, idx1: int, idx2: int) -> None:
        """Redistributes points between two chromossomes

        :param name1: first chromossome
        :param name2: second chromossome
        """
        points1 = self.distribution[idx1]
        points2 = self.distribution[idx2]
        total_points = points1 + points2

        self.distribution[idx1] = np.random.randint(0, total_points + 1)
        self.distribution[idx2] = total_points - self.distribution[idx1]

    def generate_child (
        self, mother: Strategy, odds: float = 0.10, mutation_odds: float = 0.05
    ) -> Strategy:
        if not isinstance(mother, Strategy):
            raise TypeError

        child = Strategy(self.idx, self.points, self.distribution)

        villains = set(range(len(child.distribution)))
        villains.remove(self.idx)
        mutable = villains.copy()

        while len(villains) > 1:
            villain = np.random.choice(villains)
            villains.remove(villain)

            chance = np.random.random()
            if chance <= odds:
                if villain == mother.idx:
                    continue

                mutable.remove(villain)
                if mother.idx in mutable and len(mutable) > 1:
                    mutable.remove(mother.idx)
                    villain2 = np.random.choice(mutable)
                    mutable.add(mother.idx)

                elif mother.idx in mutable:
                    break

                else:
                    villain2 = np.random.choice(mutable)

                sf_points = (self.distribution[villain], self.distribution[villain2])
                sm_points = (mother.distribution[villain], mother.distribution[villain2])

                sf_sum = sum(sf_points)
                sm_sum = sum(sm_points)

                pctf = sf_points[0] / sf_sum
                pctm = sm_points[0] / sm_sum

                c_pct = np.random.random() * (pctf - pctm) + pctm

                v1_points = int(sf_sum * c_pct)
                v2_points = sf_sum - v1_points

                child.distribution[villain] = v1_points
                child.distribution[villain2] = v2_points

                mutable.remove(villain2)
                villains.discard(villain2)

            elif chance <= odds + mutation_odds:
                mutable.remove(villain)
                villain2 = np.random.choice(mutable)
                child.change_distribution(villain, villain2)

                mutable.remove(villain2)
                villains.discard(villain2)

        return child

def match (strategy: Strategy, strategy2: Strategy) -> None:
    if not isinstance(strategy2, Strategy):
        raise TypeError

    s1_points = strategy.distribution[strategy2.idx]
    s2_points = strategy2.distribution[strategy.idx]

    # gives 50% chance in case none have points in that match
    if s1_points == 0 and s2_points == 0:
        s1_points = 1
        s2_points = 1

    total = s2_points + s1_points
    winner = np.random.randint(0, total)

    if winner < s1_points:
        strategy.generate_child(strategy2)

    else:
        strategy2.generate_child(strategy)
