import random, itertools

SUITS = {0 : "Heart", 1 : "Club", 2 : "Diamond", 3 : "Spade"}
RANKS = {0 : 'Ace', 9 : 'Jack', 10 : 'Queen', 11 : 'King' }

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self,card2):
        return ( (self.suit == card2.suit) and (self.rank == card2.rank))

    def __str__(self):
        return "< CARD : Suit:{0}, Rank:{1} >".format(self.suit, self.rank)

class Deck:


    def __init__(self,numOfDecks=1):
        self.deck = []
        for i in range(numOfDecks):
            for x in range(4):
                for y in range(13):
                    self.deck.append( Card(x, y))
        random.shuffle(self.deck)

    def getCard(self, index):
        return self.deck[index]

    def cardCount(self):
        return len(self.deck)

    def findCard(self,card):
        index = [i for i,x in enumerate(self.deck) if x == card]
        numCards = len(index)
        if numCards == 1:
            return index[0]
        elif numCards==0:
            print "Card not found"
            return -1
        else:
            return index

    def removeCard(self,card):
        index = self.findCard(card)
        if index > 0:
            del self.deck[index]
        else:
            "Something went wrong in Deck.removeCard!"

    def draw(self):
        return self.deck.pop()

class Player:
    def __init__(self,deck):
        self.faceDown = deck.draw()
        self.faceUp = deck.draw()
        self.drawnCards = []
    def hit(self,deck):
        self.drawnCards.append(deck.draw())

    def stay(self):
        print 'implement me'

    def score(self):
        score = 0
        aces = 0
        cards = [self.facedown, self.faceup, self.drawnCards]
        cards = list(itertools.chain.from_iterable(cards))
        for card in cards:
            if 0 < card.rank < 9:
                score += card.rank
            elif card.rank == 0:
                aces += 1
            else:
                score += 10
        # aces have a value of 1 or 11
        # XXX: What happens when I have Ace, King, Ace?
        if aces > 0:
            for ace in range(aces):
                if score + 11 < 22:
                    score += 11
                else:
                    score += 1
        return score

'''class Dealer(Player):
    #Dealer draws a faceup and facedown card first.



class Agent:'''


class BlackJackEnvironment:
    def __init__(self):
        temp = 0

    # i.e. play a hand of blackjack.
    def playEpisode(self):
        deck = Deck()
        #Dealer draws first
        dealer = Player(deck)
        #Agent draws second.
        player = Player(deck)
        while(True):


    def bust(self, player):
        if player.score() > 21:
            print "Implement Bust!"

import unittest

class TestDeck(unittest.TestCase):
    def testCard(self):
        card = Card(0,0)
        self.assertEqual( card.suit, 0)
        self.assertEqual( card.rank, 0)

    def testCardEquality(self):
        card1 = Card(1,1)
        card2 = Card(1,1)
        card3 = Card(1,2)
        card4 = Card(2,1)
        card5 = Card(2,5)
        # The cards are the same
        self.assertEqual(card1 == card2, True)
        # Card3 is a different rank.
        self.assertEqual(card1 == card3, False)
        # Card4 is a different suit.
        self.assertEqual(card1 == card4, False)
        # card5 is a differen suit and rank.
        self.assertEqual(card1 == card5, False)

    def testCardCount(self):
        deck = Deck()
        self.assertEqual(len(deck.deck), 52)

    def testFindCard(self):
        deck = Deck()
        card = Card(1,1)
        index = deck.findCard(card)
        self.assertEqual(card, deck.getCard(index))


    def testCardRemoval(self):
        deck = Deck()
        card = Card(1,1)
        deck.removeCard(card)
        self.assertEqual(deck.findCard(card),-1)

    def testDraw(self):
        deck = Deck()
        card = deck.draw()
        print card
        self.assertEqual(deck.findCard(card),-1)
        self.assertEqual(deck.cardCount(),51)




if __name__ == '__main__':
    unittest.main()
