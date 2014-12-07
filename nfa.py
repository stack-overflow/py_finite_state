#!/bin/env python3

class NFA:
	def __init__(self):
		self.transitions = {}
		self.start_state = 0
		self.num_states = 1
		self.accept = set()
		self.epsilon = type("epsilon", (object,), {})()
		self.alphabet = set()

	def add_transition(self, from_state, on_char, to_state):
		if from_state not in self.transitions:
			self.transitions[from_state] = {}

		if on_char not in self.transitions[from_state]:
			self.transitions[from_state][on_char] = []

		if on_char not in self.alphabet and on_char != self.epsilon:
			self.alphabet.add(on_char)

		self.transitions[from_state][on_char].append(to_state)

	def get_closure_state(self, state):
		on_epsilon_moves = self.get_next_state(state, self.epsilon)

		closure = [state]
		for work_state in on_epsilon_moves:
			closure.extend(self.get_closure_state(work_state))

		return closure

	def get_closure(self, states):
		closure = []
		for state in states:
			closure.extend(self.get_closure_state(state))

		return closure

	def get_next_state(self, state, on_char):
		return self.transitions.get(state, {}).get(on_char, [])

	def get_next(self, states, on_char):
		next_states = []
		for state in self.get_closure(states):
			next_states.extend(self.get_next_state(state, on_char))
		return self.get_closure(next_states)

	def increment_states(self):
		current = self.num_states
		self.num_states += 1
		return current

	def add_word_no_epsilon(self, word):
		current_state = self.start_state
		for letter in word:
			next_state = self.increment_states()
			self.add_transition(current_state, letter, next_state)
			current_state = next_state

		#self.accept[next_state] = True
		self.accept.add(next_state)

	def add_word(self, word):
		first_state = self.increment_states()
		self.add_transition(self.start_state, self.epsilon, first_state)

		current_state = first_state
		for letter in word:
			next_state = self.increment_states()
			self.add_transition(current_state, letter, next_state)
			current_state = next_state

		#self.accept[next_state] = True
		self.accept.add(next_state)

	def is_accepting_state(self, state):
		if state in self.accept:
			return True
		return False

	def is_accepting(self, set_states):
		for state in set_states:
			if self.is_accepting_state(state):
				return True
		return False

	def run_on_word(self, word):
		current = self.get_closure_state(self.start_state)
		i = 0;
		for letter in word:
			current = self.get_next(current, word[i])
			i += 1
			if not current:
				return False

		return self.is_accepting(current)


if __name__ == '__main__':
	nfa = NFA()
	nfa.add_word('foreach')
	nfa.add_word('for')
	nfa.add_word('cat')
	nfa.add_word('sublime')
	nfa.add_word('vim')
	nfa.add_word('python')

	word = 'foreach'
	if nfa.run_on_word(word):
		print(word + " was accepted")
	else:
		print (word + " was rejected")
