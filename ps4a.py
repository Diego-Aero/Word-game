# The 6.00 Word Game

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 10

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList

def getFrequencyDict(sequence):
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
        #Coge el valor en el diccionario asociado a x (por si acaso, si no hay ninguno, devuelve 0)
        #Si no encuentra (es inicial) da un valor de 0 + 1 y luego al buscarlo sera 1 + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.
    Puede que word sea un espacio vacío

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    score=0
    for i in word:
        score+=SCRABBLE_LETTER_VALUES[i]
        #Accede al valor de la letra, que ya está tabulado
    if len(word)==n:
        score=score*len(word)+50
    else:
        score*=len(word)
    return score



#
# Problem #2: Make sure you understand how this function works and what it does!
#
def displayHand(hand):
    """
    Displays the letters currently in the hand.
    Muestra las letras del diccionario mano teniendo en cuenta el número de veces
    que aparece cada una en él

    For example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter,end=" ")       # print all on the same line

#
# Problem #2: Make sure you understand how this function works and what it does!
#
def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n // 3 #redondeo por abajo
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        #Si es la primera da un valor de 0 + 1 y luego al buscarlo sera 1 + 1
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    handNew=hand.copy()
    #Los diccionarios son objetos mutables, no queremos que cambie hand original salvo que digamos hand = updateHand(hand, word)
    for i in word:
        if i in handNew.keys():
            handNew[i]-=1
    return handNew



#
# Problem #3: Test word validity
#
def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    handNew=hand.copy()
    
    if word not in wordList:
        #Esto incluye el caso de que word esté vacío
        return False
    
    for c in word:
        if c in handNew.keys():
            #CComprobar que la letra esté en la mano
            handNew[c]-=1
            if handNew[c]<0:
                #Comprobar que no se usen más letras de las que hay en la mano
                #Se podría contar también con string.count() y así no necesitaríamos una copia de hand
                return False
        else:
            return False
    
    return True

    """
    if word not in wordList:
        return False

    hand2 = hand.copy()
    for x in word:
        if hand2.get(x,0) > 0:
            hand2[x] -= 1
        else:
            return False
    return True
    """
    
    #Se puede hacer utilizando la funcion getFrequencyDict dada
    """
    if word not in wordList:
        return False
    
    wordDict = getFrequencyDict(word)
    
    for k in wordDict:
        if wordDict[k] > hand.get(k, 0):
            #Comprobamos que no hayamos utilizado mas cantidad de cada letra de las que hay en hand
            return False
    return True
    """


#
# Problem #4: Playing a hand
#

def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    """
    for c in hand.keys():
        count+=hand.get(c, 0)
    return count
    """
    return sum(hand.values())



def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
    # Keep track of the total score
    pointsTotal=0
    band=True
    # As long as there are still letters left in the hand:
    #while any(hand.values()):
    while calculateHandlen(hand)>0:
        # Display the hand
        print('Current Hand: ', end='')
        displayHand(hand)
        # Ask user for input
        word=input('Enter word, or a "." to indicate that you are finished: ')
        # If the input is a single period:
        if word=='.':
            # End the game (break out of the loop)
            band=False
            break      
        # Otherwise (the input is not a single period):
        else:
            # If the word is not valid:
            if not isValidWord(word, hand, wordList):
                # Reject invalid word (print a message followed by a blank line)
                print('Invalid word, please try again.')
            # Otherwise (the word is valid):
            else:
                # Tell the user how many points the word earned, and the updated total score, in one line followed by a blank line
                points=getWordScore(word, n)
                pointsTotal+=points
                print(word+' earned '+str(points)+' points. Total: '+str(pointsTotal))
                # Update the hand 
                hand=updateHand(hand, word)
        print()
                

    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    if not band:
        print('Goodbye! Total score: '+str(pointsTotal)+' points.')
    else:
        print('Run out of letters. Total score: '+str(pointsTotal)+' points.')


#
# Problem #5: Playing a game
# 

def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1    
    """
    while True:
        choice = input('Enter n for a new hand, r to replay, e to end: ')
        if choice == 'n':
            hand = dealHand(HAND_SIZE)
        elif choice == 'e':
            break
        elif choice != 'r':
            print('Invalid command.')
            continue
        try:
            playHand(hand, wordList, HAND_SIZE)
        except NameError:
            print('You have not played yet. Please play a new hand first!\n')

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)
