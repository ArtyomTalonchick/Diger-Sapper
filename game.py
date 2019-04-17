import pygame
from pygame import *
import entity.hero as hero_cl
from setting import Setting as st
import building as bld
import game
from data import Data
import camera as camera_cl


class Game():
    def __init__(self, screen):
        self.screen = screen

    def start(self):
        Data.objects = pygame.sprite.Group()  # Все объекты
        Data.platforms = []  # то, во что мы будем врезаться

        bld.build_border()  # Создаем стенку вокруг
        bld.build_block()  # Создаем блоки
        bld.create_key()

        hero = hero_cl.Hero(st.CENTER_X, st.CENTER_Y)  # создаем героя по (x,y) координатам
        Data.objects.add(hero)

        return self.play(hero)  # запускаем игровой процесс


    def play(self, hero):
        self.screen.fill(st.BACKGROUND_COLOR)

        open = False
        hor_move = vert_mov = 0
        timer = pygame.time.Clock()

        camera = camera_cl.Camera(st.LEVEL_WIDTH, st.LEVEL_HEIGHT)

        while not (hero.is_die or hero.win):  # Основной цикл программы
            timer.tick(10)
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == QUIT:
                    exit(0)
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        hero.is_die = True
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

            camera.update(hero)  # центризируем камеру относительно персонажа
            for e in Data.objects:
                self.screen.blit(e.image, camera.apply(e))
           # entities.draw(screen)  # отображение всего

            pygame.display.update()  # обновление и вывод всех изменений на экран
        return hero.win
