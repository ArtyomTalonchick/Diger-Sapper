import pygame
from pygame import *
import entity.hero as hero_cl
from setting import Setting as st
import building as bld
from game import Game
from data import Data
import camera as camera_cl
from tkinter import *
import mongo
import ml

FONT_SIZE = 100
COLOR = (27, 94, 32)
COLOR_SELECTED = (225, 0, 0)
START_X = st.WIN_WIDTH / 2 -200


MENU_MAIN_RU = ['Старт', 'Настройки', 'Описание', 'Выйти']
MENU_MAIN_EN = ['Start', 'Settings', 'About', 'Exit']
MENU_MAIN = MENU_MAIN_EN if st.LOCALIZATION == 'EN' else MENU_MAIN_RU

MENU_START_RU = ['Продолжить', 'Новая игра']
MENU_START_EN = ['Continue', 'New game']
MENU_START = MENU_START_EN if st.LOCALIZATION == 'EN' else MENU_START_RU

MENU = MENU_MAIN

DICT_EN = {'game_saved': 'Game saved', 'you_win': 'You win!', 'you_lose': 'You lose(',
            'about': 'This is the best game calls Digger-Sapper)',
            'setting': 'Settings will start working in the new game',
            'monster': 'Monster', 'mine': 'Mine'}
DICT_RU = {'game_saved': 'Игра сохранена', 'you_win': 'Вы выиграли!', 'you_lose': 'Вы проиграли(',
            'about': 'Это лучшая игра под названием Digger-Sapper)',
            'setting': 'Настройки начнут действовать в новой игре',
            'monster': 'Монстор', 'mine': 'Мина'}
DICT = DICT_EN if st.LOCALIZATION == 'EN' else DICT_RU


