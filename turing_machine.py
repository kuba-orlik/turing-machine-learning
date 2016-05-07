# coding: utf-8

class EC:
	def __repr__(self):
		return "⊔"

EmptyChar = EC()

class TuringMachine:

	def __init__(self, states, in_alphabet, out_alphabet, transition_dictionary, initial_state, accepting_state, rejecting_state):
		self.states = states
		self.in_alphabet = in_alphabet
		self.out_alphabet = out_alphabet
		self.transition_dictionary = transition_dictionary
		self.initial_state = initial_state
		self.accepting_state = accepting_state
		self.rejecting_state = rejecting_state
		self.tape = []
		self.tape_position = 0;

		self.reset()

	def reset(self):
		self.state = self.initial_state

	def input(self, char_array):
		self.reset()
		for char in char_array:
			if(not char in self.in_alphabet):
				raise ValueError('Fed input character not in in_alphabet')
		# self.tape = [EmptyChar] + char_array
		self.tape = char_array

	def step(self):
		if(self.is_finished()):
			raise ValueError("This turing machine has finished")
		transition = self.transition_dictionary[(self.state, self.read_tape())]
		self.state = transition[0]
		self.write(transition[1])
		self.move(transition[2])

	def read_tape(self):
		if(self.tape_position >= len(self.tape)):
			self.tape.append(EmptyChar)
		return self.tape[self.tape_position]

	def write(self, char):
		if(not char in self.out_alphabet):
			raise ValueError("Output character not in out_alphabet")
		self.tape[self.tape_position] = char

	def move(self, direction):
		if(not direction in ["R", "L"]):
			raise ValueError("Move direction should be either 'R' or 'L'")
		if(self.tape_position >= len(self.tape)):
			self.tape.append(EmptyChar)
		if(direction == "R"):
			self.tape_position = self.tape_position + 1
		else:
			self.tape_position = self.tape_position - 1
		if self.tape_position<0:
			self.tape_position = 0

	def is_finished(self):
		return self.state in [self.accepting_state, self.rejecting_state]

	def configuration(self):
		ret = ""
		ret2 = ""
		i = 0
		while i<= max(self.tape_position, len(self.tape)):
			if(i < len(self.tape)):
				ret = ret + str(self.tape[i])
			else:
				ret = ret + str(EmptyChar)
			if(i==self.tape_position):
				ret2 = ret2 + str(self.state)
			else:
				ret2 = ret2 + " "
			i = i + 1
		return ret + "\n" + ret2 + "\n"

	def accepted(self):
		if not self.is_finished():
			return None
		else:
			return self.state == self.accepting_state

	def decide(self, max_steps=float("inf")):
		steps = 0;
		while((not self.is_finished()) and steps < max_steps):
			steps = steps + 1
			self.step()
		return self.accepted()

	def to_dot(self):
		ret = "digraph {\n"
		ret += "{\n"
		ret += "\t" + str(self.accepting_state) + '[fillcolor=green style=filled label="accept" group="flow"];\n'
		ret += "\t" + str(self.rejecting_state) + '[fillcolor="#ff8888" style=filled label="reject" group="flow"];\n'
		ret += "\t" + str(self.initial_state) + '[shape="box" group="flow"];\n'
		ret += "\t" +'start[shape=plaintext label="start" group="flow"];\n'
		ret += "}\n"
		ret += "{rank=same " + str(self.accepting_state) + " " + str(self.rejecting_state) + "}\n"
		ret += "start -> " + str(self.initial_state) + ";\n";
		for state in self.states:
			if state in [self.accepting_state, self.rejecting_state]:
				continue
			for char in self.out_alphabet:
				if (state, char) in self.transition_dictionary:
					t = self.transition_dictionary[(state, char)]
					ret += str(state) + " -> " + str(t[0]) + '[label="' + str(char) + "→" + str(t[1]) + "," + str(t[2]) + '"];\n'
		ret += "}"
		return ret
