# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# Geometry of the playing area
CANVAS_HEIGHT = 600
CANVAS_WIDTH = 600
# Position for top banner
BANNER_POS = (25, 35)
BANNER_FONT_SIZE = 36
BANNER_TEXT = "Blackjack"
BANNER_COLOR = "White"
# Message during play
MESSAGE_POS = (250, 325)
SCORE_POS = (450, 35)
# Player's hand
PLAYER_HAND_POSX = 100
PLAYER_HAND_POSY = 150
# Dealer's hand
DEALER_HAND_POSX = 100
DEALER_HAND_POSY = 450
DEALER_HAND_POS = (DEALER_HAND_POSX, DEALER_HAND_POSY)

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []
        self.reveal_first = True  # This enables control over reveal of first card

    def __str__(self):
        retstr = "Hand contains"
        for card in self.card_list:
            retstr = retstr + " " + card.suit + card.rank
        return retstr

    def add_card(self, card):
        self.card_list.append(card)
        
    # Hide first card
    def hide(self):
        self.reveal_first = False
        
    # Reveal first card        
    def reveal(self):
        self.reveal_first = True
    # Calculate the hand's value    
    def get_value(self):
        # count aces as 1, if the hand has an ace,
        # then add 10 to hand value if it doesn't bust
        hand_value = 0
        hold_ace = False
        
        for card in self.card_list:
            hand_value += VALUES.get(card.rank)
            if card.rank == 'A':
                hold_ace = True
        # if we have an ace and don't go bust at 11, add 10
        if hold_ace and (hand_value <= 11):
            return hand_value + 10
        else:
            return hand_value
    # Display the hand
    def draw(self, canvas, pos):
        cardnum = 0
        # Step through the cards
        for card in self.card_list:
            # Treat the first card special, in case it should be hidden
            if cardnum == 0:
                if self.reveal_first:
                    # Reveal, so have Card do the work
                    card.draw(canvas, (pos[0] + cardnum * (CARD_SIZE[0] +5), pos[1]))
                else:
                    # Hide, so draw the back of the card (it's always the first one)
                    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                                      (pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]),
                                      CARD_BACK_SIZE)
            else:
                card.draw(canvas, (pos[0] + cardnum * (CARD_SIZE[0] +5), pos[1]))
            cardnum += 1
            
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []        
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(-1)
    
    def __str__(self):
        retstr = "Deck contains"
        for card in self.cards:
            retstr = retstr + " " + card.suit + card.rank
        return retstr

#define event handlers for buttons
def deal():
    global outcome, in_play, the_deck, player_hand, dealer_hand, score
    # if player hits deal button during play, they lose that hand
    if in_play:
        score -= 1
    # fresh deck
    the_deck = Deck()
    # shuffle the deck
    the_deck.shuffle()
    # set up the clear hands
    player_hand = Hand()
    dealer_hand = Hand()
    # deal cards in order player-dealer-player-dealer
    player_hand.add_card(the_deck.deal_card())
    dealer_hand.add_card(the_deck.deal_card())
    player_hand.add_card(the_deck.deal_card())
    dealer_hand.add_card(the_deck.deal_card())
    # play has started on this deal
    in_play = True
    # Prompt for next step
    outcome = "Hit or Stand?"

def hit():
    global score, in_play, outcome
    # if the hand is over, don't allow a hit
    if in_play:
        player_hand.add_card(the_deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            in_play = False
            score -= 1
            outcome = "You have busted!"

def stand():
    global score, in_play, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        in_play = False
        # if we hit 17, dealer stands
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(the_deck.deal_card())
        # we're done accepting cards
        if (player_hand.get_value() > dealer_hand.get_value()) or (dealer_hand.get_value() > 21):
            outcome = "You have won!!"
            score += 1
        else:
            outcome = "Dealer wins!"
            score -= 1

# draw handler    
def draw(canvas):
    global in_play
    # draw the banner and text indicators
    canvas.draw_text(BANNER_TEXT, BANNER_POS, BANNER_FONT_SIZE, BANNER_COLOR)
    canvas.draw_text("Player", (200, 125), 30, "White")
    canvas.draw_text("Dealer", (200, 425), 30, "White")
    # draw the player's hand
    player_hand.draw(canvas, [PLAYER_HAND_POSX, PLAYER_HAND_POSY])
    # draw the dealer's hand - hide first card, if the deal is on-going
    if in_play:
        dealer_hand.hide()
    else:
        dealer_hand.reveal()
    dealer_hand.draw(canvas, [DEALER_HAND_POSX, DEALER_HAND_POSY])
    # status message and score
    canvas.draw_text(outcome, MESSAGE_POS, 30, "White")
    canvas.draw_text("Score: " + str(score), SCORE_POS, 30, "White")
    # if hand is done ask about another deal
    if not in_play:
        canvas.draw_text('Another deal?', (MESSAGE_POS[0], MESSAGE_POS[1] + 32), 30, "White")

# initialization frame
frame = simplegui.create_frame("Blackjack", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()


# remember to review the gradic rubric

