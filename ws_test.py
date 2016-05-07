from population import Population
from random import randint

def nz(i):
	if(i<0):
		return 0
	else:
		return i

class Mutable:

	def __init__(self, number=None):
		if(number==None):
			self.number = randint(0, 10)
		else:
			self.number = number

	def mutate(self):
		rr = randint(-1,1)
		return Mutable(nz(self.number + rr))

	def __mul__(self, other):
		return Mutable(max(self.number, other.number))

def generator():
	return Mutable()

def fitness_function(a):
	return a.number


p = Population(generator, 10, fitness_function)

p.generations(1000)

print("fitness:", fitness_function(p.population[0]))
