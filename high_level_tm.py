from turing_machine import TuringMachine, EmptyChar as e
from state_transition import StateTransition
import copy

class HighLevelTM:

	def __init__(self, states, encoder, control_chars, transition_dictionary=None):
		self.encoder = encoder
		self.states = states

		self.in_alphabet = encoder.get_alphabet()
		self.out_alphabet = self.in_alphabet + control_chars + [e]
		if transition_dictionary == None:
			self.transition_dictionary = StateTransition(self.states, self.out_alphabet)
		else:
			self.transition_dictionary = transition_dictionary

	def get_machine(self):
		return TuringMachine(self.states[:], self.in_alphabet[:], self.out_alphabet[:], copy.copy(self.transition_dictionary), self.states[0], self.states[-2], self.states[-1])

	def to_dot(self):
		return self.get_machine().to_dot()

	def run(self, input_data):
		machine = self.get_machine()
		encoded_data = self.encoder.encode(input_data)
		machine.input(encoded_data)
		machine.decide(max_steps=len(encoded_data) * 100)
		return machine

	def calculate(self, input_data):
		machine = self.run(input_data)
		if machine.is_finished():
			return self.encoder.decode(machine.tape)
		else:
			return None

	def decide(self, input_data):
		machine = self.run(input_data)
		return machine.accepted()

	# def cross_over
