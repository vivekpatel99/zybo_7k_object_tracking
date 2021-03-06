 # -*- coding: utf-8 -*-
# @Author: vivekpatel99
# @Date:   2018-10-06 15:43:12
# @Last Modified by:   vivekpatel99
# @Last Modified time: 2018-10-06 16:43:29

"""
The main script calls functions from all the modules

"""

import os
import sys
import pygame
from pygame.locals import *



""" modules """

from definition import define
from tasks.face_recog import face_recog
from tasks.motion_detection import motion_detect
from tasks.cam_off import cam_off
from tasks.object_recognition import object_recognition
import globals

sys.path.append("/lib/display")
from lib.display import display_gui
from lib.display import display
from lib._logger import _logging

# -----------------------------------------------
PROJECT_TITLE = 'Closed Loop Object Tracking based on Image Recognition'

# -----------------------------------------------
""" constants declaration  """

SCREEN_SIZE = (1265, 1015)  # width, height
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Frames per second
FPS = 60

TASK_INDEX = 0


# ------------------------------------------------------------------------------
# """ FUNCTION: Setting the environment variable for displaying GUI """
# ------------------------------------------------------------------------------

def env_setup(fbpath="/dev/fb0"):
    # os.putenv("SDL_FBDEV", fbpath)
    os.environ["SDL_FBDEV"] = fbpath

    # set up audio driver to avoid alisa lib erros
    os.environ['SDL_AUDIODRIVER'] = "dsp"
    # os.environ['SDL_VIDEODRIVER'] = "svgalib"
    # os.putenv['SDL_VIDEODRIVER'] = "fbcon"


# ----------------------------------------------------------------------------------------------------------------------
# """ MAIN FUNCTION """
# ----------------------------------------------------------------------------------------------------------------------

def main_():
    """
    """

    env_setup()

    define.platform_init()

    try:
        pygame.init()
    except Exception as error:
        print(error)

    # title fonts
    fonts = pygame.font.SysFont("Comic Sans MS", 40)
    title = fonts.render(PROJECT_TITLE, False, (0, 0, 255))
    print("[INFO] title set up done...")

    # making mouse invisible
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

    screen.fill(WHITE)

    while True:

        if TASK_INDEX is 0:
            # cam_test.main()
            pass
        if TASK_INDEX is 1:
            face_recog.face_recog_pygm(screen, FPS)


# ----------------------------------------------------------------------------------------------------------------------
# """ main """
# ----------------------------------------------------------------------------------------------------------------------

def main():
    """
    """
    env_setup()

    log = _logging.logger_init(log_filepath="obj_track_img_recog.log", project_name="main")
    log.info("main script starts")

    log.info("calling  define.platform_init()")
    define.platform_init()

    log.info("calling  display_gui.Menu()")
    disply = display_gui.Menu()

    log.info("calling  disply.display_init()")
    screen = disply.display_init()

    log.info("calling  disply.display_color()")
    disply.display_color()

    log.info("calling  display.display_menu_init()")
    disply_obj = display.display_menu_init(screen)

    while True:
            if not globals.CAM_START: # camera is off, picture will be displayed
                screen.fill(WHITE) # clean up the display
                cam_off.cam_off_loop(screen, disply_obj)

            if globals.EXIT:
                break

            while globals.CAM_START:

                if globals.TASK_INDEX is 1:
                    screen.fill(WHITE)
                    face_recog.face_recog_pygm(screen, disply_obj, FPS)

                if globals.TASK_INDEX is 2:
                    screen.fill(WHITE)
                    motion_detect.motion_detection_pygm(screen, disply_obj, FPS)

                if globals.TASK_INDEX is 3:
                    screen.fill(WHITE)
                    object_recognition.object_recog_pygm(screen, disply_obj)

                if not globals.CAM_START or globals.EXIT:
                    log.info("Camera is OFF")
                    break

            if globals.EXIT:
                break

    pygame.quit()
    log.info("exiting from the main...")

if __name__ == '__main__':
    main()
