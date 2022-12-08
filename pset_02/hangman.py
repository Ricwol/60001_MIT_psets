# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ""
    for letter in secret_word:
        if letter in letters_guessed:
            guessed_word += letter
        else:
            # Current letter not guessed yet -> set to blank '_ '
            guessed_word += "_ "
    return guessed_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ""

    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available_letters += letter
    return available_letters


# -----------------------------------
# My helper functions

def get_guess():
    """
    Collects and returns valid user input, empty string ("") otherwise.

    Valid user input is a lowercase alphabet letter. All non-alphabet
    characters are invalid user input.

    Returns
    -------
    str
        single lowercase alphabet letter, if input is valid, empty string
        otherwise.

    """
    guess = input("Please guess a letter: ")
    guess = guess.lower()

    return guess if guess.isalpha() else ""


def update_stats(guesses, warnings):
    """
    Subtract one warnings and return updated values.

    As long as there are warnings left, subtract one warnings, subtract one
    guesses otherwise

    Parameters
    ----------
    guesses : int
        number of tries left.
    warnings : int
        number of warnings left.

    Returns
    -------
    int
        updated guesses value >= 0.
    int
        updated warnings value >= -1.

    """
    # IF player has warnings left
    if warnings > 0:
        # THEN reduce warnings by 1
        warnings -= 1
        warn_resp = f"You have {warnings} warnings left:"
    # ELSE IF no warnings left
    else:
        # THEN reduce guesses by 1
        guesses -= 1
        warn_resp = "You have no warnings left so you lose one guess:"
    return guesses, warnings, warn_resp


def check_guess(guess, secret_word, letters_guessed, guesses, warnings):
    """
    Check if guess is in secret_word and return updated guesses and warnings.

    If user enters a valid character that is not in secret_word, subtract one
    guess if character is a consonant, two if a vowel.
    Invalid guesses or previously asked guesses result in subtracting one from
    warnings. If no warnings left, player loses one try, i.e. subtract one
    from guesses.

    Parameters
    ----------
    guess : str
        empty string or one lowercase alphabet character.
    secret_word : str
        lowercase secret word.
    letters_guessed : list
        list of all valid guesses user already tried.
    guesses : int
        a positive number of guesses left.
    warnings : int
        number of warnings left.

    Returns
    -------
    guesses : int
        updated number of guesses according to user input.
    warnings : int
        updated number of guesses according to user input.

    """
    response = "Good guess:"
    # IF guess is invalid
    if guess == "":
        guesses, warnings, warn_resp = update_stats(guesses, warnings)
        response = f"Oops! That is not a valid letter. {warn_resp}"
    # ELSE IF guess was already used
    elif guess in letters_guessed:
        guesses, warnings, warn_resp = update_stats(guesses, warnings)
        response = f"Oops! You've already guessed that letter. {warn_resp}"
    # ELSE IF guess is valid but not in secret_word
    elif guess not in secret_word:
        # IF guess is a vowel
        if guess in "aeiou":
            # THEN reduce guesses by 2
            guesses -= 1
        # ELSE guess is a consonant
        # THEN reduce guesses by 1
        guesses -= 1
        letters_guessed.append(guess)
        response = "Oops! That letter is not in my word:"
    # ELSE guess is in secret_word
    else:
        # THEN add guess to letters_guessed
        letters_guessed.append(guess)

    # Print current status of guessed secret_word
    print(f"{response} {get_guessed_word(secret_word, letters_guessed)}")
    return guesses, warnings


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
  
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    # Initialize guesses=6, warnings=3 and letters_guessed to an empty list
    guesses = 6
    warnings = 3
    letters_guessed = []

    # PRINT Start screen to welcome the player
    print("Welcome to the game Hangman!")
    # PRINT length of the secret word and how many warnings player starts with
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warnings} warnings left")
    print("-------------")

    # WHILE player has guesses left and not has guessed the word correclty
    while guesses > 0 and not is_word_guessed(secret_word, letters_guessed):
        # PRINT how many guesses are left
        print(f"You have {guesses} guesses left")
        # PRINT which letters are still available
        print(f"Available Letters: {get_available_letters(letters_guessed)}")

        # GET input from user; assume that only one letter is entered
        guess = get_guess()

        # Check guess and update guesses and warnings accordingly
        guesses, warnings = check_guess(guess, secret_word, letters_guessed,
                                        guesses, warnings)
        print("-------------")

    # PRINT End screen
    # IF game was won
    if guesses > 0:
        # Remove duplicates by casting secret_word to set
        unique_letter = set(secret_word)
        # Calculate total score
        # based on unique letters in secret_word and guesses left
        total_score = guesses * len(unique_letter)

        # THEN print total score
        print("Congratulations, you won!")
        print(f"Your total score for this game is: {total_score}")
    # ELSE print secret_word
    else:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # Initialize guesses=6, warnings=3 and letters_guessed to an empty list
    # Initialize guesses=6, warnings=3 and letters_guessed to an empty list
    guesses = 6
    warnings = 3
    letters_guessed = []

    # PRINT Start screen to welcome the player
    print("Welcome to the game Hangman!")
    # PRINT length of the secret word and how many warnings player starts with
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warnings} warnings left")
    print("-------------")

    # WHILE player has guesses left and not has guessed the word correclty
    while guesses > 0 and not is_word_guessed(secret_word, letters_guessed):
        # PRINT how many guesses are left
        print(f"You have {guesses} guesses left")
        # PRINT which letters are still available
        print(f"Available Letters: {get_available_letters(letters_guessed)}")

        # GET input from user; assume that only one letter is entered
        guess = get_guess()

        # IF guess is invalid
            # THEN reduce warnings by 1
            # IF no warnings left
                # THEN reduce guesses by 1
        # ELSE IF guess is "*"
            # THEN print out all words in wordlist that matches the current guessed word. 
        # ELSE IF guess was already used
            # THEN reduce warnings by 1
            # IF no warnings left
                # THEN reduce guesses by 1
        # ELSE IF guess is valid but not in secret_word
            # IF guess is a vowel
                # THEN reduce guesses by 2
            # ELSE guess is a consonant
                # THEN reduce guesses by 1
        # ELSE guess is in secret_word
            # THEN add guess to letters_guessed
        print("-------------")
        break

    # PRINT End screen
    # IF game was won
    if guesses > 0:
        # Remove duplicates by casting secret_word to set
        unique_letter = set(secret_word)
        # Calculate total score
        # based on unique letters in secret_word and guesses left
        total_score = guesses * len(unique_letter)

        # THEN print total score
        print("Congratulations, you won!")
        print(f"Your total score for this game is: {total_score}")
    # ELSE print secret_word
    else:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
