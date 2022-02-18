import pygame as pg
import random

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
            font = pg.font.Font(None, 84)
            t_score = font.render(f"{score}", True, COLOR_FONT_DICT[score])
            t_score_pos = t_score.get_rect(center=(self.rect.size[0] / 2, self.rect.size[1] / 2 + 5))
            self.image = pg.Surface(self.rect.size).convert()
            self.image.fill(COLOR_SCORE_DICT[score])
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


def randscore(score):
    valid_pos = []
    for i in range(4):
        for j in range(4):
            if score[i][j] == 0:
                valid_pos.append((i, j))
    random.shuffle(valid_pos)
    if len(valid_pos) > 0:
        score[valid_pos[0][0]][valid_pos[0][1]] = random.choice([2, 4])
    return score


def updateboard(score, key):
    dscore = 0
    is_move = False
    ktype = 0

    def _update(dscore, is_move):
        for i in range(4):
            for j in range(1, 4):
                if score[i][j] != 0:
                    print(i, j)
                    k = j
                    while k != 0 and score[i][k - 1] == 0:
                        print(f"{(i, k-1, score[i][k-1])} <- {(i, k, score[i][k])}")
                        score[i][k - 1] = score[i][k]
                        score[i][k] = 0
                        k = k-1
                        print(score)
                        if k != 0:
                            print(i, k, score[i][k-1])
                        is_move = True
                    if k != 0 and score[i][k - 1] == score[i][k]:
                        dscore = dscore + score[i][k]
                        score[i][k - 1] *= 2
                        score[i][k] = 0
                        is_move = True

        return dscore, is_move
    def _S():
        pass
    def _T1():
        for i in range(4):
            for j in range(i):
                score[i][j], score[j][i] = score[j][i], score[i][j]
    def _T2():
        for i in range(4):
            for j in range(2):
                score[i][j], score[i][3-j] = score[i][3-j], score[i][j]

    if key == pg.K_a or key == pg.K_LEFT:
        ktype = 0
    elif key == pg.K_w or key == pg.K_UP:
        ktype = 1
    elif key == pg.K_d or key == pg.K_RIGHT:
        ktype = 2
    elif key == pg.K_s or key == pg.K_DOWN:
        ktype = 3

    [_S, _T1][ktype % 2]()
    [_S, _T2][(ktype//2) % 2]()
    dscore, is_move = _update(dscore, is_move)
    [_S, _T2][(ktype//2) % 2]()
    [_S, _T1][ktype % 2]()
    print(ktype)

    return score, is_move, dscore


if __name__ == '__main__':
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

    score = [[0 for j in range(4)] for i in range(4)]
    score = randscore(score)
    score = randscore(score)
    sum_score = 0
    is_end = False

    while not is_end:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN:
                sore, is_move, dscore = updateboard(score, event.key)
                sum_score = sum_score + dscore
                if is_move:
                    sore = randscore(score)

        maxscore = 0
        freecnt = 0

        for i in range(4):
            for j in range(4):
                cell[i][j].set_score(score[i][j])
                maxscore = max(score[i][j], maxscore)
                freecnt = freecnt + (score[i][j] == 0)

        if maxscore == 2048 or freecnt == 0:
            is_end = True

        drawUI()
        font = pg.font.Font(None, 70)
        t_score = font.render(f"SCORE :  {sum_score}", True, COLOR_FONT_DICT[2])
        t_score_pos = t_score.get_rect(center=(screen.get_width() / 2, 90))
        screen.blit(t_score, t_score_pos)
        _cells.draw(screen)
        pg.display.flip()

    pg.quit()
