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

		current_lexeme = ""
		last_start = 0
		last_accept_pos = -1
		
		i = 0
		while i < len(text):
			while i < len(text) and current_state != None:
				current_state = self.machine.get_next(current_state, text[i])
				if current_state != None:
					current_lexeme += text[i]

					if current_state in self.machine.accept:
						last_accept_pos = i
				else:
					break

				i += 1

			if last_accept_pos != -1:
				i = last_accept_pos + 1
				valid_lexeme = current_lexeme[:last_accept_pos + 1]
				ranges.append(range(last_accept_pos - len(valid_lexeme) + 1 , last_accept_pos + 1))
				lexemes.append(valid_lexeme)
				last_accept_pos = -1
			else:
				i += 1

			current_lexeme = ""
			current_state = self.machine.start_state

		return lexemes, ranges

if __name__ == '__main__':
	pm = PrositeMatcher()
	pm.compile("C-G-G")
	print(pm.match("CGG"))
	matches, ranges = pm.get_matches("CGGAAAACGGaasdsadsadsadCGGdsadCGGCGGCGG")
	print(matches)
	print(ranges)