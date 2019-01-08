'''
Purpose:    The aim of this simulation is to analyze the probabilities of
            different combinations in a random draw for big 2.

Author:          Kevin Ta
Date Created:    2018 December 29th
'''

###########################################
#               Libraries
###########################################

import numpy as np

###########################################
#               Constants
###########################################

SUITS = {'Spades': 0, 'Hearts': 1, 'Clubs': 2, 'Diamonds': 3}
attempts = 2500

###########################################
#               Classes
###########################################

class clCard:
    """
    Class for a single card in Big 2
    """

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

class clHand:
    """
    Class for a 13-card hand in Big 2
    """

    def __init__(self, hand):
        self.hand = hand
        self.numberCount = np.zeros(13)
        self.suitCount = np.zeros(4)

        for card in self.hand:
            self.numberCount[card[0] - 1] += 1
            self.suitCount[SUITS[card[1]] - 1] += 1

    def fnCountMultiples(self):
        """
        Counts number of each card number and stores number of doubles, triples, and quadruples as class variable
        """

        multipleNumberCount = self.numberCount

        self.quadruples = np.zeros(13)
        self.triples = np.zeros(13)
        self.doubles = np.zeros(13)

        self.quadruples = multipleNumberCount // 4
        multipleNumberCount = multipleNumberCount - self.quadruples * 4
        self.triples = multipleNumberCount // 3
        multipleNumberCount = multipleNumberCount - self.triples * 3
        self.doubles = multipleNumberCount // 2

    def fnCountFlushes(self):
        """
        Counts number of each suit and stores number of flushes as class variable
        """

        self.suits = np.zeros(4)
        self.suits = self.suitCount // 5

    def fnCountStraights(self):
        """
        Counts number of straights and stores as class variable
        """
        self.straights = 0
        straightNumberCount = self.numberCount

        if not np.all(straightNumberCount):

            zeroIndex = np.where(straightNumberCount == 0)[0]
            straightLength = np.array(fnFindStraightLength(zeroIndex))

            while np.any(straightLength >= 5):

                straightArray = np.zeros(13)
                if straightLength[0] > 5:
                    if straightLength[-1] > 5:
                        straightArray[0:5] = np.ones(5)
                        print ("Difficult to compute.")
                    else:
                        straightArray[0:5] = np.ones(5)
                else:
                    firstZeroIndex = np.argmax(straightLength > 5)
                    if firstZeroIndex >= 8:
                        straightArray[zeroIndex[firstZeroIndex - 1] + 1:zeroIndex[-1]] = np.ones(5)
                    else:
                        straightArray[zeroIndex[firstZeroIndex - 1] + 1:zeroIndex[firstZeroIndex - 1] + 6] = np.ones(5)
                self.straights += 1

                straightNumberCount = np.subtract(straightNumberCount, straightArray)

                zeroIndex = np.where(straightNumberCount == 0)[0]
                straightLength = np.array(fnFindStraightLength(zeroIndex))

        else:
            self.straights += 2

class clDeck:
    """
    Class for a 52-card deck in Big 2
    """

    def __init__(self, suits, numbers):
        self.cards = [[(i,j) for i in numbers] for j in suits]

    def fnShuffle(self):
        """
        Shuffles card order in deck to simulate random dealing of cards
        """

        deckArray = self.cards[0] + self.cards[1] + self.cards[2] + self.cards[3]
        np.random.shuffle(deckArray)
        self.cards = [deckArray[0:13], deckArray[13:26], deckArray[26:39], deckArray[39:52]]
        
###########################################
#               Functions
###########################################

def fnFindStraightLength(zeroIndex):
    """
    Finds the length of each consecutive set of numbers and returns each length in an array
    """

    straightRunLength = []

    for zind in range(len(zeroIndex)):
        if zind == 0:
            straightRunLength.append(zeroIndex[zind])
        else:
            straightRunLength.append(zeroIndex[zind] - zeroIndex[zind - 1] - 1)
    if zeroIndex[0]:
        straightRunLength.append(13 - zeroIndex[-1])
    else:
        straightRunLength.append(12 - zeroIndex[-1])
    return straightRunLength

###########################################
#               Main
###########################################

if __name__ == '__main__':
    
    deck = clDeck(SUITS, range(1,14))
    doubles = 0
    triples = 0
    quadruples = 0
    flushes = 0
    fullHouses = 0
    straights = 0

    for i in range(attempts):

        deck.fnShuffle()
        
        for j in range(4):
            playerHand = clHand(deck.cards[j])

            playerHand.fnCountMultiples()

            quadruples += sum(playerHand.quadruples)
            triples += sum(playerHand.triples)
            doubles += sum(playerHand.doubles)
            fullHouses += min(sum(playerHand.doubles), sum(playerHand.triples))

            playerHand.fnCountFlushes()
            flushes += sum(playerHand.suits)

            # playerHand.fnCountStraights()
            # straights += playerHand.straights

            print("Number of hands analyzed: {0:.0f}/{1:.0f}".format(i * 4 + j, attempts * 4))

    print("Hands Analyzed: {}".format(attempts * 4))
    print("Doubles: {0:.0f}".format(doubles))
    print("Triples: {0:.0f}".format(triples))
    print("Quadruples: {0:.0f}".format(quadruples))
    print("Full Houses: {0:.0f}".format(fullHouses))
    print("Flushes: {0:.0f}".format(flushes))
    # print("Straights: {0:.0f}".format(straights))

    input()

    pass