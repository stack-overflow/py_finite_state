#!/bin/env python3
# Deterministic Finite State Automaton
# Copyright (c) 2014 Tomasz Truszkowski, Mateusz Zych, Kamil Majcher
# All rights reserved.

import nfa, itertools

from collections import deque

class DFA:
	def __init__(self):
		self.transitions = {}
		self.accept = set()
		self.start_state = 0
		self.alphabet = frozenset()

	def add_transition(self, from_state, on_char, to_state):
		if from_state not in self.transitions:
			self.transitions[from_state] = {}

		self.transitions[from_state][on_char] = to_state

	def get_next(self, state, letter):
		ret = self.transitions.get(state, {}).get(letter)
		return  ret

	def run_on_word(self, word):
		current = self.start_state
		for letter in word:
			current = self.get_next(current, letter)
			if current == None:
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
			#fsa_dfa.accept[Q[nfa_state]] = True
			fsa_dfa.accept.add(Q[nfa_state])

	fsa_dfa.alphabet = fsa_nfa.alphabet

	return fsa_dfa

def which_set(state, partition):
	if not state:
		return None

	for set_state in partition:
		if state in set_state:
			return set_state

	return None

def set_states_split(dfa, set_states, partition):
	if len(set_states) < 2:
		return { set_states }

	head, *tail = set_states

	for letter in dfa.alphabet:
		next_set = which_set(dfa.get_next(head, letter), partition)
		first_states = set([head])
		for state in tail:
			next_for_state = which_set(dfa.get_next(state, letter), partition)
			if next_for_state != next_set:
				second_states = set_states - first_states
				ret = { frozenset(first_states) }

				if second_states:
					ret.add(frozenset(second_states))
				return ret

			first_states.add(state)

	return { set_states }


def minimize(dfa):
	states_all = frozenset(dfa.transitions.keys())
	states_accept = frozenset(dfa.accept)
	states_rest = states_all - states_accept

	T = set([ states_accept, states_rest ])
	P = set()

	while T != P:
		P = T
		T = set()
		for set_states in P:
			T |= set_states_split(dfa, set_states, P)

	set_to_state = dict()
	final_states = set()
	start_state = 0
	num_states = 0
	for set_states in T:
		set_to_state[set_states] = num_states
		if set_states & dfa.accept:
			final_states.add(num_states)
		if dfa.start_state in set_states:
			start_state = num_states

		num_states += 1
	
	minimal_dfa = DFA()
	minimal_dfa.accept = final_states
	minimal_dfa.start_state = start_state
	minimal_dfa.alphabet = dfa.alphabet

	transitions = dict()
	for set_states in T:
		current_id = set_to_state[set_states]
		some_state = set(set_states).pop()
		for letter in dfa.alphabet:
			next_state = dfa.get_next(some_state, letter)
			if next_state:
				next_set = which_set(next_state, T)
				next_id = set_to_state[next_set]
				#print("FROM " + str(current_id) + " TO " + str(next_id) + " ON " + letter)
				minimal_dfa.add_transition(current_id, letter, next_id)

	return minimal_dfa


if __name__ == '__main__':
	fsa = nfa.NFA()

	fsa.add_word('fie')
	fsa.add_word('fee')

	print(fsa.run_on_word('fie'))
	print(fsa.run_on_word('fee'))

	d = from_nfa(fsa)

	print(d.run_on_word('fie'))
	print(d.run_on_word('fee'))
	
	minimal_d = minimize(d)

	print("DFA states: " + str(d.transitions.keys()))
	print("MDFA states: " + str(minimal_d.transitions.keys()))

	print("DFA transitions: " + str(d.transitions))
	print("MDFA transitions: " + str(minimal_d.transitions))

	print("DFA start_state: " + str(d.transitions.keys()))
	print("MDFA start_state: " + str(minimal_d.transitions.keys()))

	print(minimal_d.run_on_word('fie'))
	print(minimal_d.run_on_word('fee'))	


	print("TEST MINIMIZE")

	test_n = nfa.NFA()
	d1 = test_n.increment_states()
	test_n.add_transition(test_n.start_state, 'a', d1)
	d2 = test_n.increment_states()
	test_n.add_transition(d1, 'b', d2)
	test_n.add_transition(d2, 'b', d2)
	d3 = test_n.increment_states()
	test_n.add_transition(d1, 'c', d3)
	test_n.add_transition(d3, 'c', d3)

	test_n.add_transition(d3, 'b', d2)
	test_n.add_transition(d2, 'c', d3)

	test_n.accept.add(d1)
	test_n.accept.add(d2)
	test_n.accept.add(d3)

	print(test_n.run_on_word('a'))
	print(test_n.run_on_word('ab'))
	print(test_n.run_on_word('abbbbccc'))

	test_d = from_nfa(test_n)
	print(test_d.transitions)

	print(test_d.run_on_word('a'))
	print(test_d.run_on_word('ab'))
	print(test_d.run_on_word('abbbbccc'))

	min_test_d = minimize(test_d)
	print(min_test_d.transitions)

	print(min_test_d.run_on_word('a'))
	print(min_test_d.run_on_word('ab'))
	print(min_test_d.run_on_word('abbbbccc'))