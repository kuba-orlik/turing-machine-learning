import random
import copy
from high_level_tm import HighLevelTM

def generate_transition_chars(amount):
	return list(map(chr, list(range(65, 65+amount))))


class MutableHLTM:

	def __init__(self, max_states, encoder, max_control_characters, states=None, transition_dictionary=None):
		self.max_states = max_states
		self.encoder = encoder
		self.max_control_characters = max_control_characters

		if states == None:
			states = list(range(0, random.randint(3,max_states)))
		self.control_chars = generate_transition_chars(max_control_characters)

		self.htm = HighLevelTM(states, encoder, self.control_chars, transition_dictionary=transition_dictionary)

	def hash(self):
		return str(len(self.states)) + "-" + self.htm.transition_dictionary.hash()

	def __mul__(self, other):
		states_amount = random.choice([len(self.htm.states), len(other.htm.states)])
		states = list(range(0, states_amount))
		dic1 = copy.copy(self.htm.transition_dictionary)
		dic2 = copy.copy(other.htm.transition_dictionary)
		dic1.update_states(states)
		dic2.update_states(states)

		out_alphabet = random.choice([self.htm.out_alphabet, other.htm.out_alphabet])
		dic1.update_alphabet(out_alphabet)
		dic2.update_alphabet(out_alphabet)

		dic = dic1 * dic2
		return MutableHLTM(self.max_states, self.encoder, self.max_control_characters, states, dic)


	def mutate(self, quantity=1):
		i = 0;
		ret = self
		while i<quantity:
			i+=1
			rr = random.randint(1, 10)
			if(rr==1):
				ret = ret.mutate_states()
			else:
				ret = ret.mutate_transition()
		return ret

	def mutate_states(self):
		rr = random.randint(1, 2)
		states = copy.copy(self.htm.states)
		transition_dictionary = copy.copy(self.htm.transition_dictionary)

		if(rr == 1):
			if(len(states) < self.max_states):
				i=0
				found = False
				while i<len(states):
					if i not in states:
						states.append(i)
						states.sort()
						found = True
						break
					i+=1
				if not found:
					states.append(max(states) + 1)
		else:
			if(len(states) > 3):
				del states[random.randint(0, len(states)-1)]

		i=0
		while i<len(states):
			if not states[i]==i:
				transition_dictionary.rename_state(states[i], i)
				states[i] = i
			i+=1

		transition_dictionary.update_states(states)
		return MutableHLTM(self.max_states, self.encoder, self.max_control_characters, states=states, transition_dictionary=transition_dictionary)

	def mutate_transition(self):
		states = copy.copy(self.htm.states)
		transition_dictionary = copy.copy(self.htm.transition_dictionary)
		transition_dictionary.mutate()
		return MutableHLTM(self.max_states, self.encoder, self.max_control_characters, states=states, transition_dictionary=transition_dictionary)

	def get_machine(self):
		return self.htm.get_machine()
