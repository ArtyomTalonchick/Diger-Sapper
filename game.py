import pygame
from pygame import *

import camera as camera_cl
from setting import Setting as st
from data import Data


class Game():
    def play(self, screen, hero):
        bg = Surface((st.WIN_WIDTH, st.WIN_HEIGHT))  # Создание видимой поверхности
        bg.fill(Color(st.BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

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
                        exit()
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
            screen.blit(bg, (0, 0))  # Заливаем экран

            hero.update(open, vert_mov, hor_move)  # передвижение
            if Data.key:
                Data.key.update(hero)
            if Data.exit:
                Data.exit.go_out(hero)
            for monster in Data.monsters:
                monster.update(hero)

            camera.update(hero)  # центризируем камеру относительно персонажа
            for e in Data.objects:
                screen.blit(e.image, camera.apply(e))
           # entities.draw(screen)  # отображение всего

            pygame.display.update()  # обновление и вывод всех изменений на экран
