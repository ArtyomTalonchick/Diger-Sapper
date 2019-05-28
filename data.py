from setting import Setting as st
from enum import Enum

#def init():
 #   global blocks
  #  blocks = [[None for x in range(st.NUMBER_ROW)] for x in range(st.NUMBER_COLUMN)]


class Data:
    hero = None
    blocks = [[None for x in range(st.NUMBER_ROW)] for x in range(st.NUMBER_COLUMN)]
    arrow = []
    platforms = []
    objects = []
    monsters = []
    super_monsters = []
    key = None
    exit = None
    machine_learning_x = None
    machine_learning_y = None
    machine_learning_n = None
