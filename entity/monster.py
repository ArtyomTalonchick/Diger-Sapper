from pygame import *
import time

from setting import Setting as st
from data import Data

sign = lambda x: x and (1, -1)[x < 0]

class Monster(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.is_alive = False
        self.PATH_IMAGE = "Images/monster.png"
        self.MOVE_SPEED = 8
        self.SLEEP_TIME = 2
        self.image = Surface((st.SIZE, st.SIZE))
        self.image = image.load(self.PATH_IMAGE)
        self.rect = Rect(x, y, st.SIZE, st.SIZE)
        self.start_time = int(round(time.time()))
        Data.monsters.append(self)
        Data.objects.add(self)

    def update(self, hero):
        if(int(round(time.time())) - self.start_time < self.SLEEP_TIME):
            return

        hor_move = sign(hero.rect.x - self.rect.x)
        vert_move = sign(hero.rect.y - self.rect.y)

        if not (hor_move == 0 and vert_move == 0):
            self.image = image.load(self.PATH_IMAGE)
            self.last_p = 0

        self.rect.y += vert_move * self.MOVE_SPEED
        self.collide(0, vert_move, hero)
        self.rect.x += hor_move * self.MOVE_SPEED
        self.collide(hor_move, 0, hero)

    def collide(self, xvel, yvel, hero):
        if sprite.collide_rect(self, hero):
            hero.die()
        for p in Data.platforms:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                if yvel < 0:
                    self.rect.top = p.rect.bottom

    def alive(self):
        pass
        self.is_alive = True
