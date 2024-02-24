# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left

def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # Start the ball in the center
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # Initial velocity is in the range of...
    
    hori_vel = random.randrange(90, 150)
    vert_vel = random.randrange(60, 120)
    
    # Set the initial velocity based on direction
    # Note: divide by draw_handler refresh frequency of 60
    
    if direction == RIGHT:
        ball_vel = [(hori_vel / 60.0) , -1.0 * (vert_vel / 60.0)]
    else:
        ball_vel = [-1.0 * (hori_vel / 60.0) , -1.0 * (vert_vel / 60.0)]

# Pick a direction in which the ball will start so a new game doesn't always
# start in the same direction
def pick_direction():
    
    # Pick a number from 0..9
    
    coin = random.randint(0, 10)
    
    # Even goes to the right!
    
    if (coin % 2) == 0:
        return RIGHT
    else:
        return LEFT

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # Set the initial paddle positions and start them at zero velocity
    
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0.0 
    paddle2_vel = 0.0
    
    # Reset the scores
    
    score1 = 0
    score2 = 0
    
    # Call spawn_ball to start things off... flip a coin for direction
    
    spawn_ball(pick_direction())

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]

    # check the upper and lower edges and bounce
    
    new_vert = ball_pos[1] + ball_vel[1]
    
    if (new_vert < BALL_RADIUS) or (new_vert > (HEIGHT - BALL_RADIUS)):
        ball_vel[1] = -1.0 * ball_vel[1]

    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    # check both the upper edge (HALF_PAD_HEIGHT) and the lower edge
    # (HEIGHT - HALF_PAD_HEIGHT)
    
    if ((paddle1_pos + paddle1_vel) < HALF_PAD_HEIGHT):
        paddle1_pos = HALF_PAD_HEIGHT
    elif ((paddle1_pos + paddle1_vel) > (HEIGHT - HALF_PAD_HEIGHT)):
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle1_pos += paddle1_vel

    if ((paddle2_pos + paddle2_vel) < HALF_PAD_HEIGHT):
        paddle2_pos = HALF_PAD_HEIGHT
    elif ((paddle2_pos + paddle2_vel) > (HEIGHT - HALF_PAD_HEIGHT)):
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle2_pos += paddle2_vel
    
    # draw paddles - line of width of paddle
    
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],
                     [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                     PAD_WIDTH, "White")
    canvas.draw_line([(WIDTH - HALF_PAD_WIDTH), paddle2_pos - HALF_PAD_HEIGHT],
                     [(WIDTH - HALF_PAD_WIDTH), paddle2_pos + HALF_PAD_HEIGHT],
                     PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide    
    # and check for ball touching left gutter
    # if the ball hits a paddle add 10% to its velocity and reverse
    # horizontal direction
    
    if (ball_pos[0] < (PAD_WIDTH + BALL_RADIUS)):
        if ((ball_pos[1] >= (paddle1_pos - HALF_PAD_HEIGHT)) and
            (ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT))):
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 += 1
            spawn_ball(RIGHT)
            
    elif (ball_pos[0] > (WIDTH - (PAD_WIDTH + BALL_RADIUS))):
        if ((ball_pos[1] >= (paddle2_pos - HALF_PAD_HEIGHT)) and
            (ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT))):
            ball_vel[0] = -1.1 * ball_vel[0]            
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # draw scores
    
    canvas.draw_text(str(score1), [WIDTH / 4, HEIGHT / 8], 36, "White")
    canvas.draw_text(str(score2), [3 *(WIDTH / 4), HEIGHT / 8], 36, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # Left paddle: w goes up and s goes down
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 3
        
    # Right paddle: up arrow and down arrow
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 3
   
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    # Left paddle: w goes up and s goes down
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        
    # Right paddle: up arrow and down arrow
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
   
def restart_handler():
    # if the restart button is pressed call new_game()
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart_handler, 125)


# start frame
new_game()
frame.start()

