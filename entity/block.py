from pygame import *

from setting import Setting as st
from data import Data
from .monster import Monster
from .super_monster import SuperMonster
from .key import Key
from .exit import Exit

PLATFORM_COLOR = "#BDBDBD"


class Block(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((st.SIZE, st.SIZE))
        self.image = image.load("Images/block.png")
        self.rect = Rect(x, y, st.SIZE, st.SIZE)
        Data.objects.add(self)
        Data.platforms.append(self)
        index_x = int((x - st.SIZE_BORDER  ) / st.SIZE)
        index_y = int((y - st.SIZE_BORDER  ) / st.SIZE)
        Data.blocks[index_x][index_y] = self
        self.is_mine = False
        self.is_monster = False
        self.is_super_monster = False
        self.is_key = False
        self.is_exit = False
        self.is_open = False

    def open(self):
        try:
            Data.platforms.remove(self)
            x, y = self.search()
            if self.is_mine:
                self.open_mine(Data.hero)
            elif self.is_monster:
                self.open_monster()
            elif self.is_super_monster:
                self.open_super_monster()
            elif self.is_key:
                self.open_key()
            elif self.is_exit:
                self.open_exit()
            elif (x, y) != (-1, -1):
                num_mine = self.count_number_of_mines_near(x, y)
                if num_mine == 0:
                    self.open_empty()
                else:
                    self.image = image.load("Images/Number/{0}.png".format(num_mine))
            else:
                self.open_empty()
            self.is_open = True
        except:
            pass

    def restore(self):
        if not self.is_open:
            return None
        try:
            Data.platforms.remove(self)
            x, y = self.search()
            if self.is_mine:
                self.open_mine(Data.hero)
            elif self.is_key:
                self.open_key()
            elif self.is_exit:
                self.open_exit()
            elif (x, y) != (-1, -1):
                num_mine = self.count_number_of_mines_near(x, y)
                if num_mine == 0:
                    self.open_empty()
                else:
                    self.image = image.load("Images/Number/{0}.png".format(num_mine))
            else:
                self.open_empty()
            self.is_open = True
        except:
            pass


    def open_mine(self, hero):
        self.image = image.load("Images/mine.png")
        hero.die()

    def open_monster(self):
        Monster(self.rect.x, self.rect.y)
        Data.objects.remove(self)

    def open_super_monster(self):
        SuperMonster(self.rect.x, self.rect.y)
        Data.objects.remove(self)

    def open_key(self):
        key = Key(self.rect.x, self.rect.y)
        Data.objects.remove(self)

    def open_exit(self):
        exit = Exit(self.rect.x, self.rect.y)
        Data.objects.remove(self)

    def open_empty(self):
        self.image = Surface((st.SIZE, st.SIZE))
        self.image.fill(Color(PLATFORM_COLOR))
        Data.objects.remove(self)

    def count_number_of_mines_near(self, x, y):
        num_mine = 0
        try:    # ****-кодские проверки x, y недопускают перескока в разные концы массива
            block = Data.blocks[x - 1][y]
            if x > 0 and (block.is_mine or block.is_monster or block.is_super_monster):
                num_mine += 1
        except:
            pass
        try:
            block = Data.blocks[x + 1][y]
            if x < len(Data.blocks) - 1 and (block.is_mine or block.is_monster or block.is_super_monster):
                num_mine += 1
        except:
            pass
        try:
            block = Data.blocks[x][y - 1]
            if y > 0 and (block.is_mine or block.is_monster or block.is_super_monster):
                num_mine += 1
        except:
            pass
        try:
            block = Data.blocks[x][y + 1]
            if y < len(Data.blocks[0]) - 1 and (block.is_mine or block.is_monster or block.is_super_monster):
                num_mine += 1
        except:
            pass
        return num_mine

    def search(self):
        for x in range(st.NUMBER_COLUMN):
            for y in range(st.NUMBER_ROW):
                if Data.blocks[x][y] == self:
                   return x, y
        return -1, -1

    def is_empty(self):
        return not (self.is_mine or self.is_monster or
         self.is_key or self.is_exit or self.is_open or self.is_super_monster)

    def arrow(self, path):
        self.image = image.load(path)

    def no_arrow(self):
        if not self.is_open:
            self.image = image.load('Images/block.png')
