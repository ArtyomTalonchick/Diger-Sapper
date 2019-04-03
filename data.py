from setting import Setting as st
from enum import Enum

#def init():
 #   global blocks
  #  blocks = [[None for x in range(st.NUMBER_ROW)] for x in range(st.NUMBER_COLUMN)]

class Data:
    blocks = [[None for x in range(st.NUMBER_ROW)] for x in range(st.NUMBER_COLUMN)]
    arrow = []
    platforms = []
    objects = []
    monsters = []
    key = None
    exit = None
