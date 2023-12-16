import numpy as np
from strategy import Strategy, match


class Generation:
    population: list[Strategy]

    def __init__ (self, distributions: np.ndarray[np.ndarray]) -> None:
        self.population = [
            Strategy(idx, np.sum(distributions[idx]), distributions[idx])
            for idx in range(distributions.shape[0])
        ]

    def avaliate_population (self) -> None:
        for strategy in self.population:
            fitness = []

            for opponent in self.population:
                if strategy.idx == opponent.idx:
                    continue

                str_points = strategy.distribution[opponent.idx]
                opp_points = opponent.distribution[strategy.idx]
                fitness.append(str_points / (str_points + opp_points))

            strategy.fitness = np.average(fitness)

        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def preserve_population () -> None:
        pass

    def generate_new_population (self) -> None:
        pass
