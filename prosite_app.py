#!/bin/env python3
# Prosite regular expressions matcher
# Copyright (c) 2014 Tomasz Truszkowski
# All rights reserved.

import prosite_matcher

if __name__ == '__main__':

	print("\n Hi, this is Prosite Matcher! \n")

	sequence = input("Sequence: ")
	regex = input("Regular expression: ")

	prositeMatcher = prosite_matcher.PrositeMatcher()
	prositeMatcher.compile(regex)
	matches, ranges = prositeMatcher.get_matches(sequence)

	print(matches, ranges)

	print("Found patterns: ", end="")

	if (len(matches) > 0):

		print(sequence[ 0 : ranges[0][0] ], end="")

		for i in range(0, len(matches)):

			print("\033[91m", end="")
			print(sequence[ ranges[i][0] : ranges[i][1] ], end="")
			print("\033[0m", end="")

			if (i < len(matches) - 1):
				print(sequence[ ranges[i][1] : ranges[i + 1][0] ], end="")

		print(sequence[ ranges[len(ranges) - 1][1] : len(sequence)])

	else:

		print(sequence)

	print("")
