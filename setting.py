class Setting:
    SIZE_BORDER = 16
    SIZE = 64
    NUMBER_ROW = 20
    NUMBER_COLUMN = 32
    LEVEL_HEIGHT = SIZE * NUMBER_ROW + 2 * SIZE_BORDER
    LEVEL_WIDTH = SIZE * NUMBER_COLUMN + 2 * SIZE_BORDER
    WIN_HEIGHT = 720
    WIN_WIDTH = 1080
    CENTER_X = SIZE_BORDER + SIZE * int(NUMBER_COLUMN / 2)
    CENTER_Y = SIZE_BORDER + SIZE * int(NUMBER_ROW / 2)
    MOVE_SPEED = 64
    BACKGROUND_COLOR = (189, 189, 189)
    DENSITY_MINES = 15
    DENSITY_MONSTERS = 15
    DENSITY_SUPERMONSTERS = 1
