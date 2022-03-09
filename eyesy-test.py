import importlib
import argparse
import random
import math
import os
import pygame
import pygame.gfxdraw
from pygame.color import THECOLORS

# we use these next few lines in order to run the patch we want to test from the command line using "python3 eyesy-test.py module_you_want_to_test.py", it will remove the .py extension from the module and that will become the variable "eyesy_mode"
parser = argparse.ArgumentParser(description="Critter and Guitari Eyesy program debug environment")
parser.add_argument('module', type=str, help="Filename of the Pygame program to test")
parser.add_argument('-r', '--record', type=int, help="Record out to image sequence for ffmpeg")
args = parser.parse_args()
eyesy_mode = importlib.import_module(args.module.split('.py')[0])



# initialize to Eyesy's resolution
screenWidth, screenHeight = 1280, 720
# pygame.init() might not be needed 
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Knob values and settings, .5 is as if they were at 12 o'clock
knobs = {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.2, 5: 0.5, "step": 0.0005}

# give ourselves our initial values
class eyesy(object):
    def __init__(self):
        for knob_id in range(1, 6): # shorthand way of having self.knob# and setting it to the values from the dictionary made before 
            setattr(self, f"knob{knob_id}", knobs[knob_id])

        self.audio_in = [random.randint(-32768, 32767) for i in range(100)]
        self.bg_color = (0, 0, 0)
        self.audio_trig = False
        self.midi_note_new = False
        self.mode_root = os.path.dirname(eyesy_mode.__file__)
        # xres and yres seem to work best as matching screenWidth and screenHeight
        self.xres = 1280
        self.yres = 720

# color_picker is used to change the color of the drawings via knob4
    def color_picker(self):
        """
        Original color_picker function from ETC. See link below:
        https://github.com/critterandguitari/ETC_Mother/blob/master/etc_system.py
        """
        c = self.knob4

        # all the way down random bw
        rando = random.randrange(0, 2)
        color = (rando * 255, rando * 255, rando * 255)
        #print(c)
        # random grey and white
        if c > .02 :
            rando = random.randrange(0,255)
            color = (rando, rando, rando)
        # dark grey
        if c > .04 :
            color = (50, 50, 50)
        # medium-dark grey
        if c > .06 :
            color = (100, 100 ,100)
        # medium-light grey
        if c > .08 :
            color = (150, 150 ,150)
        # light grey
        if c > .10 :
            color = (175, 175 ,175)
        # lightest grey
        if c > .12 :
            color = (200, 200 ,200)
        # white
        if c > .14 :
            color = (250, 250 ,250)
        #colors that fade into each other
        if c > .16 :
            r = math.sin(c * 2 * math.pi) * .5 + .5
            g = math.sin(c * 4 * math.pi) * .5 + .5
            b = math.sin(c * 8 * math.pi) * .5 + .5
            color = (r * 255,g * 255,b * 255)
        # random colors
        if c > .96 :
            color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        # random colors but even brighter
        if c > .98 :
            r = random.randrange(0, 2) * 255
            g = random.randrange(0, 2) * 255
            b = random.randrange(0, 2) * 255
            color = (r,g,b)

        #color2 = (color[0], color[1], color[2]) i don't think this is needed, seems to be working okay without it

        return color

    def color_picker_bg(self):
        """
        Original color_picker_bg function from ETC. See link below:
        https://github.com/critterandguitari/ETC_Mother/blob/master/etc_system.py
        """
        #print(self.knob5)
        c = self.knob5
        r = (1 - (math.cos(c * 3 * math.pi) * .5 + .5)) * c
        g = (1 - (math.cos(c * 7 * math.pi) * .5 + .5)) * c
        b = (1 - (math.cos(c * 11 * math.pi) * .5 + .5)) * c
        #print(c,r,g,b)
        color = (r * 255, g * 255, b * 255)
        #print(color)
        self.bg_color = color
        return color


def update_knobs(key, knobs):
    """Update knobs but pressing a number between 1 - 5 and up/down keys together"""
    for knob_id in range(1, 6):
        if key[getattr(pygame, f"K_{knob_id}")] and key[pygame.K_UP]:
            knobs[knob_id] += knobs["step"]
            knobs[knob_id] = min(knobs[knob_id], 1.0)
            setattr(eyesy_instance, f"knob{knob_id}", knobs[knob_id])
        if key[getattr(pygame, f"K_{knob_id}")] and key[pygame.K_DOWN]:
            knobs[knob_id] -= knobs["step"]
            knobs[knob_id] = max(knobs[knob_id], 0.0)
            setattr(eyesy_instance, f"knob{knob_id}", knobs[knob_id])


eyesy_instance = eyesy()

eyesy_mode.setup(screen, eyesy_instance) # takes in the screen we set up and the initial settings of the eyesy_instance
running = True
recording = False
counter = -1

"""can probably get rid of these 
if args.record:
    recording = True
    print('recording')

if recording:
    if not os.path.exists('imageseq'):
        os.makedirs('imageseq')
    counter = 0"""

while running: # this is where we interact with everything and simulate using the eyesy
    #screen.fill(THECOLORS['black']) might not be needed
    eyesy_mode.draw(screen, eyesy_instance) 

    key = pygame.key.get_pressed() # registers what key(s) are/is being pressed 
    update_knobs(key, knobs)
    if key[pygame.K_q]:
        exit()

    if key[pygame.K_SPACE]:
        eyesy_instance.audio_trig = True
        print("true")
    if key[pygame.K_z]:
        eyesy_instance.audio_trig = False
        print("false")
    
    # from DudeTheDev
    # pressing x simulates loud audio playing, c simulates low audio
    if key[pygame.K_x]:
        eyesy_instance.audio_in = [random.randint(-32768, 32767) for i in range(100)]
    if key[pygame.K_c]:
        eyesy_instance.audio_in = [random.randint(-300, 300) for i in range(100)]
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if you try to quit, let's leave this loop
            running = False
    pygame.display.flip()

"""cant also probably delete this 
  if recording and counter < args.record:
        pygame.image.save(screen, "imageseq/%05d.jpg" % counter)
        counter += 1
    elif recording and counter == args.record:
        exit()"""
