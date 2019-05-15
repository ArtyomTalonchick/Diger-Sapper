import pymongo
from data import Data
from entity.block import Block
from setting import Setting as st
import entity.hero as hero_cl
from entity.monster import Monster
from entity.super_monster import SuperMonster


def save():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]#create db
    save_hero(mydb)
    save_blocks(mydb)
    save_monsters(mydb)
    save_super_monsters(mydb)


def restore():
    clear_data();
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]#create db
    restore_hero(mydb)
    restore_blocks(mydb)
    restore_monsters(mydb)
    restore_super_monsters(mydb)

def clear_data():
    Data.restore = False
    Data.hero = None
    Data.blocks = [[None for x in range(st.NUMBER_ROW)] for x in range(st.NUMBER_COLUMN)]
    Data.arrow = []
    Data.platforms = []
    #Data.objects = []
    Data.monsters = []
    Data.super_monsters = []
    Data.key = None
    Data.exit = None


def save_blocks(mydb):
    mycol = mydb["blocks"]#find collection
    mycol.drop()
    mycol = mydb["blocks"]#create collection
    mylist = []
    for blocks in Data.blocks:
        for block in blocks:
            if(not block):
                continue
            mylist.append({"x": block.rect.x, "y": block.rect.y,
                            "is_mine": block.is_mine, "is_monster": block.is_monster,
                            "is_super_monster": block.is_super_monster, "is_key": block.is_key,
                            "is_exit": block.is_exit, "is_open": block.is_open,})
    if mylist:
        return mycol.insert_many(mylist)

def restore_blocks(mydb):
    mycol = mydb["blocks"] #create collection
    mylist = mycol.find()
    for data_block in mylist:
        block = Block(data_block["x"], data_block["y"])
        block.is_mine = data_block["is_mine"]
        block.is_monster = data_block["is_monster"]
        block.is_super_monster = data_block["is_super_monster"]
        block.is_key = data_block["is_key"]
        block.is_exit = data_block["is_exit"]
        block.is_open = data_block["is_open"]
    for blocks in Data.blocks:
        for block in blocks:
            if(not block):
                continue
            elif block.is_open:
                block.restore()
                #block.open()



def save_hero(mydb):
    mycol = mydb["hero"]#find collection
    mycol.drop()
    mycol = mydb["hero"]#create collection
    hero = Data.hero
    mydict = {"x": hero.rect.x, "y": hero.rect.y,
                    "has_key": hero.has_key}
    return mycol.insert_one(mydict)

def restore_hero(mydb):
    mycol = mydb["hero"] #create collection
    data_hero = mycol.find_one()
    Data.hero = hero_cl.Hero(data_hero["x"], data_hero["y"])  # создаем героя по (x,y) координатам
    Data.hero.has_key = data_hero["has_key"]


def save_monsters(mydb):
    mycol = mydb["monsters"]#find collection
    mycol.drop()
    mycol = mydb["monsters"]#create collection
    mylist = []
    for monster in Data.monsters:
        mylist.append({"x": monster.rect.x, "y": monster.rect.y})
    if mylist:
        return mycol.insert_many(mylist)

def restore_monsters(mydb):
    mycol = mydb["monsters"] #create collection
    mylist = mycol.find()
    for data_monster in mylist:
        monster = Monster(data_monster["x"], data_monster["y"])


def save_super_monsters(mydb):
    mycol = mydb["super_monsters"]#find collection
    mycol.drop()
    mycol = mydb["super_monsters"]#create collection
    mylist = []
    for super_monsters in Data.super_monsters:
        mylist.append({"x": super_monsters.rect.x, "y": super_monsters.rect.y})
    if mylist:
        return mycol.insert_many(mylist)

def restore_super_monsters(mydb):
    mycol = mydb["super_monsters"] #create collection
    mylist = mycol.find()
    for data_super_monsters in mylist:
        super_monsters = SuperMonster(data_super_monsters["x"], data_super_monsters["y"])


def save_settings():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]#create db
    mycol = mydb["settings"]#find collection
    mycol.drop()
    mycol = mydb["settings"]#create collection
    mydict = {"SIZE_BORDER": st.SIZE_BORDER, "SIZE": st.SIZE,
                "NUMBER_ROW": st.NUMBER_ROW, "NUMBER_COLUMN": st.NUMBER_COLUMN,
                "LEVEL_HEIGHT": st.LEVEL_HEIGHT, "LEVEL_WIDTH": st.LEVEL_WIDTH,
                "WIN_HEIGHT": st.WIN_HEIGHT, "WIN_WIDTH": st.WIN_WIDTH,
                "MOVE_SPEED": st.MOVE_SPEED, "BACKGROUND_COLOR": st.BACKGROUND_COLOR,
                "DENSITY_MINES": st.DENSITY_MINES, "DENSITY_MONSTERS": st.DENSITY_MONSTERS,
                "DENSITY_SUPERMONSTERS": st.DENSITY_SUPERMONSTERS }
    return mycol.insert_one(mydict)

def restore_settings():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["settings"]
    data_st = mycol.find_one()
    st.SIZE_BORDER = data_st["SIZE_BORDER"]
    st.SIZE = data_st["SIZE"]
    st.NUMBER_ROW = data_st["NUMBER_ROW"]
    st.NUMBER_COLUMN = data_st["NUMBER_COLUMN"]
    st.LEVEL_HEIGHT = data_st["LEVEL_HEIGHT"]
    st.LEVEL_WIDTH = data_st["LEVEL_WIDTH"]
    st.WIN_HEIGHT = data_st["WIN_HEIGHT"]
    st.WIN_WIDTH = data_st["WIN_WIDTH"]
    st.MOVE_SPEED = data_st["MOVE_SPEED"]
    st.BACKGROUND_COLOR = data_st["BACKGROUND_COLOR"]
    st.DENSITY_MINES = data_st["DENSITY_MINES"]
    st.DENSITY_MONSTERS = data_st["DENSITY_MONSTERS"]
    st.DENSITY_SUPERMONSTERS = data_st["DENSITY_SUPERMONSTERS"]
