from pygame import *
from data import Data
from setting import Setting as st

PLATFORM_COLOR = "#212121"


class Border(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((st.SIZE_BORDER, st.SIZE_BORDER))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, st.SIZE_BORDER, st.SIZE_BORDER)
        Data.objects.add(self)
        Data.platforms.append(self)

    def open(self, hero):
        pass
