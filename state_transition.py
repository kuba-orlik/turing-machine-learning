import random

r = random.choice

class StateTransition:
	def __init__(self, states, alphabet, dic=None):
		self.states = states
		self.alphabet = alphabet

		if dic==None:
			self.dic = {}
			i = 0
			while i < len(states):
				j = 0
				while j < len(alphabet):
					self.dic[(self.states[i], self.alphabet[j])] = self.random_transition()
					j += 1
				i += 1
		else:
			self.dic = dic

	def __getitem__(self, index):
		return self.dic[index]

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
			t = (t[0], r(self.alphabet), t[1])
		else:
			t= (t[0], t[1], r(["R", "L"]))
		self.dic[coords] = t

	def update_states(self, new_states):

		states_to_add = []
		for state in new_states:
			if not state in self.states:
				states_to_add.append(state)

		self.states = new_states
		for state in states_to_add:
			for char in self.alphabet:
				if not (state, char) in self.dic:
					self.dic[(state, char)] = self.random_transition()

		self.cleanup()

	def cleanup(self):
		keys = list(self.dic.keys())
		for key in keys:
			if (not (key[0] in self.states)) and (not (key[1] in self.alphabet)):
				del self.dic[key]

	def update_alphabet(self, new_alphabet):

		chars_to_add = []
		for char in new_alphabet:
			if not char in self.alphabet:
				chars_to_add.append(char)

		self.alphabet = new_alphabet

		for char in chars_to_add:
			for state in self.states:
				if not ((state, char) in self.dic):
					self.dic[(state, char)] = self.random_transition()

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
			rr = random.randint(1, 3)
			if rr==1:
				new_dic[key] = self.dic[key]
			else:
				new_dic[key] = other.dic[key]
		return StateTransition(self.states, self.alphabet, new_dic)

	def hash(self):
		ret = ""
		for state in self.states.sort():
			ret += self.dic[(state, self.alphabet[0])][0]
		return ret
