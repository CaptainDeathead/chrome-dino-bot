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
    CACTUS_TYPES = ['1-cactus-s', '1-cactus', '2-cactus-s', '2-cactus', '3-cactus', '4-cactus', 'bird_head']
    CACTUS_WAIT_TIME_FACTOR = 0.1
    DINO_JUMP_DIST = 100
    IMG_DETECT_CONFIDENCE = 0.99
    BASE_DINO_SPEED = 12 # WITH START SLOWER = 12, WITHOUT = 14
    TOP_BIRD_HEAD_Y = 60

    def __init__(self, dino: Dino, surface: pg.Surface, bot_playing: bool = True) -> None:
        self.dino = dino
        self.surface = surface

        self.cactus_images = []
        for cactus_type in self.CACTUS_TYPES:
            self.cactus_images.append(Image.open(f"Images/Dark/{cactus_type}.png"))
            self.cactus_images.append(Image.open(f"Images/Light/{cactus_type}.png"))
        
        self.restart_img = Image.open("Images/restart.png")

        self.cacti = []
        self.last_cactus_addition = 0

        self.dino_speed = 0
        self.nojump_dist = self.DINO_JUMP_DIST
        self.last_offsets = [0 for _ in range(10)]

        self.game_over = False
        self.score = 0
        self.bot_playing = bot_playing

    def add_cactus(self, cactus_rect: pg.Rect) -> None:        
        self.last_cactus_addition = time()
        self.cacti.append(Cactus(cactus_rect, self.last_cactus_addition))

    def update_cacti(self, cacti_rects: pg.Rect) -> None:
        cacti_len = len(self.cacti)

        dino_offset = 1.113 ** self.dino_speed

        self.last_offsets.pop(0)
        self.last_offsets.append(dino_offset)

        actuall_offset = sum(self.last_offsets) / len(self.last_offsets)
        self.nojump_dist = self.DINO_JUMP_DIST + actuall_offset

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

    def reset(self) -> None:
        print("RESTARTING!!!")
        self.dino.jump()

        self.__init__(self.dino, self.surface)

    def grab_and_update(self, screenshot) -> None:
        restart_btns = list(_locateAll_opencv(self.restart_img, screenshot, grayscale=True, confidence=self.IMG_DETECT_CONFIDENCE))

        if len(restart_btns) > 0:
            print("Game end!")
            if self.bot_playing:
                self.reset()
            
            self.game_over = True
            return

        cacti_rects = []
        used_x_values = []

        for i, cactus_img in enumerate(self.cactus_images):
            for cactus in _locateAll_opencv(cactus_img, screenshot, grayscale=True, confidence=self.IMG_DETECT_CONFIDENCE):
                if i == 13 or i == 12:
                    if int(cactus.top) < self.TOP_BIRD_HEAD_Y:
                        if self.bot_playing: continue

                cactus_left = int(cactus.left)

                if cactus_left < self.nojump_dist:
                    if self.bot_playing: self.dino.jump()
                    
                    self.cacti = []
                    self.score += 1
                    #print("Jump")

                add_value = True

                for x_value in used_x_values:
                    if abs(cactus_left - x_value) < 40: add_value = False

                if add_value:
                    used_x_values.append(cactus_left)
                    cacti_rects.append(pg.Rect(cactus_left, int(cactus.top), cactus.width, cactus.height))

        if len(cacti_rects) == 0: return

        cacti_rects = sorted(cacti_rects, key=lambda rect: rect.x)
        self.update_cacti(cacti_rects)