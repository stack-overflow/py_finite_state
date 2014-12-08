#!/bin/env python3
# Prosite regular expressions parser and compilator
# Copyright (c) 2014 Tomasz Truszkowski
# All rights reserved.
import string

import nfa
import dfa

PROSITE_ALPHABET_SET = set(string.ascii_uppercase)

def nfa_for_word(word):
	lexeme_nfa = nfa.NFA()
	lexeme_nfa.add_word(lexeme)
	return lexeme_nfa

def parse_uppercase(in_str, i):
	lexeme = ""
	while i < len(in_str) and (in_str[i].isupper() or in_str[i] == '-'):
		while in_str[i] == '-':
			i += 1
		if i >= len(in_str):
			break
		if in_str[i].isupper():
			lexeme += in_str[i]
			i += 1

	if i < len(in_str):
		if not in_str[i].isupper() and in_str[i] != '-':
			i -= 1

	print("Build machine for word: " + lexeme)
	return i, lexeme

def parse_alternative(in_str, i):
	if in_str[i] != '[':
		return None
	i += 1
	alt_letters = set()
	while  i < len(in_str) and in_str[i] != ']':
		if not in_str[i].isupper():
			return None
		alt_letters.add(in_str[i])
		i += 1

	print("Build machine for alternative: " + str(alt_letters))
	return i, alt_letters

def parse_negation(in_str, i):
	if in_str[i] != '{':
		return None
	i += 1
	neg_letters = set()
	while  i < len(in_str) and in_str[i] != '}':
		if not in_str[i].isupper():
			return None
		neg_letters.add(in_str[i])
		i += 1

	print("Build machine for negation: " + str(neg_letters))
	return i, PROSITE_ALPHABET_SET - neg_letters

def parse_repetition(in_str, i):
	if in_str[i] != '(':
		return None
	i += 1
	repetition_range = []
	num = ""
	while  i < len(in_str) and in_str[i] != ')':
		if not in_str[i].isdigit() and in_str[i] != ',':
			return None

		if in_str[i] == ',':
			repetition_range.append(num)
			num = ""
		else:
			num += in_str[i]
		i += 1

	repetition_range.append(num)

	print("Build machine for repetition: " + str(repetition_range))
	return i, repetition_range

def parse_any(in_str, i):
	if in_str[i] != 'x':
		return None
	#i += 1
	print("Build machine for any")
	return i, PROSITE_ALPHABET_SET

if __name__ == '__main__':
	regex = 'C-G-G-x(4,7)-{ABC}-G-x(3)-C-x(5)-C-x(3,5)-[NHG]-x-[FYWM]-x(2)-Q-C'
	valid = "CGGVVVVNGVVVCVVVVVCVVVGVMVVQC"

	machine_parts = []
	i = 0
	state = 0
	lexeme = ""
	argument = None

	prosite_nfa = nfa.NFA()
	create_matcher_func = None
	append_to_state = prosite_nfa.start_state

	while i < len(regex):
		while regex[i] == '-':
			i += 1
		if regex[i].isupper():
			i, argument = parse_uppercase(regex, i)
			create_matcher_func = prosite_nfa.create_word_matcher
		elif regex[i] == 'x':
			i, argument = parse_any(regex, i)
			create_matcher_func = prosite_nfa.create_any_matcher
		elif regex[i] == '[':
			i, argument = parse_alternative(regex, i)
			create_matcher_func = prosite_nfa.create_any_matcher
		elif regex[i] == '{':
			i, argument = parse_negation(regex, i)
			create_matcher_func = prosite_nfa.create_any_matcher

		i += 1

		rep = 1
		if i < len(regex) and regex[i] == '(':
			i, repetition_range = parse_repetition(regex, i)
			#print("Repetition: " + repetition_range[0])
			rep = int(repetition_range[0])
			i += 1

		end_state = prosite_nfa.create_repetition_matcher(rep, create_matcher_func, argument, append_to_state)
		append_to_state = end_state

	prosite_nfa.accept.add(append_to_state)
	prosite_dfa = dfa.from_nfa(prosite_nfa)

	print(prosite_dfa.run_on_word(valid))
	min_prosite_dfa = dfa.minimize(prosite_dfa)
	print(min_prosite_dfa.run_on_word(valid))
	print("Non minimal DFA transitions table size: " + str(len(prosite_dfa.transitions)))
	print("Minimal DFA transitions table size: " + str(len(min_prosite_dfa.transitions)))

	print("DFA: " + str(prosite_dfa.transitions.keys()))
	print("MDFA: " + str(min_prosite_dfa.transitions.keys()))



#			elif regex[i] == 'x':
#				state = ParserState.seen_x
#			elif regex[i] == '[':
#				state = ParserState.seen_alternative
#			elif regex[i] == '{':
#				state = ParserState.seen_negation

#print(machine_parts)
