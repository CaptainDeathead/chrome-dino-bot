import pygame as pg
import pyautogui as pag

class Dino:
    def __init__(self, rect: pg.Rect) -> None:
        self.rect = rect

    def jump(self) -> None:
        pag.press("space")