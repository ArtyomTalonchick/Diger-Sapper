from pygame import *
from data import Data
import building as bld
from setting import Setting as st

class Key(sprite.Sprite):
    is_owned_by_hero = False
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((st.SIZE, st.SIZE))
        self.image = image.load("Images/key.png")
        self.rect = Rect(x, y, st.SIZE, st.SIZE)
        Data.objects.add(self)
        Data.key = self

    def update(self, hero):
        if sprite.collide_rect(self, hero):
            self.image = image.load("Images/key_small.png")

        if not hero.has_key and sprite.collide_rect(self, hero):
            hero.has_key = True
            self.image = image.load("Images/key_small.png")
            for block in Data.arrow:
                block.no_arrow()
            bld.create_exit()

        if hero.has_key:
            self.rect.x = hero.rect.x
            self.rect.y = hero.rect.y
            #Data.objects.remove(self)
