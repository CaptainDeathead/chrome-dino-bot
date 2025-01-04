import pyautogui as pag
import pygame as pg

from dino import Dino
from cactus import CactiManager
from screen_overlay import blit_pygame_surface

pg.init()

surfaces = []

#pag.mouseInfo() # Use this to get the dino window rect
dino_rect = pg.Rect(2575-1920, 127, 3195-2575, 339-127)

surface = pg.Surface(dino_rect.size)
pg.draw.rect(surface, (0, 255, 0), (0, 0, dino_rect.w, dino_rect.h), width=5)

dino = Dino(dino_rect)
cacti_manager = CactiManager(dino, surface)

while 1:
    #blit_pygame_surface(surface, (dino_rect.x, dino_rect.y))
        
    screenshot = pag.screenshot(None, region=dino_rect)
    cacti_manager.grab_and_update(screenshot)