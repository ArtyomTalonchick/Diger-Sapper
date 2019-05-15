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

FONT_SIZE = 100
COLOR = (27, 94, 32)
COLOR_SELECTED = (225, 0, 0)
START_X = st.WIN_WIDTH / 2 -200

MENU = ['Start', 'Settings', 'About', 'Exit']


class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.current = 0
        self.update_text()


    def main_menu(self):
        global MENU
        self.game = Game(self.screen)
        sc = self.screen
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                exit(0)
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    if MENU == ['Start', 'Settings', 'About', 'Exit']:
                        exit()
                    else:
                        MENU = ['Start', 'Settings', 'About', 'Exit']
                elif e.key == K_UP:
                    self.current -= 1
                elif e.key == K_DOWN:
                    self.current += 1
                elif e.key == K_RETURN:
                    selected_text = MENU[self.current]
                    if selected_text == 'Start':
                        self.start()
                    elif selected_text == 'Continue':
                        self.start_game(True)
                    elif selected_text == 'New game':
                        self.start_game(False)
                    elif selected_text == 'Settings':
                        self.settings()
                    elif selected_text == 'About':
                        self.about()
                    elif selected_text == 'Exit':
                        exit()
        self.current %= len(MENU)
        self.update_text()
        pygame.display.update()

    def update_text(self):
        self.screen.fill(st.BACKGROUND_COLOR)
        for i in range(len(MENU)):
            text_str = MENU[i]
            if i == self.current:
                text = self.font.render(text_str, 1, COLOR_SELECTED)
            else:
                text = self.font.render(text_str, 1, COLOR)
            self.screen.blit(text, (self.get_start_x_y(text_str)[0], (i + 1) * 110))

    def start(self):
        global MENU
        MENU = ['Continue', 'New game']

    def start_game(self, restore):
        self.game = Game(self.screen)
        result = self.game.start(restore)
        self.show_result(result)
        MENU = ['Start', 'Settings', 'About', 'Exit']

    def show_result(self, result):
        self.screen.fill(st.BACKGROUND_COLOR)
        if result == 0:
            mongo.save()
            result_text = 'Game saved'
            color = (104, 184, 216)
        elif result == 1:
            result_text = 'You win!)'
            color = (64, 211, 31)
        elif result == -1:
            result_text = 'You lose((('
            color = (225, 0, 0)
        text = self.font.render(result_text, 1, color)
        self.screen.blit(text, self.get_start_x_y(result_text))
        pygame.display.update()
        self.wait()

    def about(self):
        self.screen.fill(st.BACKGROUND_COLOR)
        font = pygame.font.Font(None, 30)
        text_str = "This is the best game calls Digger-Sapper)"
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
        label = Label(root, text='Settings will start working in the new game')
        label.place(x=50, y=20)

        label_1 = Label(root, text='Manster 1:')
        label_1.place(x=100, y=60)
        w1 = Scale(root, from_=1, to=99, orient=HORIZONTAL)
        w1.set(100 - st.DENSITY_MONSTERS)
        w1.place(x=200, y=50)

        label_2 = Label(root, text='Manster 2:')
        label_2.place(x=100, y=110)
        w2 = Scale(root, from_=1, to=99, orient=HORIZONTAL)
        w2.set(100 - st.DENSITY_SUPERMONSTERS)
        w2.place(x=200, y=100)

        label_3 = Label(root, text='Mine:')
        label_3.place(x=100, y=160)
        w3 = Scale(root, from_=1, to=99, orient=HORIZONTAL)
        w3.set(100 - st.DENSITY_MINES)
        w3.place(x=200, y=150)

        btn = Button(text="Ok", command=lambda: self.get_setting(w1, w2, w3, root))
        btn.place(x=250, y=200)

        root.mainloop()

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
