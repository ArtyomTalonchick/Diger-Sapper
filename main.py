import pygame
from pygame import *
import entity.hero as hero_cl
from setting import Setting as st
import building as bld
from data import Data
from menu import Menu


def main():
    pygame.init()  # Инициация PyGame
    screen = pygame.display.set_mode((st.WIN_WIDTH, st.WIN_HEIGHT))  # Создаем окно
    pygame.display.set_caption("Diger-saper")  # Пишем в шапку

    menu = Menu(screen)
    while True:
        menu.main_menu()

if __name__ == "__main__":
    main()
