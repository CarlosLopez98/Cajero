import pygame

pygame.init()
font = pygame.font.Font(None, 40)


class Globe:
    pygame.init()

    def __init__(self, data: str, pos, rad):
        self.x, self.y = pos
        self.rad = rad
        self.data = data
        self.text = font.render(self.data, False, (0, 0, 0))

    def render(self, surface):
        pygame.draw.circle(surface, '#FFFFFF', (self.x + self.rad, self.y + self.rad), self.rad)
        pygame.draw.circle(surface, '#000000', (self.x + self.rad, self.y + self.rad), self.rad, 3)
        surface.blit(self.text, (self.x + 20, self.y + 20))

    def change_data(self, data: str):
        self.data = data
        self.text = font.render(self.data, False, (0, 0, 0))
