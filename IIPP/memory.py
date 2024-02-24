# implementation of card game - Memory

import simplegui
import random

# Set up some globals constants
CARD_HEIGHT = 100
CARD_WIDTH  = 50
CARD_NUM_POSX = 12
CARD_NUM_POSY = 68
FONT_SIZE = 60

# Set up some globals, starting with a set of cards and set them hidden
cards = range(8) + range(8)
exposed = [False] * len(cards)

# helper function to initialize globals
def new_game():
    global cards, cards_revealed, exposed, turns
    
    # Shuffle the cards
    random.shuffle(cards)
    # all cards are hidden
    cards_revealed = 0
    #
    for n in range(len(cards)):
        exposed[n] = False
    # set turns back to 0
    turns = 0
    # update the label
    new_label = "Turns = " + str(turns)
    label.set_text(new_label)

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global cards_revealed, first_card, second_card, turns

    # Determine the card that was clicked on (divide by CARD_WIDTH)
    card_num = pos[0] // CARD_WIDTH
    # if this card is already exposed, we're all done here
    if exposed[card_num]:
        return    
    # if no cards have been revealed, expose the card and remember its index
    if cards_revealed == 0:
        exposed[card_num] = True
        first_card = card_num
        cards_revealed = 1
    # if one card is revealed expose the card and remember the 2nd index
    elif cards_revealed == 1:
        exposed[card_num] = True
        second_card = card_num
        cards_revealed = 2
        # update turn count and display of the count
        turns += 1
        new_label = "Turns = " + str(turns)
        label.set_text(new_label)
    else:
        # if the cards didn't match, hide them again
        if cards[first_card] <> cards[second_card]:
            exposed[first_card] = False
            exposed[second_card] = False
        # expose the new card and remember it as the first card
        exposed[card_num] = True
        first_card = card_num
        cards_revealed = 1    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    
    for n in range(len(cards)):
        card_pos = [CARD_NUM_POSX + (n * CARD_WIDTH), CARD_NUM_POSY]
        if exposed[n]:
            canvas.draw_text(str(cards[n]), card_pos, FONT_SIZE, "Red")
        else:
            # create a rectangle of size card in the nth position
            point_list = [(n * CARD_WIDTH, 0),
                          (n * CARD_WIDTH, CARD_HEIGHT),
                          ((n + 1) * CARD_WIDTH, CARD_HEIGHT),
                          ((n + 1) * CARD_WIDTH, 0)]
            canvas.draw_polygon(point_list, 1, "White", "Green")
        # draw a line to delineate cards better    
        canvas.draw_line([n * CARD_WIDTH, 0], [n * CARD_WIDTH, CARD_HEIGHT], 1, "White")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric

