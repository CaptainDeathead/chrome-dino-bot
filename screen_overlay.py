import win32gui
import win32con
import win32api

import pygame as pg

# CREDIT: chatgpt.com
def draw_pixel(x: int, y: int, color: tuple[int, int, int]):
    """
    Draws a single pixel on the screen at (x, y) with the specified color.
    Args:
        x (int): X coordinate of the pixel.
        y (int): Y coordinate of the pixel.
        color (tuple): RGB color as (R, G, B).
    """
    hdc = win32gui.GetDC(0)  # Get the device context for the entire screen
    rgb_color = win32api.RGB(*color)  # Convert (R, G, B) to Windows RGB format
    win32gui.SetPixel(hdc, x, y, rgb_color)  # Set the pixel at (x, y)
    win32gui.ReleaseDC(0, hdc)  # Release the device context

def pygame_surface_to_list(surface: pg.Surface) -> list[list[tuple[int, int, int]]]:
    width, height = surface.get_size()
    rgb_list = []

    for y in range(height):
        row = []
        for x in range(width):
            pixel = surface.get_at((x, y))
            if pixel.a == 255:
                row.append((pixel.r, pixel.g, pixel.b))
            else:
                row.append((0, 0, 0))

        rgb_list.append(row)

    return rgb_list    

def blit_pygame_surface(surface: pg.Surface, coords: tuple[int, int]) -> None:
    array = pygame_surface_to_list(surface)

    for y in range(len(array)):
        for x in range(len(array[y])):
            if array[y][x] == (0, 0, 0): continue 

            draw_pixel(x + coords[0], y + coords[1], array[y][x])