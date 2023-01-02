# Nerdle Solver

# Author: Ryan Kuhn
# Creation Date: 6/1/2020
#
# Background: Nerdle is a variation of the popular game, Wordle, which gives 6 guesses to identify the day's word
# For each guess, the game will tell you if each letter is not in the word at all, in the correct place, or is
# in the word but in the correct place.
# Nerdle is the same concept but instead of words, it asks to solve equations
# This solution iteratively provides a suggestion for the user to submit into the nerdlegame.com website
# The user then inputs the feedback from the website about which characters are correct


import collections
import pandas as pd
import numpy as np
import itertools

# All options for integers
int_opts = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
# All operator options
operation_opts = ["+", "-", "/", "*", "="]


input_test = ['2', '1', "+", '3', '6', "=", '5', '6']
invalid_input1 = ["=", 1, "+", 3, 6, "=", 5, 6]
invalid_input2 = [1, 1, "+", "/", 6, "=", 5, 6]



def LR_equivalent(input):
    # Find the index of the = sign
    eq_index = input.index("=")
    # Find the characters on the left of the =
    left = input[0:eq_index]
    # Find the characters on the right of the =
    right = input[eq_index+1:]
    # Convert to strings
    left_str = "".join(left)
    right_str = "".join(right)

    # # Check if integers have a leading zero
    # all_ints = set()
    # no_left_op = True
    # no_right_op = True
    # for op in operation_opts:
    #     if op in left_str:
    #         all_ints.update(set(left_str.split(op)))
    #         no_left_op = False
    #     if op in right_str:
    #         all_ints.update(set(right_str.split(op)))
    #         no_right_op = False
    # if no_left_op:
    #     all_ints.update(left_str)
    # if no_right_op:
    #     all_ints.update(right_str)
    #
    # all_ints = list(all_ints)
    # for string in all_ints:
    #     if string[0] == '0':
    #         return False
    #     else:
    #         continue

    #Evaluate the left and right side of the equation. Ensure that they are equal
    try:
        if eval(left_str) != eval(right_str):
            return False
        else:
            return True
    except:
        return False


# Function to check if the input list does not have operators which are directly adjacent
# This would be an invalid equation
def nonadjacent_operands(input):
    # Check to make sure an operand or = is not at the beginning or end
    if input[0] in operation_opts or input[0] == "=":
        return False
    if input[-1] in operation_opts or input[-1] == "=":
        return False

    # Check that theres only 1 =
    if input.count("=") != 1:
        return False

    # Checks if the operators are next to eachother. If so, returns False
    for i in range(1,len(input)-2):
        if input[i] in operation_opts:
            if input[i+1] in operation_opts:
                return False
            else:
                continue
        else:
            continue
    # Return True
    return True

# Purple characters are those which are in the equation but are not in the correct location
purple = []
# Define an empty set which containes the indices in the  equation which are correctly identified
known_indices = set()
# Define the length of the equation
num_characters = 8
# Set of all of the possible characters
all_set = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "+", "-", "/", "*", "="}
# Set of all the operators
op_set = {"+", "-", "/", "*", "="}
# Create an array which denotes all options for each index in the equation.
all_opts = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "+", "-", "/", "*", "="] for x in range(8)]


# Main function to iterate through user input
def get_feedback():
    # invalid variable indicates if
    invalid = True
    # Iterate through each guess until solved
    while invalid:
        # feedback is the user input about correct/incorrect characters
        feedback = input("Type 'yay' if solved.\n Otherwise what is correct? (Comma separated -1:DNE, 0:Wrong loc, 1:Right loc) EX: -1,0,1,0... ")
        # Exit if solved
        if feedback == 'yay':
            print('Game Won!!')
            exit()
        # Uncomment for backdoor option for testing with default inputs
        #elif feedback == 'x':
        #    feedback = '1,-1,-1,-1,0,1,1,-1'

        # Split the input by , into array
        fb_split = feedback.split(',')
        # If the length of input is incorrect, loop again and request input
        if len(fb_split) != num_characters:
            invalid = True
            continue
        # If the number of right and wrong locations is <1 loop again
        if fb_split.count("0") + fb_split.count("1") < 1:
            invalid = True
            continue
        invalid = False

    return fb_split


