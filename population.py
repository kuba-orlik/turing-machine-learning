from weightedset import WeightedRandomSetWithReplacement
import random

sexual_reproduction_percent = 50
asexual_reproduction_percent = 50
max_mutation_strength = 100

class Population:

	def __init__(self, generator, size, fitness_function):
		self.generator = generator
		self.size = size
		self.fitness_function = fitness_function
		self.population = WeightedRandomSetWithReplacement(fitness_function)
		self.populate()

	def populate(self, amount=None):
		if(amount==None):
			amount = self.size
		print("\tpopulating...")
		while len(self.population) < self.size:
			instance = self.generator()
			self.population.add(instance)
			print (len(self.population), "/", self.size)

	def generations(self, iterations=1):
		for i in range(iterations):
			print("generation", i, "population", len(self.population))
			print("\tbest rank:", self.fitness_function(self.population[0]))
			self.generation()

	def mutate(self):
		print("\tmutating...")
		to_add = []
		for i in range(int(len(self.population) * asexual_reproduction_percent / 100)):
			instance = self.population.draw()
			for i in range(1, random.randint(1, max_mutation_strength)):
				mutant = instance.mutate()
				if mutant not in self.population:
					to_add.append(mutant)
		print("\tadding", str(len(to_add)), "mutated instances to population...")
		for instance in to_add:
			self.population.add(instance)

	def cross(self):
		to_add = []

		print("\tcrossing...")
		for i in range(int(len(self.population) * sexual_reproduction_percent / 100)):
			mate1 = self.population.draw()
			mate2 = self.population.draw()
			kid = mate1 * mate2
			if kid not in self.population:
				to_add.append(kid)
		print("\tadding", str(len(to_add)), "crossed items to population...")
		for instance in to_add:
			self.population.add(instance)

	def generation(self):
		if random.randint(1,2) == 1:
			self.mutate()
			self.cross()
		else:
			self.cross()
			self.mutate()

		print("\tkilling inefficient ones...")
		self.population.trim(self.size)
