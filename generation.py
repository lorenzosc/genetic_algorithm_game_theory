import numpy as np
from strategy import Strategy, match


class Generation:
    individuals: list[Strategy]
    archetypes: np.ndarray[int]
    population = int

    def __init__ (self, distributions: np.ndarray[np.ndarray]) -> None:
        self.individuals = [
            Strategy(idx, np.sum(distributions[idx]), distributions[idx, :].copy())
            for idx in range(distributions.shape[0])
        ]
        self.avaliate_archetypes()
        self.population = self.individuals[0].distribution.shape[0]

    def avaliate_population (self) -> None:
        """
        Function to calculate fitness score and order population
        """
        for strategy in self.individuals:
            fitness = []

            for opponent in self.individuals:
                if strategy.idx == opponent.idx:
                    continue

                str_points = strategy.distribution[opponent.idx]
                opp_points = opponent.distribution[strategy.idx]
                fitness.append(str_points / (str_points + opp_points))

            strategy.fitness = np.average(fitness)

        self.individuals.sort(key=lambda x: x.fitness, reverse=True)

    def preserve_population (self, survival = 0.2) -> list[Strategy]:
        """Preserve a percentage of each archetype population for the next generation

        :param survival: percentagem of each archetype that will survive, defaults to 0.2
        :return: List of strategies that were preserved
        """
        histogram = np.ceil(self.archetypes * survival)

        new_population = []

        for strategy in self.individuals:
            if histogram[strategy.idx]:
                new_population.append(strategy)
                histogram[strategy.idx] -= 1
        
        return new_population

    def avaliate_archetypes (self) -> None:
        """Creates histogram of how many of each archetype exists in population
        """
        
        histogram = np.zeros(self.individuals[0].distribution.shape[0])
        for strategy in self.individuals:
            histogram[strategy.idx] = histogram[strategy.idx] + 1
        
        self.archetypes = histogram.copy()

    def generate_new_population (self) -> None:
        self.avaliate_population()

        population = self.preserve_population()

        while len(population) < self.population:
            strategy1 = np.random.choice(self.population)
            strategy2 = np.random.choice(self.population)
            population.append(match(strategy1, strategy2))

        self.individuals = population
        self.avaliate_archetypes()

