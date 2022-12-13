# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    # Base case
    # A sequence with only 1 character.
    if len(sequence) == 1:
        return [sequence]

    # Recursive case
    # Any sequence longer than one character
    permutations = []
    # LOOP through all letters in sequence
    for i, letter in enumerate(sequence):
        # Get substring without current letter
        sub = sequence[:i] + sequence[i+1:]
        # CHECK all permutations for sub sequence without current letter
        for permutation in get_permutations(sub):
            # Append current letter to all permutations of substring
            permutations.append(letter + permutation)
    # RETURN all permutations
    return permutations

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    # Test cases
    print("TESTING No recursive call")
    # Empty string
    example_input = ""
    expected_output = []
    print('Input: "{}"'.format(example_input))
    print('Expected Output:', expected_output)
    print('Actual Output:', get_permutations(example_input))
    print()

    # String with only one letter
    example_input = 'a'
    expected_output = ['a']
    print('Input: "{}"'.format(example_input))
    print('Expected Output:', expected_output)
    print('Actual Output:', get_permutations(example_input))
    print("-"*70)

    print("TESTING Exactly one recursive call")
    # String with two unique letter
    example_input = 'ab'
    expected_output = ['ab', 'ba']
    print('Input: "{}"'.format(example_input))
    print('Expected Output:', expected_output)
    print('Actual Output:', get_permutations(example_input))
    print("-"*70)

    print("TESTING Two or more recursive calls")
    # String with three unique character
    example_input = '012'
    expected_output = ['012', '021', '102', '120', '201', '210']
    print('Input: "{}"'.format(example_input))
    print('Expected Output:', expected_output)
    print('Actual Output:', get_permutations(example_input))
