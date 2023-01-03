# Imports
import random
import matplotlib.pyplot as plt
import numpy as np

items = [
    {
        "name":"a",
        "w": 2,
        "v": 10
    },
    {
        "name":"b",
        "w": 3,
        "v": 5
    },
    {
        "name":"c",
        "w": 5,
        "v": 15
    },
    {
        "name":"d",
        "w": 7,
        "v": 7
    },
    {
        "name":"e",
        "w": 1,
        "v": 6
    },
    {
        "name":"f",
        "w": 4,
        "v": 18
    },
    {
        "name":"g",
        "w": 1,
        "v": 3
    }
]

items = []

for i in range(100):
    items.append({
        "name": "p",
        "v": random.randint(1,20),
        "w": random.randint(1,10)
    })

MAX_W = 300

POPULATION_SIZE = 200
MUTATION_RATE = 0.8
EPOCH = 300

# O: one-point , N: n-point , U: uniform
REC_METHOD = "O"

# T: Tournament Selection , S: Stochastic Universal , R: Roulette Selection
PARENT_SELC_METHOD = "T"

class DNA:
    def __init__(self, max_w, items, mutationRate, rec_method):
        self.length = len(items)
        self.max_w = max_w
        self.total_weight = 0
        self.items = items
        self.mutationRate = mutationRate
        self.rec_method = rec_method

        self.genes = []
        for i in range(self.length):
            self.genes.append(random.randint(0,1))

    def recombinant(self, parent):
        match self.rec_method:
            case "O":
                return self.o_crossover(parent)
            case "U":
                return self.u_crossover(parent)
            case "N":
                return self.n_crossover(parent)
            case _:
                return self.o_crossover(parent)
    
    def o_crossover(self, parent):
        child = DNA(self.max_w, self.items, self.mutationRate, self.rec_method)
        n_b2 = self.length // 2
        child.genes = self.genes[:n_b2] + parent.genes[n_b2:]
        return child

    def n_crossover(self, parent):
        points = 5
        x = (self.length // (points + 1))
        child = DNA(self.max_w, self.items, self.mutationRate, self.rec_method)
        child.genes = []
        p = 0
        for i in range(points):
            l = len(child.genes)
            if self.length - l < x or p >= points + 1:
                child.genes = child.genes + parent.genes[l:]
                break
            child.genes = child.genes + self.genes[l: l+x]
            l = len(child.genes)
            p += 1
            if self.length - l < x or p >= points + 1:
                child.genes = child.genes + self.genes[l:]
                break
            child.genes = child.genes + parent.genes[l: l+x]
            p += 1

        return child

    def u_crossover(self, parent):
        child = DNA(self.max_w, self.items, self.mutationRate, self.rec_method)
        child.genes = []
        for i in range(self.length):
            r = random.randint(0, 1)
            if r:
                child.genes.append(self.genes[i])
            else:
                child.genes.append(parent.genes[i])

        return child

    def mutate (self):
        if random.random() < self.mutationRate:
            index = random.randint(0, len(self.genes) - 1)
            if self.genes[index]:
                self.genes[index] = 0
            else:
                self.genes[index] = 1

    def calcFitness(self):
        self.total_weight = 0
        total_value = 0
        index = 0
        for i in self.genes:
            if i:
                self.total_weight += items[index]["w"]
                total_value += items[index]["v"]
            index += 1
        self.value = total_value
        if self.total_weight>self.max_w:
            self.value = 0
        self.w_d = abs(self.max_w - self.total_weight) 



class Population :
    def __init__(self, pop_size, max_w, items, mutationRate, rec_method, parent_selc_method):
        self.pop_size = pop_size
        self.max_w = max_w
        self.items = items
        self.mutationRate = mutationRate
        self.parent_selc_method = parent_selc_method
        self.rec_method = rec_method

        self.population = []
        for i in range(pop_size):
            self.population.append(DNA(self.max_w, self.items, self.mutationRate, self.rec_method))
        
        self.calcFitness()
    
    def generate(self):
        new_pop = []
        for i in range(self.pop_size):
            parentA, parentB = self.selector()
            child = parentA.recombinant(parentB)
            child.mutate()
            child.calcFitness()
            new_pop.append(child)
        
        self.population = new_pop
    
    def calcFitness(self):
        for i in self.population:
            i.calcFitness()

    def selector(self):
        match self.parent_selc_method:
            case "T":
                return self.t_selector()

    def sort_by_value_w_d(self, pop=[]):
        return sorted(pop, key=lambda x: (-x.value, x.w_d))
    
    def t_selector(self):
        k = 5
        selecteds_p1 = []
        selecteds_p2 = []
        for i in range(3):
            r_index1 = random.randint(0, self.pop_size - 1)
            r_index2 = random.randint(0, self.pop_size - 1)
            selecteds_p1.append(self.population[r_index1])
            selecteds_p2.append(self.population[r_index2])
        
        parent_1 = self.sort_by_value_w_d(selecteds_p1)[0]
        parent_2 = self.sort_by_value_w_d(selecteds_p2)[0]

        return parent_1, parent_2
    
    def sort_selector(self):
        sortend_list = sorted(self.population, key=lambda x: (-x.value, x.w_d))

        self.population = sortend_list


    def kill(self):
        self.population = self.population[:self.pop_size]
    
    def get_best_in_generation(self):
        return self.sort_by_value_w_d(self.population)[0]

myPOP = Population(POPULATION_SIZE, MAX_W, items, MUTATION_RATE, REC_METHOD, PARENT_SELC_METHOD)
best_values = []
best_weight = []
index = 0

# best value found position
bvfp = {
    "x": 0,
    "v": 0
}

while EPOCH:
    myPOP.calcFitness()
    myPOP.generate()
    # myPOP.sort_selector()
    # myPOP.kill()
    
    index += 1

    best = myPOP.get_best_in_generation()

    if bvfp["v"] < best.value:
        bvfp["v"] = best.value
        bvfp["x"] = index
    
    best_values.append(best.value)

    EPOCH -= 1


print("############################################")


print("best genes  : ", end="")
print(best.genes)

print("best value  : ", end="")
print(best.value)

print("total weight: ", end="")
print(best.total_weight)

print("############################################")


plt.scatter(bvfp["x"], bvfp["v"])
plt.text(bvfp["x"], bvfp["v"] + 1, "best value: "+ str(bvfp["v"]) + " gen: " + str(bvfp["x"]), 
         bbox = dict(facecolor = 'red', alpha = 0.5))

plt.plot(np.arange(index), best_values)
plt.show()

