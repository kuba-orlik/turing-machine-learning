import random
import copy

r = random.choice

class StateTransition:
	def __init__(self, states, alphabet, dic=None):
		self.states = states
		self.alphabet = alphabet

		if dic==None:
			self.dic = {}
		else:
			self.dic = dic
		self.fix_holes()

	def __getitem__(self, index):
		if not index in self.dic:
			raise ValueError("Bad key value: " + str(index))
		return self.dic[index]

	def copy(self):
		twin = StateTransition(copy.deepcopy(self.states), copy.copy(self.alphabet), self.dic.copy())
		return twin

	def __contains__(self, index):
		return index in self.dic

	def random_transition(self):
		return (r(self.states), r(self.alphabet), r(["R", "L"]))

	def mutate(self):
		coords = (r(self.states), r(self.alphabet))
		t = self.dic[coords]
		rr = random.randint(0,2)
		if(rr == 0):
			t = (r(self.states), t[1], t[2])
		elif(rr == 1):
			t = (t[0], r(self.alphabet), t[2])
		else:
			t= (t[0], t[1], r(["R", "L"]))
		self.dic[coords] = t

	def update_states(self, new_states):
		self.states = new_states
		self.fix_holes()
		self.cleanup()

	def fix_holes(self):
		for state in self.states:
			for char in self.alphabet:
				key = (state, char)
				if not (key in self.dic):
					self.dic[key] = self.random_transition()
				else:
					value = self.dic[key]
					if not value[0] in self.states:
						value = (r(self.states), value[1], value[2])
					if not value[1] in self.alphabet:
						value = (value[0], r(self.alphabet), value[2])
					self.dic[key] = value


	def cleanup(self):
		keys = list(self.dic.keys())
		for key in keys:
			if (not (key[0] in self.states)) and (not (key[1] in self.alphabet)):
				del self.dic[key]

	def update_alphabet(self, new_alphabet):
		self.alphabet = new_alphabet
		self.fix_holes()
		self.cleanup()

	def rename_state(self, prev_state, new_state):
		keys = list(self.dic.keys())
		for key in keys:
			val = self.dic[key]
			if key[0]==prev_state:
				new_key = (new_state, key[1])
			else:
				new_key = key

			if val[0]==prev_state:
				new_val = (new_state, val[1], val[2])
			else:
				new_val = val

			del self.dic[key]
			self.dic[new_key] = new_val
		self.fix_holes()

	def __mul__(self, other):
		if not self.alphabet == other.alphabet:
			raise ValueError("crossing dictionaries with different alphabets")
		if not self.states == other.states:
			raise ValueError("crossing dictionaries with different states")
		new_dic = {}

		if len(self.dic.keys()) < len(other.dic.keys()):
			keys = self.dic.keys()
		else:
			keys = other.dic.keys()

		# dics can contain unnecessary keys

		for key in keys:
			rr = random.randint(1, 2)
			if rr==1:
				new_dic[key] = self.dic[key]
			else:
				new_dic[key] = other.dic[key]
		return StateTransition(copy.copy(self.states), copy.copy(self.alphabet), new_dic)

	def hash(self):
		ret = ""
		for state in self.states.sort():
			ret += self.dic[(state, self.alphabet[0])][0]
		return ret
