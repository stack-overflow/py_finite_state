import nfa
import dfa

from enum import Enum

class ParserState(Enum):
	seen_nothing = 0
	seen_uppercase = 1
	seen_x = 2
	seen_alternative = 3
	seen_negation = 4
	change_state = 5
	error = 6

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
	machine = nfa_for_word(lexeme)
	return i, machine

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
	return i, neg_letters

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
	return i

def parse_any(in_str, i):
	if in_str[i] != 'x':
		return None

	#i += 1
	print("Build machine for any")
	return i

if __name__ == '__main__':
	regex = 'C-G-G-x(4,7)-{ABC}-G-x(3)-C-x(5)-C-x(3,5)-[NHG]-x-[FYWM]-x(2)-Q-C'

	machine_parts = []
	i = 0
	state = 0
	lexeme = ""

	while i < len(regex):
		while regex[i] == '-':
			i += 1
		if regex[i].isupper():
			i, lexeme_nfa = parse_uppercase(regex, i)
			machine_parts.append(lexeme_nfa)
		elif regex[i] == 'x':
			i = parse_any(regex, i)
		elif regex[i] == '[':
			i, machine = parse_alternative(regex, i)
		elif regex[i] == '{':
			i, machine = parse_negation(regex, i)
		elif regex[i] == '(':
			i = parse_repetition(regex, i)
		else:
			print("lolzord")

		i += 1
#			elif regex[i] == 'x':
#				state = ParserState.seen_x
#			elif regex[i] == '[':
#				state = ParserState.seen_alternative
#			elif regex[i] == '{':
#				state = ParserState.seen_negation

#print(machine_parts)
