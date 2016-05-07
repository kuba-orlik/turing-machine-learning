from weightedset import WeightedRandomSetWithReplacement
import random

sexual_reproduction_percent = 20
asexual_reproduction_percent = 10
max_mutation_strength = 3

class Population:

	def __init__(self, generator, size, fitness_function):
		self.generator = generator
		self.size = size
		self.fitness_function = fitness_function
		self.instances = []
		self.populate()

	def populate(self):
		for i in range(self.size):
			self.instances.append(self.generator())

	def weigh_population(self):
		s = WeightedRandomSetWithReplacement()
		for instance in self.instances:
			s.add(instance, self.fitness_function(instance))
		return s

	def generations(self, iterations=1):
		for i in range(iterations):
			self.generation()

	def generation(self):
		s = self.weigh_population()

		to_add = []

		for i in range(int(len(s) * sexual_reproduction_percent / 100)):
			mate1 = s.draw()
			mate2 = s.draw()
			kid = mate1 * mate2
			to_add.append(kid)

		for i in range(int(len(s) * asexual_reproduction_percent / 100)):
			instance = s.draw()
			for i in range(1, random.randint(1, max_mutation_strength)):
				instance = instance.mutate()
			to_add.append(instance)

		for instance in to_add:
			s.add(instance, self.fitness_function(instance))

		new_population = s._members[-self.size:]
