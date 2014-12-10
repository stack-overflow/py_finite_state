import string
import unittest

import nfa
import dfa

class TestNFA(unittest.TestCase):
	def test_add_word(self):
		machine = nfa.NFA()
		machine.add_word('kot')
		machine.add_word('cat')
		machine.add_word('foreach')
		
		kot_result = machine.run_on_word('kot')
		cat_result = machine.run_on_word('cat')
		foreach_result = machine.run_on_word('foreach')

		self.assertTrue(kot_result)
		self.assertTrue(cat_result)
		self.assertTrue(foreach_result)

	def test_get_next(self):
		machine = nfa.NFA()
		machine.add_word('cat')
		current_state = [machine.start_state]

		first_state = machine.get_next(current_state, 'c')
		second_state = machine.get_next(first_state, 'a')
		third_state = machine.get_next(second_state, 't')

		self.assertTrue(first_state)
		self.assertTrue(second_state)
		self.assertTrue(third_state)

	def test_get_next_and_acceptance(self):
		machine = nfa.NFA()
		machine.add_word('cat')
		current_state = [machine.start_state]

		first_state = machine.get_next(current_state, 'c')
		second_state = machine.get_next(first_state, 'a')
		third_state = machine.get_next(second_state, 't')

		self.assertTrue(machine.is_accepting(third_state))

	def test_create_matchers(self):
		manual_nfa = nfa.NFA()
		kot_end = manual_nfa.create_word_matcher("kot", [manual_nfa.start_state])
		manual_nfa.accept.add(kot_end)

		self.assertTrue(manual_nfa.run_on_word("kot"))
		self.assertFalse(manual_nfa.run_on_word("foreach"))

		any_end = manual_nfa.create_any_matcher(string.ascii_uppercase, [kot_end])
		manual_nfa.accept.add(any_end)

		self.assertTrue(manual_nfa.run_on_word("kotO"))
		self.assertFalse(manual_nfa.run_on_word("koto"))
		

		rep_end = manual_nfa.create_repetition_matcher_experimental(range(2, 3), manual_nfa.create_word_matcher, "cat", [any_end])
		manual_nfa.accept.add(rep_end[0])

		self.assertTrue(manual_nfa.run_on_word("kotVcatcat"))
		self.assertFalse(manual_nfa.run_on_word("kotVcat"))
		self.assertTrue(manual_nfa.run_on_word("kotV"))

		rep_ends = manual_nfa.create_repetition_matcher_experimental(range(2, 5), manual_nfa.create_any_matcher, string.ascii_uppercase, rep_end)
		for state in rep_ends:
			manual_nfa.accept.add(state)

		self.assertTrue(manual_nfa.run_on_word("kotVcatcatVVVV"))

		

if __name__ == '__main__':
	unittest.main()