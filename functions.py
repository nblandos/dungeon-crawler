import pygame
import hashlib
import os
import random


def get_hit_box(surface, top=0, left=0):
    # Returns the minimal bounding area of an image
    surface_mask = pygame.mask.from_surface(surface)
    rect_list = surface_mask.get_bounding_rects()
    if rect_list:
        hit_box = rect_list[0].unionall(rect_list)
        hit_box.move_ip(top, left)
        return hit_box


def time_passed(time, amount):
    if pygame.time.get_ticks() - time > amount:
        return True


def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

