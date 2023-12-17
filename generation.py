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

    mnmx_wr: list[tuple[float, float]]
    mnmx_pr: list[tuple[float, float]]

    def __init__ (self, pop_size: int, distributions: np.ndarray[np.ndarray], podium_size: int = 10) -> None:
        _, self.n_arch = distributions.shape
        self.pop_size = pop_size
        self.arch_podium = [ 0 for _ in range(self.n_arch) ]
        self.top_podium = [ 0 for _ in range(self.n_arch) ]
        self.playrate = [ [] for _ in range(self.n_arch) ]
        self.winrate = [ [] for _ in range(self.n_arch) ]

        self.mnmx_wr = [ (np.inf, 0) for _ in range(self.n_arch) ]
        self.mnmx_pr = [ (np.inf, 0) for _ in range(self.n_arch) ]

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
        wrs = [ [] for _ in range(self.n_arch) ]

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

            wrs[strategy.idx].append(strategy.fitness)

        for arch_idx in range(self.n_arch):
            self.winrate[arch_idx].append(np.mean(wrs[arch_idx]))
            self.mnmx_wr[arch_idx] = (
                min(self.mnmx_wr[arch_idx][0], min(wrs[arch_idx])),
                max(self.mnmx_wr[arch_idx][1], max(wrs[arch_idx]))
            )

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
        self.avaliate_archetypes()
        self.avaliate_population()

        for arch_idx in range(self.n_arch):
            pr = self.archetypes[arch_idx] / self.pop_size * 100
            self.playrate[arch_idx].append(pr)
            self.mnmx_pr[arch_idx] = (
                min(self.mnmx_pr[arch_idx][0], pr),
                max(self.mnmx_pr[arch_idx][1], pr)
            )

        self.top_podium[self.individuals[0].idx] += 1
        for ind in self.individuals[ : self.podium_size ]:
            self.arch_podium[ind.idx] += 1 / self.podium_size

        population = self.preserve_population()

        weights = [ x.fitness for x in self.individuals ]
        while len(population) < self.pop_size:
            strategy1, strategy2 = random.choices(self.individuals, weights=weights, k=2)
            population.append(match(strategy1, strategy2))

        self.individuals = population

    def evolve (self, n_gen: int) -> None:
        for idx in range(n_gen):
            if idx % 100 == 0:
                print(f"gen idx: {idx}")

            self.generate_new_population()

        print("Presence in the podium for each archetype")
        for arch_idx in range(self.n_arch):
            pr = np.array(self.playrate[arch_idx])
            wr = (np.array(self.winrate[arch_idx])[ 1 : ] * pr) / pr.mean()

            print(f"Arch: {arch_idx} Base Points: {self.arch_points[arch_idx]}")

            print("\tPodium Statistics")
            print(
                f"\t\tPodium%: {self.arch_podium[arch_idx] / n_gen:.2f}",
                f"\t\tTop1%: {self.top_podium[arch_idx] / n_gen:.2f}", sep="\n"
            )

            print("\tPlayRate Statistics")
            print(
                f"\t\tAvg PlayRate: {pr.mean():.2f}%",
                f"\t\tPr Std: {pr.std():.2f}",
                # f"\t\tMoving Avg: {}",
                f"\t\tMin Pr: {self.mnmx_pr[arch_idx][0]:.2f}",
                f"\t\tMax Pr: {self.mnmx_pr[arch_idx][1]:.2f}", sep="\n"
            )
            print("\tWinRate Statistics")
            print(
                f"\t\tAvg WinRate: {wr.mean():.3f}",
                f"\t\tWr Std: {wr.std():.3f}",
                f"\t\tMin Wr: {self.mnmx_wr[arch_idx][0]:.2f}",
                f"\t\tMax Wr: {self.mnmx_wr[arch_idx][1]:.2f}", sep="\n"
            )

        print()
