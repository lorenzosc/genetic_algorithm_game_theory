import random

import numpy as np

from strategy import Strategy, match


class Generation:
    individuals: list[Strategy]
    archetypes: np.ndarray[int]

    pop_size: int
    n_arch: int

    podium_size: int
    arch_points: list[int]
    arch_podium: list[float]
    top_podium: list[float]
    playrate: list[list[float]]
    winrate: list[list[float]]

    def __init__ (self, pop_size: int, distributions: np.ndarray[np.ndarray], podium_size: int = 10) -> None:
        _, self.n_arch = distributions.shape
        self.pop_size = pop_size
        self.arch_podium = [ 0 for _ in range(self.n_arch) ]
        self.top_podium = [ 0 for _ in range(self.n_arch) ]
        self.playrate = [ [] for _ in range(self.n_arch) ]
        self.winrate = [ [] for _ in range(self.n_arch) ]
        self.arch_points = [ np.sum(distributions[idx]) for idx in range(self.n_arch) ]
        self.podium_size = podium_size

        self.individuals = [
            Strategy(idx, self.arch_points[idx], distributions[idx])
            for idx in range(self.n_arch)
        ]
        self.avaliate_population()
        base_weights = [ ind.fitness for ind in self.individuals ]

        self.individuals = random.choices(self.individuals, weights=base_weights, k=self.pop_size)

        self.avaliate_archetypes()

    def avaliate_archetypes (self) -> None:
        """Creates histogram of how many of each archetype exists in population
        """
        self.archetypes = np.zeros(self.n_arch)
        for strategy in self.individuals:
            self.archetypes[strategy.idx] += 1

    def avaliate_population (self) -> None:
        """
        Function to calculate fitness score and order population
        """
        for strategy in self.individuals:
            fitness = []

            for opponent in self.individuals:
                str_points = strategy.distribution[opponent.idx]
                opp_points = opponent.distribution[strategy.idx]

                if str_points + opp_points == 0:
                    fitness.append(0.5)

                else:
                    fitness.append(str_points / (str_points + opp_points))

            strategy.fitness = np.average(fitness)

            self.winrate[strategy.idx].append(strategy.fitness)

        self.individuals.sort(key=lambda x: x.fitness, reverse=True)

    def preserve_population (self, survival: float = 0.2) -> list[Strategy]:
        """Preserve a percentage of each archetype population for the next generation

        :param survival: percentagem of each archetype that will survive, defaults to 0.2
        :return: List of strategies that were preserved
        """
        histogram = np.ceil(self.archetypes * survival)

        new_population = []

        for strategy in self.individuals:
            if histogram[strategy.idx] > 0:
                new_population.append(strategy)
                histogram[strategy.idx] -= 1

        return new_population

    def generate_new_population (self) -> None:
        self.avaliate_population()

        print("Archetypes playrate")
        for arch_idx in range(self.n_arch):
            self.playrate[arch_idx].append(self.archetypes[arch_idx] / self.archetypes.sum() * 100)

            print(
                f"arch: {arch_idx} - "
                f"{self.archetypes[arch_idx] / self.archetypes.sum() * 100 : .2f}%",
                end=" "
            )

        print("\n ------------------------------- ")

        print(f"Top {self.podium_size} - Decks")
        self.top_podium[self.individuals[0].idx] += 1
        for ind in self.individuals[ : self.podium_size ]:
            print(f"Archetype: {ind.idx} - Fitness: {ind.fitness:.3f} - Points: {ind.points}")
            self.arch_podium[ind.idx] += 1 / self.podium_size

        print(" ------------------------------- ")
        population = self.preserve_population()

        weights = [ x.fitness for x in self.individuals ]
        while len(population) < self.pop_size:
            strategy1, strategy2 = random.choices(self.individuals, weights=weights, k=2)
            population.append(match(strategy1, strategy2))

        self.individuals = population
        self.avaliate_archetypes()

    def evolve (self, n_gen: int) -> None:
        for _ in range(n_gen):
            self.generate_new_population()

        print("Presence in the podium for each archetype")
        for arch_idx in range(self.n_arch):
            wr = np.array(self.winrate[arch_idx])
            pr = np.array(self.playrate[arch_idx])

            print(
                f"Arch: {arch_idx} - Podium%: {self.arch_podium[arch_idx] / n_gen:.2f}"
                f" Top1%: {self.top_podium[arch_idx] / n_gen:.2f}"
                f" Avg PlayRate: {pr.mean():.2f}%"
                f" Pr Std: {pr.std():.2f}"
                f" Avg WinRate: {wr.mean():.3f}"
                f" Wr Std: {wr.std():.3f}"
                f" Base Points: {self.arch_points[arch_idx]}"
            )

        print()
