import pygame
from pygame import *
import entity.hero as hero_cl
from setting import Setting as st
import building as bld
from game import Game
from data import Data
import camera as camera_cl

FONT_SIZE = 100
COLOR = (27, 94, 32)
COLOR_SELECTED = (225, 0, 0)
START_X = st.WIN_WIDTH / 2 - 100

MENU = ['Start', 'Settings', 'About', 'Exit']


class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.current = 0
        self.update_text()
        self.game = Game(self.screen)


    def main_menu(self):
        sc = self.screen
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                exit(0)
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    exit()
                elif e.key == K_UP:
                    self.current -= 1
                elif e.key == K_DOWN:
                    self.current += 1
                elif e.key == K_RETURN:
                    selected_text = MENU[self.current]
                    if selected_text == 'Start':
                        win = self.game.start()
                        self.show_result(win)
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
            if i == self.current:
                text = self.font.render(MENU[i], 1, COLOR_SELECTED)
            else:
                text = self.font.render(MENU[i], 1, COLOR)
            self.screen.blit(text, (START_X, (i + 1) * 110))

    def show_result(self, win):
        self.screen.fill(st.BACKGROUND_COLOR)
        if win:
            result_text = 'You win!)'
            color = (255, 16, 00)
        else:
            result_text = 'You lose((('
            color = (109, 76, 65)
        text = self.font.render(result_text, 1, color)
        self.screen.blit(text, (START_X, st.WIN_HEIGHT / 2))
        pygame.display.update()
        self.wait()

    def about(self):
        self.screen.fill(st.BACKGROUND_COLOR)
        font = pygame.font.Font(None, 30)
        text = font.render("This is the best game calls Digger-Sapper)", 1, (200, 16, 00))
        self.screen.blit(text, (START_X, st.WIN_HEIGHT / 2))
        pygame.display.update()
        self.wait()

    def settings(self):
        pass

    def wait(self):
        wait = True
        while wait:
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == QUIT:
                    exit(0)
                if e.type == KEYDOWN:
                    if e.key == K_RETURN or e.key == K_ESCAPE:
                        wait = False
