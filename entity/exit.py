from pygame import *
from data import Data
from setting import Setting as st

class Exit(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((st.SIZE, st.SIZE))
        self.image = image.load("Images/exit.png")
        self.rect = Rect(x, y, st.SIZE, st.SIZE)
        Data.objects.add(self)
        Data.exit = self

    def go_out(self, hero):
        if sprite.collide_rect(self, hero):
            hero.win = True
