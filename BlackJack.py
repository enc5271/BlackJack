import random, itertools
import numpy as np

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

# FIXME The deck is an infinite deck so cards should be replaced.
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

    # This is unused in the infinite deck.
    def removeCard(self,card):
        index = self.findCard(card)
        if index > 0:
            del self.deck[index]
        else:
            "Something went wrong in Deck.removeCard!"

    #This is an infinited deck i.e. draw with replacement.
    def draw(self):
        return random.choice(self.deck)

class Player:
    def __init__(self,deck,policy):
        self.faceDown = deck.draw()
        #This card is visible to the agent when held by the dealer.
        self.faceUp = deck.draw()
        self.drawnCards = []
        self.policy = policy

    # Draw a card from the deck.
    def hit(self,deck):
        self.drawnCards.append(deck.draw())

    def bust(self):
        return self.getScore() > 21

    def play(self, deck):
        score = self.getScore()
        action = self.policy[score]
        if action == 0:
            self.hit(deck)
            return 0
        else:
            return 1


    def getScore(self):
        score = 0
        aces = 0
        cards = self.drawnCards
        cards.append(self.faceUp)
        cards.append(self.faceDown)
        for card in cards:
            if 0 < card.rank < 9:
                score += card.rank
            elif card.rank == 0:
                aces += 1
            else:
                score += 10
        # aces have a value of 1 or 11
        if aces > 0:
            for i in range(aces):
                #add aces to score initially all valued 11. Toggle values to 1.
                scoreWithAces = score + 11*(aces - i) + 1*i
                if scoreWithAces < 22:
                    return scoreWithAces
            score = score + aces
        return score



class BlackJack:
    def __init__(self,agentPolicy, dealerPolicy):
        self.agentPolicy = agentPolicy
        self.dealerPolicy = dealerPolicy

    # i.e. play a hand of blackjack.
    def playEpisode(self):
        deck = Deck()
        #Dealer draws first
        dealer = Player(deck,self.dealerPolicy)
        #Agent draws second.
        agent = Player(deck, self.agentPolicy)
        states = [agent.getScore()]
        # FIXME should be in a loop. loop until bust or sticks.
        while(True):
            stay = agent.play(deck)
            if stay:
                break
            elif agent.bust():
                break
            else:
                states.append(agent.getScore())
        while(True):
            stay = dealer.play(deck)
            if stay:
                break
            elif agent.bust():
                break
        reward = self.scoreHand(agent,dealer)
        return states,reward

    def scoreHand(self, agent, dealer):
        agentScore = agent.getScore()
        dealerScore = dealer.getScore()
        #If the agent busts reward is -1.
        if agentScore > 21:
            return -1
        #If the dealer busts the agent wins; reward = +1
        elif dealerScore > 21:
            return 1
        #Score is tied; reward = 0
        elif dealerScore == agentScore:
            return 0
        elif dealerScore > agentScore:
            return -1
        elif agentScore > dealerScore:
            return 1
        else:
            print "Something went wrong in BlackJack.scoreHand()"

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
        self.assertNotEqual(deck.findCard(card),-1)
        self.assertEqual(deck.cardCount(),52)

class TestBlackJack(unittest.TestCase):
    def testEpisode(self):
        #Normally this is passed from MonteCarlo.py so I had to create it here for testing.
        dealerPolicy = np.zeros(22)
        for i in range(17,22):
            dealerPolicy[i] = 1
        # TODO Find the agent policy in Suttons book.
        playerPolicy = np.zeros(22)

        game = BlackJack(playerPolicy, dealerPolicy)
        self.assertTrue(-1 <= game.playEpisode() <=1)



if __name__ == '__main__':
    unittest.main()
