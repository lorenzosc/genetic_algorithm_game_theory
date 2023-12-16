# genetic_algorithm_game_theory
Implementation of genetic algorithm for analysis over different player choices across several generations for game theory optimal strategies

Each strategy isn't equally powerful. Each strategy has a points attribute which says how many points that strategy has in total to distribute against it's opponents. When two strategies clash, the chance of each being the winner is the total of both investments in that match divided by their own investment. The winner will transfer most of it's chromossomes for the child that will be bred from that crossover.

It's important to notice that each strategy belongs to an archetype identified by a unique name, which is how their opponent determines how many points were invested in that match. Since the distribution changes, it's very important to notice that two strategies from the same archetype won't be equal, but they will have the same total of points to distribute against it's opponents
