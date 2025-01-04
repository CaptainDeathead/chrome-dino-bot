import pygame as pg

from time import time

from dino import Dino
from image_recognition import _locateAll_opencv
from PIL import Image

class Cactus:
    def __init__(self, rect: pg.Rect, index: int) -> None:
        self.rect = rect
        self.index = index

    def __str__(self):
        return str(self.rect)
    
    def __repr__(self):
        return str(self.rect)

class CactiManager:
    CACTUS_TYPES = ['1-cactus-s', '1-cactus', '2-cactus-s', '2-cactus', '3-cactus', '4-cactus']
    CACTUS_WAIT_TIME_FACTOR = 0.1
    DINO_JUMP_DIST = 100
    IMG_DETECT_CONFIDENCE = 0.95
    BASE_DINO_SPEED = 12 # WITH START SLOWER = 12, WITHOUT = 14

    def __init__(self, dino: Dino, surface: pg.Surface) -> None:
        self.dino = dino
        self.surface = surface

        self.cactus_images = []
        for cactus_type in self.CACTUS_TYPES:
            self.cactus_images.append(Image.open(f"Images/Dark/{cactus_type}.png"))
            self.cactus_images.append(Image.open(f"Images/Light/{cactus_type}.png"))

        self.cacti = []
        self.last_cactus_addition = 0

        self.dino_speed = 0
        self.nojump_dist = self.DINO_JUMP_DIST

    def add_cactus(self, cactus_rect: pg.Rect) -> None:
        if time() - self.last_cactus_addition < self.dino_speed * self.CACTUS_WAIT_TIME_FACTOR:
            #return
            ...
        
        self.last_cactus_addition = time()
        self.cacti.append(Cactus(cactus_rect, self.last_cactus_addition))

    def update_cacti(self, cacti_rects: pg.Rect) -> None:
        cacti_len = len(self.cacti)

        if cacti_len > 0:
            #print(self.cacti[0].rect.x)
            #print(self.cacti)
            ...

        dino_offset = 1.1 ** self.dino_speed

        self.nojump_dist = self.DINO_JUMP_DIST + dino_offset

        if cacti_len > 0:
            print(self.cacti[0].rect.x, self.nojump_dist)        

        #if cacti_len > 0 and self.cacti[0].rect.x < self.nojump_dist:
        #    self.dino.jump()
        #    print("Jumping...")
        #    self.cacti.pop(0)

        cacti_len = len(self.cacti)

        for i, cactus_rect in enumerate(cacti_rects):
            if i >= cacti_len:
                self.add_cactus(cactus_rect)
            else:
                self.set_dino_speed(self.cacti[i].rect.x - cactus_rect.x)
                self.cacti[i].rect = cactus_rect

                #pg.draw.rect(self.surface, (255, 0, 0), self.cacti[i].rect)

    def set_dino_speed(self, new_dino_speed: int) -> None:
        self.dino_speed = new_dino_speed

    def grab_and_update(self, screenshot) -> None:
        cacti_rects = []
        used_x_values = []

        for cactus_img in self.cactus_images:
            for cactus in _locateAll_opencv(cactus_img, screenshot, grayscale=True, confidence=self.IMG_DETECT_CONFIDENCE):
                cactus_left = int(cactus.left)

                if cactus_left < self.nojump_dist:
                    self.dino.jump()
                    self.cacti = []
                    print("Jump")

                add_value = True

                for x_value in used_x_values:
                    if abs(cactus_left - x_value) < 40: add_value = False

                if add_value:
                    used_x_values.append(cactus_left)
                    cacti_rects.append(pg.Rect(cactus_left, int(cactus.top), cactus.width, cactus.height))

        if len(cacti_rects) == 0: return

        cacti_rects = sorted(cacti_rects, key=lambda rect: rect.x)

        #print(cacti_rects)
        self.update_cacti(cacti_rects)