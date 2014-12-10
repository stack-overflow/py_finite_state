#!/bin/env python3
# Prosite regular expressions matcher
# Copyright (c) 2014 Tomasz Truszkowski
# All rights reserved.

import prosite_compiler

class PrositeMatcher:
	def __init__(self):
		self.machine = None
		self.pattern = None

	def compile(self, pattern):
		self.pattern = pattern
		self.machine = prosite_compiler.compile(pattern)

	def match(self, word):
		return self.machine.run_on_word(word)

	def get_matches(self, text):
		current_state = self.machine.start_state
		lexemes = []
		ranges = []

		lexeme_len = 0
		lexeme = ""
		last_start = 0
		last_accept_pos = -1
		
		i = 0
		while i < len(text):
			while i < len(text) and current_state != None:
				current_state = self.machine.get_next(current_state, text[i])
				if current_state != None:
					lexeme_len += 1
					lexeme += text[i]

					if current_state in self.machine.accept:
						last_accept_pos = i
				else:
					break

				i += 1

			if last_accept_pos != -1:
				i = last_accept_pos + 1
				valid_lexeme_end = last_accept_pos
				valid_lexeme_start = valid_lexeme_end - lexeme_len + 1
				ranges.append(range(valid_lexeme_start, valid_lexeme_end + 1))

				# Not needed as function returns list of positions in original text
				lexeme = lexeme[:last_accept_pos + 1]
				lexemes.append(lexeme)

				last_accept_pos = -1
			else:
				i += 1

			lexeme_len = 0
			lexeme = ""
			current_state = self.machine.start_state

		return lexemes, ranges

if __name__ == '__main__':
	pm = PrositeMatcher()
	pm.compile("C-G-G")
	print(pm.match("CGG"))
	text = "CGGAAAACGGaasdsadsadsadCGGdsadCGGCGGCGG"
	matches, ranges = pm.get_matches(text)

#	for match in ranges:
#		for i in match:
#			print(text[i], end="")
#		print()

	print(matches)
	print(ranges)