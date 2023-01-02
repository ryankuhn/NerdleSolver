# NerdleSolver
Solver for the game Nerdle which is an equation version of Wordle

# Author: Ryan Kuhn
# Creation Date: 6/1/2020
#
# Background: Nerdle is a variation of the popular game, Wordle, which gives 6 guesses to identify the day's word
# For each guess, the game will tell you if each letter is not in the word at all, in the correct place, or is
# in the word but in the correct place.
# Nerdle is the same concept but instead of words, it asks to solve equations
# This solution iteratively provides a suggestion for the user to submit into the nerdlegame.com website
# The user then inputs the feedback from the website about which characters are correct

# User inputs comma separated string (-1:DNE, 0:Wrong loc, 1:Right loc) 
# EX: 8 character equation would be -1,0,1,0,1,1,-1,0
# This means the first and seventh characters do not appear in the equation
# The second, forth, and last characters are in the wrong place
# And the third, fifth, and sixth characters are in the correct possition
