# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    # Convert all letters in word to lowercase
    word = word.lower()
    # INITIALIZE total_points VARIABLE TO 0
    total_points = 0
    # LOOP through all letters in word
    for letter in word:
        # ADD value of letter TO total_points IF wildcard return 0
        total_points += SCRABBLE_LETTER_VALUES.get(letter, 0)
    # INITIALIZE word_len VARIABLE TO word length
    word_len = len(word)
    # Compute value for second component
    calculated_value = 7*word_len - 3*(n - word_len)
    # Compute word_score
    word_score = total_points * max(calculated_value, 1)
    # RETURN word_score
    return word_score


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    # Reduce num_vowels by 1 to replace one vowel with wildcard
    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    # Add one wildcard "*" to hand
    hand["*"] = 1
    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """

    # Convert all letters to lowercase
    word = word.lower()
    # CREATE copy of hand
    hand_copy = hand.copy()
    # LOOP through all letters of word
    for letter in word:
        # IF letter IN hand_copy AND letter count is greater than 0
        if letter in hand_copy and hand_copy[letter] > 0:
            # THEN subtract 1 FROM letter count in hand_copy
            hand_copy[letter] -= 1
    # RETURN updated copy of hand
    return hand_copy


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    # Define helper function compose_word
    def compose_word(hand, frequency):
        # LOOP through all letters in word to see if word can be composed of
        # letters in the hand
        for letter, freq in frequency.items():
            # IF letter not in hand OR freq > count in hand[letter]
            if letter not in hand or freq > hand[letter]:
                # THEN the word can't be composed with the letters in the hand
                return False
        # RETURN True as word can be composed with letters in hand
        return True

    # Convert all letters to lowercase
    word = word.lower()
    # Get individual letter frequency in word
    frequency = get_frequency_dict(word)
    # Initialize valid_word to False
    valid_word = False

    # IF word can be composed with letters in the hand
    if compose_word(hand, frequency):
        # IF wildcard in word
        if "*" in word:
            # THEN test if wildcard can be replaced by a vowel
            # to form a valid word from word_list
            # LOOP through all vowels in VOWELS
            for vowel in VOWELS:
                wildcard = word.replace("*", vowel)
                if wildcard in word_list:
                    valid_word = True
        # ELSE word only contains alphabetic letters
        elif word in word_list:
            valid_word = True
    return valid_word


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    # RETURN sum of count of all letters in hand
    return sum(hand.values())


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """

    # Keep track of the total score
    total_score = 0
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        # Display the hand
        print("Current hand: ", end="")
        display_hand(hand)
        # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished: ')
        # If the input is two exclamation points:
        if word == "!!":
            # End the game (break out of the loop)
            break
        # Otherwise (the input is not two exclamation points):
        # If the word is valid:
        elif is_valid_word(word, hand, word_list):
            # Tell the user how many points the word earned,
            # and the updated total score
            word_score = get_word_score(word, calculate_handlen(hand))
            total_score += word_score
            print('"{}" earned {} points.'.format(word, word_score), end=" ")
            print('Total: {} points'.format(total_score))
        # Otherwise (the word is not valid):
        else:
            # Reject invalid word (print a message)
            print("That is not a valid word. Please choose another word.")
        # update the user's hand by removing the letters of their entered word
        hand = update_hand(hand, word)
        print()
    # IF player ran out of letters
    if calculate_handlen(hand) == 0:
        # THEN print message accordingly
        print("Ran out of letters")
    # Return the total score as result of function
    return total_score


#
# Problem #6: Playing a game
#


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    # Create copy of current hand
    sub_hand = hand.copy()
    if letter in hand:
        # Pick random letter FROM all ascii lowercase letters
        sub_letter = random.choice(string.ascii_lowercase)
        # WHILE randomly chosen letter IN hand
        while sub_letter in hand:
            # DO SELECT another random letter
            sub_letter = random.choice(string.ascii_lowercase)
        # GET value of letter
        let_val = sub_hand[letter]
        # Remove letter from hand
        del sub_hand[letter]
        # Add substituted letter to hand with same amount as previous letter
        sub_hand[sub_letter] = let_val
    # RETURN sub_hand
    return sub_hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    # INITIALIZE total_game_score score to 0, substitute_letter and
    # replayed_hand to False
    total_game_score = 0
    substitute_letter = False
    replayed_hand = False

    # GET number of hands from user
    hands = int(input("Enter total number of hands: "))
    # WHILE player has hands left to play
    while hands > 0:
        # DO play hand
        # INITIALIZE total_score for current hand to 0
        total_score = 0
        # GET hand of size HAND_SIZE
        hand = deal_hand(HAND_SIZE)

        # Player can substitute one letter per game
        if not substitute_letter:
            print("Current hand: ", end="")
            display_hand(hand)
            # GET user input if player wants to substitute a letter
            user_input = input("Would you like to substitute a letter? ")
            # IF player wants to substitute a letter
            if user_input.lower()[0] == "y":
                # THEN GET letter from user input
                letter = input("Which letter would you like to replace: ")
                # Update hand with substituted letter
                hand = substitute_hand(hand, letter)
                substitute_letter = True
            print()

        # SET total_score TO score of current game of hand
        total_score = play_hand(hand, word_list)
        print("Total score for this hand:", total_score)
        print("----------")

        # Player can replay one hand per game
        if not replayed_hand:
            # Ask user if he wants to replay his hand
            user_input = input("Would you like to replay the hand? ")
            # IF user doesn't want to replay his hand
            if user_input.lower()[0] == "y":
                # THEN replay the current hand
                replay_score = play_hand(hand, word_list)
                print("Total score for this hand:", total_score)
                print("----------")

                replayed_hand = True
                # Keep the better score of both runs
                total_score = max(total_score, replay_score)
        # Decrement hands by 1
        hands -= 1
        # ADD total_score TO total_game_score
        total_game_score += total_score
    print("Total score over all hands: {} points".format(total_game_score))


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
