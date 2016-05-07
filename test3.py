from population import Population
from mutable_hl_tl import MutableHLTM
import number_encoders

def fitness_function(mhltm):
	return 1/len(mhltm.htm.states)

def generator():
	return MutableHLTM(10, number_encoders.unary, 2)

p = Population(generator, 10, fitness_function)

p.generations(100)
