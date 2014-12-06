import nfa, itertools

from collections import deque

class DFA:
	def __init__(self):
		self.transitions = {}
		self.accept = {}
		self.start_state = 0

	def add_transition(self, from_state, on_char, to_state):
		if from_state not in self.transitions:
			self.transitions[from_state] = {}

		self.transitions[from_state][on_char] = to_state

	def get_next(self, state, letter):
		return self.transitions.get(state, {}).get(letter)

	def run_on_word(self, word):
		current = self.start_state
		for letter in word:
			current = self.get_next(current, letter)
			if not current:
				return False

		return current in self.accept


def from_nfa(fsa_nfa):
	fsa_dfa = DFA()
	state_cnt = itertools.count()
	Q = {}

	q0 = frozenset(fsa_nfa.get_closure_state(fsa_nfa.start_state))
	Q[q0] = next(state_cnt)
	working_list = deque([q0])

	while working_list:
		q = working_list.pop()
		for letter in fsa_nfa.alphabet:
			next_on_letter = frozenset(fsa_nfa.get_next(q, letter))
			if next_on_letter:
				if next_on_letter not in Q:
					Q[next_on_letter] = next(state_cnt)
					working_list.append(next_on_letter)

				fsa_dfa.add_transition(Q[q], letter, Q[next_on_letter])

	for nfa_state in Q.keys():
		if fsa_nfa.is_accepting(nfa_state):
			fsa_dfa.accept[Q[nfa_state]] = True

	return fsa_dfa

def minimize(fsa_dfa):
	

if __name__ == '__main__':
	fsa = nfa.NFA()

	fsa.add_word('foreach')
	fsa.add_word('for')
	fsa.add_word(' ')

	print(fsa.run_on_word('foreach'))
	print(fsa.run_on_word('for'))
	print("frozenset([1, 2, 4, 8]) == frozenset([1, 2, 4, 8]): " + str(frozenset([1, 2, 4, 8]) == frozenset([1, 2, 4, 8])))

	d = from_nfa(fsa)
	print(d.transitions.keys())
	print(d.accept.keys())
	print(d.transitions)
	print(d.run_on_word('foreach'))
	print(d.run_on_word('for'))
	print(d.run_on_word(' '))

	
