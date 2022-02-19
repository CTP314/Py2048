import pygame as pg
import random
import controller

COLOR_DICT = {"background": (250, 248, 238, 1), "container": (187, 173, 160, 1),
              "grid": (205, 193, 180, 1), }
COLOR_SCORE_DICT = {2: (238, 228, 218, 1), 4: (237, 224, 200, 1), 8: (242, 177, 121, 1),
                    16: (245, 149, 99, 1), 32: (246, 124, 95, 1), 64: (246, 94, 59, 1),
                    128: (237, 207, 114, 1), 256: (234, 204, 97, 1), 512: (237, 200, 80),
                    1024: (237, 197, 63, 1), 2048: (237, 194, 46, 1)}
COLOR_FONT_DICT = {2: (119, 110, 101, 1), 4: (119, 110, 101, 1), 8: (249, 246, 242, 1),
                   16: (249, 246, 242, 1), 32: (249, 246, 242, 1), 64: (249, 246, 242, 1),
                   128: (249, 246, 242, 1), 256: (249, 246, 242, 1), 512: (249, 246, 242, 1),
                   1024: (249, 246, 242, 1), 2048: (249, 246, 242, 1)}
container = pg.Rect((0, 0), (450, 450))
grid = pg.Rect((0, 0), (97.5, 97.5))


class Cell(pg.sprite.Sprite):
    def __init__(self, center=(0, 0)):
        super(Cell, self).__init__()
        self.rect = grid.copy()
        self.rect.center = center
        self.origin_rect = self.rect
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill(COLOR_DICT["grid"])
        self.score = 0

    def set_score(self, score):
        self.score = score
        if score != 0:
            font = pg.font.Font(None, 70)
            t_score = font.render(f"{score}", True, COLOR_FONT_DICT[min(score, 2048)])
            t_score_pos = t_score.get_rect(center=(self.rect.size[0] / 2, self.rect.size[1] / 2 + 5))
            self.image = pg.Surface(self.rect.size).convert()
            self.image.fill(COLOR_SCORE_DICT[min(score, 2048)])
            self.image.blit(t_score, t_score_pos)
        else:
            self.image = pg.Surface(self.rect.size).convert()
            self.image.fill(COLOR_DICT["grid"])


def drawUI():
    screen.blit(background, (0, 0))
    pg.draw.rect(background, COLOR_DICT["container"], container, border_radius=6)
    for i in range(4):
        for j in range(4):
            grid.center = s_center[0] + 109.5 * i, s_center[1] + 109.5 * j
            pg.draw.rect(background, COLOR_DICT["grid"], grid, border_radius=3)

def getActionFromKey(key):
    if key == pg.K_a or key == pg.K_LEFT:
        return 0
    elif key == pg.K_w or key == pg.K_UP:
        return 1
    elif key == pg.K_d or key == pg.K_RIGHT:
        return 2
    elif key == pg.K_s or key == pg.K_DOWN:
        return 3
    return -1


if __name__ == '__main__':
    py2048 = controller.GameController()
    pg.init()
    screen = pg.display.set_mode((530, 630), pg.SCALED)
    pg.display.set_caption("2048")
    pg.mouse.set_visible(True)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(COLOR_DICT["background"])

    if pg.font:
        pass

    container.center = screen.get_width() / 2, screen.get_height() * (1 - 3 / 100) - 225

    # center-(225, 225)+(97.5, 97.5)/2+(12, 12)
    s_center = (container.center[0] - 164.25, container.center[1] - 164.25)
    cell = [[Cell((s_center[0] + 109.5 * j, s_center[1] + 109.5 * i)) for j in range(4)] for i in range(4)]
    _cells = pg.sprite.RenderPlain()

    clock = pg.time.Clock()

    for i in range(4):
        for j in range(4):
            _cells.add(cell[i][j])

    totscore = 0
    is_end = False

    while not is_end:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN:
                _, totscore, is_end = py2048.run(getActionFromKey(event.key))

        for i in range(4):
            for j in range(4):
                cell[i][j].set_score(py2048._board[i][j])

        drawUI()
        font = pg.font.Font(None, 70)
        t_score = font.render(f"SCORE :  {totscore}", True, COLOR_FONT_DICT[2])
        t_score_pos = t_score.get_rect(center=(screen.get_width() / 2, 90))
        screen.blit(t_score, t_score_pos)
        _cells.draw(screen)
        pg.display.flip()

    pg.quit()
