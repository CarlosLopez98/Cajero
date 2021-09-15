import json
from random import choice
from spritesheet import SpriteSheet
from globe import Globe
from random import randint

# We get all the data from the json file
with open('characters.json') as file:
    sprites_data = json.load(file)
file.close()


class Character:
    """ Represents a character. """

    def __init__(self, pos=(0, 0), scale=None):
        self.image = 0
        self.rect = None
        self.x, self.y = pos
        self.char = choice(list(sprites_data.items()))[1]
        self.rects = self.get_rects(self.char['frames'])
        self.sprite_sheet = SpriteSheet(f'res/{self.char["filename"]}', scale)
        self.images = self.sprite_sheet.images_at(self.rects, -1)
        self.walk = False
        self.goal_pos = None
        self.vel = 4

        self.attending = False
        # bills
        self.bills = randint(1, 20)  # Random number of bills that the person has to pay

        # Globe for number of bills
        self.globe = Globe(str(self.bills), (self.x, self.y), 30)

    def render(self, surface):
        image = self.images[self.image // 60]
        self.rect = image.get_rect()
        self.rect.topleft = self.x, self.y
        surface.blit(image, self.rect)

        self.globe.x, self.globe.y = self.x, self.y - 30 * 2
        self.globe.render(surface)

    def move(self):
        self.image += 1
        if self.image == 360:
            self.image = 0
        if self.image % 3 == 0:
            self.x += self.vel

    def stop(self):
        self.image = 1

    def get_pos(self) -> tuple:
        return self.x, self.y

    def get_rects(self, rects: dict):
        return [(rect['x'], rect['y'], rect['w'], rect['h']) for rect in rects.values()]

    def pay_bill(self):
        self.bills -= 1
        self.globe.change_data(str(self.bills))
