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

	#print("Build machine for word: " + lexeme)
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

	#print("Build machine for alternative: " + str(alt_letters))
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

	#print("Build machine for negation: " + str(neg_letters))
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

	#print("Build machine for repetition: " + str(repetition_range))
	return i, repetition_range

def parse_any(in_str, i):
	if in_str[i] != 'x':
		return None
	#i += 1
	#print("Build machine for any")
	return i, PROSITE_ALPHABET_SET

def compile(regex):
	i = 0
	argument = None

	prosite_nfa = nfa.NFA()
	create_matcher_func = None
	append_to_state = [prosite_nfa.start_state]


	while i < len(regex) and regex[i] is not '.':
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
	#	else:
			# Error - not known symbol
	#		return None

		i += 1

		rep = range(1, 2)
		if i < len(regex) and regex[i] == '(':
			i, repetition_range = parse_repetition(regex, i)
		
			begin = int(repetition_range[0])
			end = int(repetition_range[-1]) + 1
			rep = range(begin, end)

			i += 1

		append_to_state = prosite_nfa.create_repetition_matcher_experimental(rep, create_matcher_func, argument, append_to_state)

	for state in append_to_state:
		prosite_nfa.accept.add(state)

	return dfa.minimize(dfa.from_nfa(prosite_nfa))



if __name__ == '__main__':
	regex = 'C-G-G-x(4,7)-{ABC}-G-x(3)-C-x(5)-C-x(3,5)-[NHG]-x-[FYWM]-x(2)-Q-C'
	valid = "CGGVVVVNGVVVCVVVVVCVVVGVMVVQC"
	valid2 = "CGGVVVVNGVVVCVVVVVCVVVVGVMVVQC"

	import time

	print("COMPILE START")
	start = time.clock()
	prosite_dfa = compile(regex)
	end = time.clock()
	compile_time = end - start
	print("COMPILE END")

	print("DFA MATCH START")
	is_valid_dfa = False
	start = time.clock()
	for i in range(0, 20000):
		is_valid = prosite_dfa.run_on_word(valid)
	end = time.clock()
	dfa_match_time = (end - start) / 20000.0
	print("DFA MATCH END")

	print("DFA match time: " + str('{0:.20f}'.format(float(dfa_match_time))))
	print("Compile time: " + str('{0:.20f}'.format(float(compile_time))))

	print(is_valid == True)