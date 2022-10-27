import pygame


def get_hit_box(surf, top=0, left=0):
    # Returns the minimal bounding area of an image
    surf_mask = pygame.mask.from_surface(surf)
    rect_list = surf_mask.get_bounding_rects()
    if rect_list:
        hit_box = rect_list[0].unionall(rect_list)
        hit_box.move_ip(top, left)
        return hit_box
