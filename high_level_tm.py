from turing_machine import TuringMachine, EmptyChar as e
from state_transition import StateTransition

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
		return TuringMachine(self.states, self.in_alphabet, self.out_alphabet, self.transition_dictionary, self.states[0], self.states[-2], self.states[-1])

	# def cross_over