def check_guess(guess):
    # Get user feedback
    fb_split = get_feedback()

    guess_freq = collections.Counter(guess)
    # The values that were guessed multiple times
    mult_guess_vals = [k for (k,v) in guess_freq.items() if v > 1]


    for i in range(len(fb_split)):
        # Only guessed this val once
        # Gray - val may be at other guess locations, but not anywhere else
         # If this val guess was gray and this guess was guessed multiple times
        if fb_split[i] == '-1' and guess[i] in mult_guess_vals:
            guess_indices = [j for j, x in enumerate(guess) if x == guess[i]]
            guess_indices.remove(i) # Remove this guess index from this list
            fb_guess = [x for j, x in enumerate(fb_split) if j in guess_indices]

            # If theres ONLY Gray and Green, remove this guess from all guesses except those green
            if '0' not in fb_guess:
                gray_loc = [j for j, x in enumerate(fb_split) if x == '-1'] # Get all the indices of all the gray
                for loc in gray_loc:
                    if loc in guess_indices:
                        # Remove all the gray indices from the list,
                        guess_indices.remove(loc)
                remove_from_opts(guess[i], 'gray', guess_indices)

            # If theres ONLY Gray and Purple, Only remove from gray locations
            elif '1' not in fb_guess:
                # gray_loc = [j for j, x in enumerate(fb_split) if x == '-1']
                # for loc in gray_loc:
                #     remove_from_opts(guess[i], 'purple', loc)
                remove_from_opts(guess[i], 'purple', i)

            # If ALL other guesses were Gray
            elif '1' not in fb_guess and '0' not in fb_guess:
                remove_from_opts(guess[i], 'gray', 'all')

        # Gray - val not in equation at all. Only One Guess
        elif fb_split[i] == '-1' and guess[i] not in mult_guess_vals:
            remove_from_opts(guess[i], 'gray', 'all')
        # Purple - val in equation but wrong spot
        elif fb_split[i] == '0':
            remove_from_opts(guess[i], 'purple', i)
            purple.append((guess[i]))
        # Green - val is in the right place
        elif fb_split[i] == '1':
            remove_from_opts(guess[i], 'green', i)
            known_indices.update([i])




def remove_from_opts(opt_2_rem, cat, index):
    # Removes this value from all possible positions except where it is also guessed
    if cat == 'gray' and type(index) == list:
        # Iterate through values in list
        for val_list_index in range(len(all_opts)):
            # If this position was part of the multiple guess, don't remove it
            if val_list_index in index:
                # Don't remove anything
                continue
            # If this position is either this guess or not one of the repeat guesses, then remove it
            else:
                if opt_2_rem in all_opts[val_list_index]:
                    all_opts[val_list_index].remove(opt_2_rem)
        return

    # Removes this value from all possible positions
    if cat == 'gray' and index == 'all':
        for val_list in all_opts:
            if opt_2_rem in val_list:
                val_list.remove(opt_2_rem)
        return

    # Removes everything but the opt_2_rem since this is the correct pos
    if cat == 'green' and type(index) == int and index >= 0 and index < 8:
        all_opts[index] = [opt_2_rem]
        if opt_2_rem == "=":
            remove_from_opts(opt_2_rem, 'gray', [index])
        return
    # Removes value from this specific position
    elif cat == 'purple' and type(index) == int and index >= 0 and index < 8:
        if opt_2_rem in all_opts[index]:
            all_opts[index].remove(opt_2_rem)
        return


# Just 1
    # right pos -> remove all from that row, don't touch others
    # wrong pos -> remove from just that row
    # DNE -> remove from all (unless more than 1 guessed, then go below)
# Two
    # Green, green - Standard
    # Purple, Purple - standard
    # DNE, DNE - all delete
    # Green, Purple
    # Green, DNE - Green stay, all other DNE
    # Purple, DNE - Purple applies, only this guess DNE



