from pygame import *

import pyganim

from setting import Setting as st
from data import Data


ANIMATION = [('Images/Hero/10.png', 0.1)]


class Hero(sprite.Sprite):
    win = False
    is_die = False
    last_p = 0
    has_key = False
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((st.SIZE, st.SIZE))
        self.image = image.load("Images/Hero/10.png")
        self.rect = Rect(x, y, st.SIZE, st.SIZE)
       # self.boltAnimStay = pyganim.PygAnimation(ANIMATION)
      #  self.boltAnimStay.play()
        #self.boltAnimStay.blit(self.image, (0, 0))

    def update(self, open, vert_move, hor_move):

        if not (hor_move == 0 and vert_move == 0):
            self.image = image.load("Images/Hero/{0}{1}.png".format(hor_move, vert_move))
            self.last_p = 0
            #self.boltAnimStay.blit(self.image, (0, 0))

        if open and self.last_p != 0:
            self.last_p.open(self)

        self.rect.y += vert_move * st.MOVE_SPEED
        #self.collide(0, vert_move, open, platforms)
        self.rect.x += hor_move * st.MOVE_SPEED
        #self.collide(hor_move, 0, open, platforms)
        self.collide(hor_move, vert_move, open)  #

    def collide(self, xvel, yvel, open):
        for p in Data.platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо
                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево
                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top # то не падает вниз
                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх
                if open:
                    p.open(self)
                self.last_p = p

    def die(self):
        pass
        #self.is_die = True
