# implementation of Spaceship - program template for RiceRocks
# N.B. - this runs on CodeSkulptor currently
# todo - implement generic GUI

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

# game globals
MAX_ROCKS = 12
ROCK_SPEED = 0.6
rock_vel_range = 0.6
rock_counter = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def recenter(self, center_pos):
        self.pos = center_pos
        self.vel = [0 , 0]
        self.angle = 0
        self.angle_vel = 0
        self.thrust = False
        
    def shoot(self):
        global a_missile, missile_group
        # create a new missile and shoot it
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        # add a_missile to the missile_group
        missile_group.add(a_missile)    

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image,
                              [self.image_center[0] + self.age * self.image_size[0],
                               self.image_center[1]],
                              self.image_size, self.pos, self.image_size, self.angle)
        
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) < (self.radius + other_object.get_radius()):
            return True
        return False

    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def get_angle(self):
        return self.angle
    
    def update(self):
        # update age of sprite and check against lifespan
        self.age += 1
        if self.age >= self.lifespan:
            # indicate removal - nothing else to be done
            return True
        
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # keep this sprite!
        return False

# key handlers to control ship   
def keydown(key):
    if started:
        if key == simplegui.KEY_MAP['left']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(True)
        elif key == simplegui.KEY_MAP['space']:
            my_ship.shoot()
        
def keyup(key):
    if started:
        if key == simplegui.KEY_MAP['left']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, rock_vel_range, rock_counter
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        # click to start, so set lives and score
        lives = 3
        score = 0
        started = True
        # set the rock_vel_range to its original value
        rock_vel_range = ROCK_SPEED
        rock_counter = 0
        # provide a soundtrack
        soundtrack.rewind()
        soundtrack.play()

def draw(canvas):
    global time, started, lives, score, rock_group
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    # check for collisions
    if group_collide(my_ship, rock_group):
        # reduce lives
        lives -= 1
        # if we are down to zero lives
        if lives == 0:
            # set game to not started and
            # clear all the rocks, reset scores and score
            started = False
            rock_group = set()
            soundtrack.rewind()
            # park the ship back at the center
            my_ship.recenter([WIDTH / 2, HEIGHT / 2])
            print my_ship.get_position()
            
    # check for missile hits on rocks
    score = score + (10 * group_group_collide(rock_group, missile_group))
    
    # update ship and sprites
    my_ship.update()
    update_sprite_group(rock_group)
    update_sprite_group(missile_group)
    update_sprite_group(explosion_group)

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# helper - process_sprite_group
def process_sprite_group(canvas, sp_grp):
    # go across each of the sprites in the group and draw them
    for sp in sp_grp:
        sp.draw(canvas)
    
# helper - update_sprite_group
def update_sprite_group(sp_grp):
    # in case we have discards coming up
    sp_discs = set()
    # for each sprite in the group update its position
    for sp in sp_grp:
        # update and check if lifespan exceeded
        if sp.update():
            sp_discs.add(sp)
    # iterate over discards to remove them
    for sp in sp_discs:
        sp_grp.discard(sp)
        
# helper group_collide - see if obj1 collides with the group
def group_collide(obj1, sp_grp):
    global explosion_group
    # for each sprite in the group test for collision and return True if yes
    for sp in sp_grp:
        if sp.collide(obj1):
            # create an explosion at the location of sp
            a_boom = Sprite(sp.get_position(), [0, 0],
                            sp.get_angle(), 0.0,
                            explosion_image,
                            explosion_info,
                            explosion_sound)
            # add this boom to the explosion group
            explosion_group.add(a_boom)
            # discard sp - eliminates chance of ship materializing in the
            # rock that it just flew into (also discards missile, which 
            # prevents a single missile from hitting >1 rock)
            # n.b. - discard is safe, as we leave the for loop immediately
            sp_grp.discard(sp)
            return True
    # no collisions, so return False
    return False

# helper group_group_collide - note sp_grp1 are the ones to be destroyed!
def group_group_collide(sp_grp1, sp_grp2):
    # set up the hit count and discard set
    hit_count = 0
    sp_discs = set()
    # sp_grp1 should be rocks, if we shoot missiles in sp_grp2
    for sp in sp_grp1:
        if group_collide(sp, sp_grp2):
            hit_count += 1
            sp_discs.add(sp)
    # now remove the struck objects
    for sp in sp_discs:
        sp_grp1.discard(sp)
    # and get set for score update
    return hit_count

# timer handler that spawns a rock and adds it to the rock group    
def rock_spawner():
    global a_rock, rock_group, rock_vel_range, rock_counter
    # make sure we have started and not maxed out the rocks
    if started and (len(rock_group) < MAX_ROCKS):
        # generate a new rock position
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        # check against ship position - if we're clear by a bit
        if dist(rock_pos, my_ship.get_position()) > 1.5 * (asteroid_info.get_radius() + my_ship.get_radius()):
            rock_vel = [random.random() * rock_vel_range - .3,
                        random.random() * rock_vel_range - .3]
            rock_avel = random.random() * .2 - .1
            a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
            # add the rock to the group
            rock_group.add(a_rock)
            # keep track of how many rocks we've generated in the game for speed control
            rock_counter += 1
            # every MAX_ROCKS increase rock_vel_range by a factor...
            rock_vel_range = (1 + (rock_counter // MAX_ROCKS)) * ROCK_SPEED
            
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and create (empty) sets for missiles, rocks and explosions 
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
