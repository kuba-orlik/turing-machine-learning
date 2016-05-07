from population import Population
from mutable_hl_tl import MutableHLTM
import number_encoders

def go():
	def is_power_of_two(i):
		while i>1:
			if i%2 == 1:
				return False
			i = i // 2
		return True

	def grade_answers(htm, steps):
		tp = 0
		fp = 0
		tn = 0
		fn = 0
		for i in range(steps + 1):
			res = htm.decide(i)
			truth = is_power_of_two(i)
			if truth == True:
				if res == True:
					tp += 1
				elif res == False:
					fp += 1
				else:
					fn += 1 #dubious?
			else:
				if res == True:
					fn += 1
				elif res == False:
					tn += 1
				else:
					fp += 1 #dubious?
		return f(tp, fp, fn, 0.5)

	def f(true_positive, false_positive, false_negative, beta=1):
		top = ((1 + beta ** 2) * true_positive)
		bottom = ((1+beta**2)*true_positive + beta**2 * false_negative + false_positive)
		if bottom == 0:
			return 0
		else:
			return top/bottom

	def fitness_function(mhltm, sample_size=33):
		htm = mhltm.htm
		trivial_cases = range(0,5)
		for i in trivial_cases:
			if is_power_of_two(i) != htm.decide(i):
				return 0
		# return 1 + 99 * (grade_answers(htm, sample_size)/len(htm.states))
		return 1 + 99 * (grade_answers(htm, sample_size))

	def generator():
		return MutableHLTM(12, number_encoders.unary, 1)

	p = Population(generator, 50, fitness_function)

	p.generations(1000)


	print(p.population[0].to_dot())

	print("\n\n")

	print("fitness_function(p.population[0])", fitness_function(p.population[0]))

	print(fitness_function(p.population[0], 200))

	for i in range(17):
		print(i, p.population[0].htm.decide(i))

# import cProfile
#
# cProfile.run('go()', "stats")

go()
