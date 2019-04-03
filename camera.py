from pygame import *
import setting

st = setting.Setting()


class Camera(object):

    def __init__(self, width, height):
        self.camera_func = camera_configure
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def reverse(self, pos):  # получение внутренних координат из глобальных
        return pos[0] - self.state.left, pos[1] - self.state.top


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + st.WIN_WIDTH / 2, -t + st.WIN_HEIGHT / 2

    # Ограничения по границам
    l = min(0, l)                            # Не движемся дальше левой
    l = max(-(camera.width - st.WIN_WIDTH), l)    # Не движемся дальше правой
    t = max(-(camera.height - st.WIN_HEIGHT), t)  # Не движемся дальше нижней
    t = min(0, t)                            # Не движемся дальше верхней

    return Rect(l, t, w, h)
