from pygame import *

import random
from entity.block import Block
from entity.border import Border
from setting import Setting as st
from data import Data


def build_border():
    for y in range(int(st.LEVEL_HEIGHT / st.SIZE_BORDER)):
        Border(0, y * st.SIZE_BORDER)
        Border(st.LEVEL_WIDTH - st.SIZE_BORDER, y * st.SIZE_BORDER)
    for x in range(int(st.LEVEL_WIDTH / st.SIZE_BORDER)):
        Border(x * st.SIZE_BORDER, 0)
        Border(x * st.SIZE_BORDER, st.LEVEL_HEIGHT - st.SIZE_BORDER)


def build_block():
    for x in range(st.NUMBER_COLUMN):
        for y in range(st.NUMBER_ROW):
            if not (x == st.NUMBER_COLUMN / 2 and y == st.NUMBER_ROW / 2):
                block = Block(st.SIZE_BORDER + st.SIZE * x, st.SIZE_BORDER + st.SIZE * y)
                if not random.randint(0, st.DENSITY_MINES) and block.is_empty():
                    block.is_mine = True
                elif not random.randint(0, st.DENSITY_MONSTERS) and block.is_empty():
                    block.is_monster = True
                elif not random.randint(0, st.DENSITY_SUPERMONSTERS) and block.is_empty():
                    block.is_super_monster = True
                Data.blocks[x][y] = block


def search_empty_block():
    x, y = random.randint(0, st.NUMBER_COLUMN - 1), random.randint(0, st.NUMBER_ROW - 1)
    while not Data.blocks[x][y].is_empty():
        x, y = random.randint(0, st.NUMBER_COLUMN - 1), random.randint(0, st.NUMBER_ROW - 1)
    return x, y


def create_arrows(x, y):
    for _x in range(st.NUMBER_COLUMN):
        create_arrow(Data.blocks[_x][y], "Images/horizontal.png")
    for _y in range(st.NUMBER_ROW):
        create_arrow(Data.blocks[x][_y], "Images/vertical.png")


def create_arrow(block, path):
    if not random.randint(0, 10) and block.is_empty():
        block.arrow(path)
        Data.arrow.append(block)


def create_key():
    x, y = search_empty_block()
    Data.blocks[x][y].is_key = True
    create_arrows(x, y)


def create_exit():
    x, y = search_empty_block()
    Data.blocks[x][y].is_exit = True
    create_arrows(x, y)