class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.game = Game(self.screen)
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.current = 0
        self.localization()
        self.update_text()


    def main_menu(self):
        global MENU
        sc = self.screen
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                exit(0)
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    if MENU == MENU_MAIN:
                        exit()
                    else:
                        MENU = MENU_MAIN
                elif e.key == K_UP:
                    self.current -= 1
                elif e.key == K_DOWN:
                    self.current += 1
                elif e.key == K_RETURN:
                    selected_text = MENU[self.current]
                    if selected_text == MENU_MAIN[0]:
                        self.start()
                    elif selected_text == MENU_START[0]:
                        self.start_game(True)
                    elif selected_text == MENU_START[1]:
                        self.start_game(False)
                    elif selected_text == MENU_MAIN[1]:
                        self.settings()
                    elif selected_text == MENU_MAIN[2]:
                        self.about()
                    elif selected_text == MENU_MAIN[3]:
                        exit()
        self.current %= len(MENU)
        self.update_text()
        pygame.display.update()

    def update_text(self):
        self.screen.fill(st.BACKGROUND_COLOR)
        bg = pygame.image.load("Images/menu.png")
        self.screen.blit(bg, (0, 0))
        for i in range(len(MENU)):
            text_str = MENU[i]
            if i == self.current:
                text = self.font.render(text_str, 1, COLOR_SELECTED)
            else:
                text = self.font.render(text_str, 1, COLOR)
            self.screen.blit(text, (self.get_start_x_y(text_str)[0], (i + 1) * 110))

    def start(self):
        global MENU
        MENU = MENU_START

    def show_predict(self):
        self.screen.fill(st.BACKGROUND_COLOR)

        pred_rbf, pred_lin = ml.predict()
        pred_rbf = "RBF: " + str(pred_rbf)
        pred_lin = "Linear: " + str(pred_lin)
        text = self.font.render(pred_rbf, 1, (104, 14, 216))
        self.screen.blit(text, (self.get_start_x_y(pred_rbf)[0], 200))
        text = self.font.render(pred_lin, 1, (10, 190, 100))
        self.screen.blit(text, (self.get_start_x_y(pred_lin)[0], 400))

        pygame.display.update()
        self.wait()

    def start_game(self, restore):
        self.show_predict()
        result = self.game.start(restore)
        if result == 1:
            ml.push(0)
        elif result == -1:
            ml.push(100)
        self.show_result(result)
        MENU = MENU_MAIN

    def show_result(self, result):
        self.screen.fill(st.BACKGROUND_COLOR)
        mongo.save()
        if result == 0:
            result_text = DICT['game_saved']
            color = (104, 184, 216)
        elif result == 1:
            result_text = DICT['you_win']
            color = (64, 211, 31)
        elif result == -1:
            result_text =  DICT['you_lose']
            color = (225, 0, 0)
        text = self.font.render(result_text, 1, color)
        self.screen.blit(text, self.get_start_x_y(result_text))
        pygame.display.update()
        self.wait()


    def about(self):
        self.screen.fill(st.BACKGROUND_COLOR)
        font = pygame.font.Font(None, 30)
        text_str = DICT['about']
        width, height = font.size(text_str)
        text = font.render(text_str, 1, (200, 16, 00))
        self.screen.blit(text, ((st.WIN_WIDTH - width) / 2, (st.WIN_HEIGHT - height) / 2))
        pygame.display.update()
        self.wait()


    def settings(self):
        root = Tk()
        root.title('Settings')
        root.geometry('450x300')
        root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
        label = Label(root, text=DICT['setting'])
        label.place(x=50, y=20)

        label_1 = Label(root, text=DICT['monster'] + '1:')
        label_1.place(x=100, y=60)
        w1 = Scale(root, from_=1, to=99, orient=HORIZONTAL)
        w1.set(100 - st.DENSITY_MONSTERS)
        w1.place(x=200, y=50)

        label_2 = Label(root, text=DICT['monster'] + '2:')
        label_2.place(x=100, y=110)
        w2 = Scale(root, from_=1, to=99, orient=HORIZONTAL)
        w2.set(100 - st.DENSITY_SUPERMONSTERS)
        w2.place(x=200, y=100)

        label_3 = Label(root, text=DICT['mine'] + ':')
        label_3.place(x=100, y=160)
        w3 = Scale(root, from_=1, to=99, orient=HORIZONTAL)
        w3.set(100 - st.DENSITY_MINES)
        w3.place(x=200, y=150)

        btn = Button(text="Ok", command=lambda: self.get_setting(w1, w2, w3, root))
        btn.place(x=200, y=200)

        loc_btn = Button(text=st.LOCALIZATION, command=lambda: self.localization())
        loc_btn.place(x=250, y=200)

        root.mainloop()

    def localization(self):
        global MENU, MENU_MAIN, MENU_MAIN_EN, MENU_MAIN_RU, MENU_START, MENU_START_EN, MENU_START_RU, DICT, DICT_EN, DICT_RU
        if st.LOCALIZATION == 'EN':
            st.LOCALIZATION = 'RU'
            MENU_MAIN = MENU_MAIN_RU
            MENU_START = MENU_START_RU
            DICT = DICT_RU
        else:
            st.LOCALIZATION = 'EN'
            MENU_MAIN = MENU_MAIN_EN
            MENU_START = MENU_START_EN
            DICT = DICT_EN
        MENU = MENU_MAIN

    def get_setting(self, w1, w2, w3, root):
        st.DENSITY_MONSTERS = 100 - w1.get()
        st.DENSITY_SUPERMONSTERS = 100 - w2.get()
        st.DENSITY_MINES = 100 - w3.get()
        mongo.save_settings()
        root.destroy()

    def wait(self):
        wait = True
        while wait:
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == QUIT:
                    exit(0)
                if e.type == KEYDOWN:
                    if e.key == K_RETURN or e.key == K_ESCAPE:
                        wait = False

    def get_start_x_y(self, text):
        width, height = self.font.size(text)
        return (st.WIN_WIDTH - width) / 2, (st.WIN_HEIGHT - height) / 2
