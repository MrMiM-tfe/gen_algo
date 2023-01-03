
import random, math
import matplotlib.pyplot as plt
import numpy as np

items = []

for i in range(10):
    items.append({
        "name": "p",
        "value": random.randint(1,100),
        "weight": random.randint(1,200)
    })

population_size = 200
DNA_length = len(items)
max_weight = 800
mutationRate = 0.1


class DNA:
    def __init__(self, length, max_w, items, mutationRate):
        self.length = length
        self.max_w = max_w
        self.items = items
        self.mutationRate = mutationRate
        self.genes = []

        for i in range(self.length):
            self.genes.append(random.randint(0,1))

    def calcFitness (self):
        score = 0
        w = 0
        index = 0
        for i in self.genes:
            if i:
                w += items[index]["weight"]
                score += items[index]["value"]
            index += 1
        if w > self.max_w:
            score = 0
        self.weight = w
        self.fitness = (score)
        self.value = score

    
    def crossover (self, parent):
        child = DNA(len(self.genes), self.max_w, self.items, self.mutationRate)

        # midpoint = random.randint(0, len(self.genes) - 1)
        midpoint = math.floor(len(self.genes) / 2)

        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else :
                child.genes[i] = parent.genes[i]
        
        return child
    
    def mutate (self):
        if random.random() < self.mutationRate:
            index = random.randint(0, len(self.genes) - 1)
            if self.genes[index]:
                self.genes[index] = 0
            else:
                self.genes[index] = 1

class Population :
    def __init__(self, pop_size, max_w, items, mutationRate):
        self.pop_size = pop_size
        self.max_w = max_w
        self.items = items
        self.mutationRate = mutationRate

        self.population = []
        for i in range(pop_size):
            self.population.append(DNA(DNA_length, self.max_w, self.items, self.mutationRate))
        

    def calcFitness (self):
        for i in self.population:
            i.calcFitness()

    def naturalSelection (self):
        self.matingPool = []

        self.maxFitness = 0
        bestGen = self.population[0]
        for i in range(len(self.population)):
            if self.population[i].fitness > self.maxFitness:
                self.maxFitness = self.population[i].fitness
                bestGen = self.population[i]
        
        # for i in range(math.floor(len(self.population) / 3)):
        #     self.matingPool.append(bestGen)

        for i in range(len(self.population)):
            if self.maxFitness == 0:
                fitness = 0
            else:
                fitness = self.population[i].fitness / self.maxFitness * 100
            n = math.floor(fitness)
            for i in range(n):
                self.matingPool.append(self.population[i])
    
    def generate (self):
        print(len(self.matingPool))
        if len(self.matingPool) > 0:
            newpop = []
            for i in range(len(self.population)):
                a = random.randint(0, len(self.matingPool) - 1)
                b = random.randint(0, len(self.matingPool) - 1)
                parentA = self.matingPool[a]
                parentB = self.matingPool[b]
                child = parentA.crossover(parentB)
                child.mutate()
                child.calcFitness()
                newpop.append(child)

            self.population = newpop
    
    def evaluate (self, runing, slotions):
        genes = []
        for i in self.population:
            genes.append(''.join(str(e) for e in i.genes))
        
        count = {}
        for i in genes:
            count[i] = genes.count(i)

        mostrepeted = { genes[0]: count[genes[0]] }
        
        for i in count:
            if count[i] > list(mostrepeted.values())[0]:
                mostrepeted = {i : count[i]}
        # print(mostrepeted, end=" ")
        # print(len(self.population))
        # print(mostrepeted)
        index = genes.index(list(mostrepeted.keys())[0])
        slotion = self.population[index].value
        self.slotion = slotion
        plt.plot(np.arange(runing), slotions)
        plt.pause(0.0000000000000000000000000000000000001)
        # if (list(mostrepeted.values())[0]) >= math.floor(len(self.population) / 3):





myPOP = Population(500, max_weight, items, mutationRate)
myPOP.calcFitness()

plt.show()
slotion = []
for i in range(500):
    myPOP.naturalSelection()
    myPOP.generate()
    myPOP.evaluate(i , slotion)
    # print(myPOP.population[0].genes, end=" ")
    # print(myPOP.population[0].fitness)

    slotion.append(myPOP.slotion)

# n = 1024
# X = np.random.normal(0, 1, n)
# Y = np.random.normal(0, 1, n)
# T = np.arctan2(X, Y)

# plt.scatter(np.arange(500), slotion)

# plt.xticks(())
# plt.yticks(())
