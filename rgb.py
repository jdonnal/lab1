#!/usr/bin/python
import pygame
import serial
import pygame, sys
from pygame.locals import *

# Declare constants (ALL CAPS)
HEIGHT = 500
WIDTH = 400
WHITE = (255,255,255)

def main():
    # Create the game window
    pygame.init()
    DISPLAY_SURF=pygame.display.set_mode((500, 400))
    pygame.display.set_caption('RGB World!')

    # Create a font object
    fontObj = pygame.font.Font('freesansbold.ttf', 32)

    # Open up the serial connection to Arduino
    s = serial.Serial("/dev/ttyACM0",9600,
                      timeout=0.5)
    # Game Loop
    while(True):
        # (1) Handle pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # (2) Handle custom logic
        rgb = read_arduino(s)
        if(rgb is None):
            continue # skip, and try again next time
        # set the display color
        DISPLAY_SURF.fill(rgb)
        
        # write the array to the screen
        textSurfaceObj = fontObj.render(str(rgb),True,WHITE)
        textRectObj = textSurfaceObj.get_rect()
        # center the text on the screen
        textRectObj.center = (HEIGHT/2,WIDTH/2)
        # write the text
        DISPLAY_SURF.blit(textSurfaceObj, textRectObj)

        # (3) Update the display
        pygame.display.update()

def read_arduino(myserial):
    # ask for data
    myserial.write('.')
    # read the response
    vals = myserial.readline()
    # if arduino doesn't respond
    if(len(vals)==0):
        return None #...ignore
    # convert to an array of numbers
    rgb = [int(x) for x in vals.split(',')]
    return rgb

if __name__=="__main__":
    main()

