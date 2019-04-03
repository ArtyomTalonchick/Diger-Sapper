from pygame import *
import time

from setting import Setting as st
from data import Data
from monster import Monster

sign = lambda x: x and (1, -1)[x < 0]

class SuperMonster(Monster):
    def __init__(self, x, y):
        Monster.__init__(self, x, y)
        self.PATH_IMAGE = "Images/superMonster.png"
        self.image = image.load(self.PATH_IMAGE)
        self.MOVE_SPEED = 1
        self.SLEEP_TIME = 2

    def collide(self, xvel, yvel, hero):
        pass
