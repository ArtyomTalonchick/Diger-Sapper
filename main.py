# Импортируем библиотеку pygame
import pygame
from pygame import *
import hero as hero_cl
from setting import Setting as st
import building as bld
import game
from data import Data

gm = game.Game()

def main():
    pygame.init()  # Инициация PyGame
    screen = pygame.display.set_mode((st.WIN_WIDTH, st.WIN_HEIGHT))  # Создаем окно
    pygame.display.set_caption("Name of my game")  # Пишем в шапку

    while True:
        Data.objects = pygame.sprite.Group()  # Все объекты
        Data.platforms = []  # то, во что мы будем врезаться

        bld.build_border()  # Создаем стенку вокруг
        bld.build_block()  # Создаем блоки
        bld.create_key()

        hero = hero_cl.Hero(st.CENTER_X, st.CENTER_Y)  # создаем героя по (x,y) координатам
        Data.objects.add(hero)

        gm.play(screen, hero)  # запускаем игровой процесс

        f1 = pygame.font.Font(None, 100)
        text1 = f1.render('Restart?', 1, (27, 94, 32))
        screen.blit(text1, (200, 200))

        pygame.display.update()  # обновление и вывод всех изменений на экран

        wait = True
        while wait:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == KEYDOWN:
                    if e.key == K_RETURN:
                        wait = False
                    if e.key == K_ESCAPE:
                        exit()

if __name__ == "__main__":
    main()
