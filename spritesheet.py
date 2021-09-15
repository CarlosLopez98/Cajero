import pygame


class SpriteSheet:
    def __init__(self, filename, scale=None):
        """ Load the sheet """
        self.scale = scale
        try:
            self.sheet = pygame.image.load(filename).convert()
            if self.scale:
                size = self.sheet.get_size()
                self.sheet = pygame.transform.scale(self.sheet, (size[0] * self.scale, size[1] * self.scale))
        except pygame.error as e:
            print(f'Unable to load sprites sheet image: {filename}')
            raise SystemExit(e)

    def image_at(self, rectangle, color_key=None):
        """ Loads a specific image from a specific rectangle. """
        # Loads image from x, y x+offset, y+offset
        rectangle = (rectangle[0] * self.scale, rectangle[1] * self.scale,
                     rectangle[2] * self.scale, rectangle[3] * self.scale)
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        return image

    def images_at(self, rects, color_key=None):
        """ Load a whole bunch of images and return them as list. """
        return [self.image_at(rect, color_key) for rect in rects]

    def load_strip(self, rect, image_count, color_key=None):
        """ Load a whole strip of images, and return them as a list. """
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups, color_key)