def create_guess():
    # Try new method for creating all possible, eliminate options of multiple operators beforehand
    # call function for next_letter()
    # require 1 and only 1 =
    # Don't allow 0 after operator or as first val
    # Within for loop, create deep copy of all_opts, remove options from each position as you create it
    all_possible = []
    num_combos = 1
    for i in range(len(all_opts)):
        num_combos = num_combos * len(all_opts[i])

    print(str(num_combos) + " Total combinations")

    def recursion_plz(all_opts, pos, option):
        if pos == 0:
            option = []

        for i in range(len(all_opts[pos])):
            option = option[0:pos]
            letter = all_opts[pos][i]
            # Return if there is no =
            if pos > 6 and '=' not in option:
                return
            if pos > 0:  # Ensures we don't access out of bounds index
                # Make sure we don't have adjacent operators
                if letter in operation_opts:  # If letter is an operator
                    if option[pos - 1] in operation_opts:  # if previous position in option was also an operator
                        return
                    # Can't have two =
                    elif letter == '=' and '=' in option:
                        return
                    # Don't allow operators on right side of = (Could consolidate into 1 rule)
                    elif '=' in option:
                        return
                # Make sure we don't have leading zeros or lone zeros
                if len(set(option).intersection(op_set)) >= 1:  # If there is at least 1 operator in option already
                    # There is an operator in the option already
                    # Returns the index of the last operator
                    last_operator_ind = max([ind for ind, v in enumerate(option) if v in set(option).intersection(op_set)])
                    # If there is a leading 0, return without appending to all_possible
                    if last_operator_ind+1 < pos and option[last_operator_ind + 1] == '0':
                        return
            # Return if 4 numbers in a row
            if pos >= 3 and letter in int_opts and set(option).issubset(int_opts):
                continue


            option = option + [letter]

            if pos >= 7:
                all_possible.append(option)
            elif pos < 7:
                recursion_plz(all_opts, pos + 1, option)
        if pos >= 7:
            return

    options = []
    recursion_plz(all_opts, 0, options)

    #all_possible = list(itertools.product(*all_opts))


    if len(all_possible) == 0:
        print("You can't do that! That's impossible!")
        exit()

    del_list = [0 for i in range(len(all_possible))]
    # TIME DRAINER
    all_possible[:] = [lst for lst in all_possible if nonadjacent_operands(lst) and LR_equivalent(lst)]

    if len(all_possible) == 0:
        print("You can't do that! That's impossible!")
        exit()


    rank_poss_list = [0 for i in range(len(all_possible))]
    optimal = []
    unguessed = all_set.difference(guessed_set)
    all_indices = {0, 1, 2, 3, 4, 5, 6, 7}
    purple_freq = collections.Counter(purple)
    # Step through all possible solutions to rank them
    for i in range(len(all_possible)):
        guess = all_possible[i]
        # Indices of the unknown positions
        unknown_ind = all_indices.difference(known_indices)
        temp_purple = set([x for x in purple])
        # iterate through all unknown positions
        for position in list(unknown_ind):
            # The letter at this position in the new guess
            letter = all_possible[i][position]
            # !!!! Need to force option to include >= purple freq
            if letter in temp_purple:
                # Removes letter from set of temp_purple so that you don't double count letters that show up 2x+
                temp_purple.remove(letter)
                # If the guess contains the same number of a value as there were purples for that value
                if purple_freq[letter] == all_possible[i].count(letter):
                    rank_poss_list[i] += 50

                # If guess has more of the purple letter, still give some value
                elif purple_freq[letter] < all_possible[i].count(letter):
                    rank_poss_list[i] += 25
                # If guess has fewer purple letters, disqualify
                elif purple_freq[letter] > all_possible[i].count(letter):
                    rank_poss_list[i] = np.nan
                    break

            else:
                continue
        # Add weight for words with no / or *
        if all_possible[i].count('/') == 0 or all_possible[i].count('*') == 0:
            rank_poss_list[i] += 10
        # Add weight for guess which contains unguessed letters
        set_in_guess = set(all_possible[i])
        rank_poss_list[i] += len(set_in_guess.intersection(unguessed)) * 5

    possible_count = len([x for x in rank_poss_list if x != np.nan])
    print(str(possible_count) + " Total POSSIBLE Combinations")
    max_rank_i = rank_poss_list.index(np.nanmax(rank_poss_list))
    next_guess = all_possible[max_rank_i]
    purple.clear()

    return next_guess



# Removes operations from first and last slot
for op in operation_opts:
    remove_from_opts(op, 'gray', [1,2,3,4,5,6])
# Frome 0 from initial position
remove_from_opts('0', 'purple', 0)

guessed_set = set()
solved = False
# Default initial guess
print("First Guess: ")
next_guess = ['2', '1', '+', '3', '6', '=', '5', '7']
guessed_set.update(next_guess)
print(next_guess)

# Continue while it is not solved
while solved == False:
    check_guess(next_guess)
    df = pd.DataFrame(all_opts).T
    print(df)
    print("Creating next guess...")
    next_guess = create_guess()
    guessed_set.update(next_guess)
    print(next_guess)


