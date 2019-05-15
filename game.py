import pygame
from pygame import *
import entity.hero as hero_cl
from setting import Setting as st
import building as bld
import game
from data import Data
import camera as camera_cl

import mongo

class Game():
    def __init__(self, screen):
        self.screen = screen

    def start(self, restore):
        Data.objects = pygame.sprite.Group()  # Все объекты
        #Data.platforms = []  # то, во что мы будем врезаться

        bld.build_border()  # Создаем стенку вокруг
        if restore:
            mongo.restore()
        else:
            bld.build_block()  # Создаем блоки
            bld.create_key()
            Data.hero = hero_cl.Hero(st.CENTER_X, st.CENTER_Y)  # создаем героя по (x,y) координатам

        return self.play()  # запускаем игровой процесс


    def play(self):
        hero = Data.hero
        self.screen.fill(st.BACKGROUND_COLOR)

        open = False
        hor_move = vert_mov = 0
        timer = pygame.time.Clock()

        camera = camera_cl.Camera(st.LEVEL_WIDTH, st.LEVEL_HEIGHT)

        hero.is_die, hero.win = False, False
        save_game = False
        while not (hero.is_die or hero.win or save_game):  # Основной цикл программы
            hero.is_die, hero.win = False, False
            timer.tick(10)
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == QUIT:
                    exit(0)
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        save_game = True
                    if e.key == K_SPACE:
                        open = True
                    if e.key == K_RIGHT:
                        hor_move = 1
                        vert_mov = 0
                    elif e.key == K_LEFT:
                        hor_move = -1
                        vert_mov = 0
                    elif e.key == K_UP:
                        vert_mov = -1
                        hor_move = 0
                    elif e.key == K_DOWN:
                        vert_mov = 1
                        hor_move = 0
                if e.type == KEYUP:
                    if e.key == K_SPACE:
                        open = False
                    if e.key == K_LEFT or e.key == K_RIGHT:
                        hor_move = 0
                    if e.key == K_UP or e.key == K_DOWN:
                        vert_mov = 0

            self.screen.fill(st.BACKGROUND_COLOR)

            hero.update(open, vert_mov, hor_move)  # передвижение
            if Data.key:
                Data.key.update(hero)
            if Data.exit:
                Data.exit.go_out(hero)
            for monster in Data.monsters:
                monster.update(hero)
            for monster in Data.super_monsters:
                monster.update(hero)

            camera.update(hero)  # центризируем камеру относительно персонажа
            for e in Data.objects:
                self.screen.blit(e.image, camera.apply(e))
           # entities.draw(screen)  # отображение всего

            pygame.display.update()  # обновление и вывод всех изменений на экран
        timer.tick(5)
        if save_game:
            return 0
        elif hero.win:
            return 1
        elif hero.is_die:
            return -1
        else:
            raise
