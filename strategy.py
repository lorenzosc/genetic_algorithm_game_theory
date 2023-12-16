import random

class Strategy:
    name: str
    points: int
    distribution: dict[str, int]

    def __init__ (
            self, name: str, points: int, distribution: dict[str, int]
    ) -> None:
        self.name = name
        self.points = points
        self.distribution = distribution

    def mutation (
            self, odds: float = 0.05
    ) -> None:
        """Generate mutation in a strategy by changing points distribution

        :param odds: odd for each chromossome to mutate, defaults to 0.05
        """
        villains = set(self.distribution.keys())

        for villain in self.distribution:

            chance = random.random()
            if chance <= odds:

                villains.remove(villain)
                villain2 = random.choice(villains)
                villains.remove(villain2)
                self.change_distribution(villain, villain2)

    def change_distribution (self, name1: str, name2: str) -> None:
        """Redistributes points between two chromossomes

        :param name1: first chromossome
        :param name2: second chromossome
        """
        points1 = self.distribution[name1]
        points2 = self.distribution[name2]
        total_points = points1 + points2
        self.distribution[name1] = random.randint(0, total_points)
        self.distribution[name2] = total_points - self.distribution[name1]

def match (
        strategy1: Strategy, strategy2: Strategy, 
) -> None:
    
    s1_points = strategy1.distribution[strategy2.name]
    s2_points = strategy2.distribution[strategy1.name]

    #gives 50% chance in case none have points in that match
    if s1_points == 0 and s2_points == 0:
        s1_points = 1
        s2_points = 1

    total = s2_points+s1_points
    winner = random.randint(0, total-1)
    if winner < s1_points:
        generate_child(strategy1, strategy2)
    else:
        generate_child(strategy2, strategy1)

def generate_child (
        father: Strategy, mother: Strategy
) -> Strategy:
    pass