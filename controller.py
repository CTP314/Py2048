from queue import Empty
import random

class GameController():
    def __init__(self) -> None:
        self._board = [[0 for j in range(4)] for i in range(4)]
        self._maxscore = 0
        self._totscore = 0
        self._round = 0
        self.__createNewCell()
        self.__createNewCell()

    def __createNewCell(self) -> bool:
        valid_pos = []
        for i in range(4):
            for j in range(4):
                if self._board[i][j] == 0:
                    valid_pos.append((i, j))
        if valid_pos is Empty:
            return False
        nx, ny = random.choice(valid_pos)
        self._board[nx][ny] = random.choice([2, 4])
        self._maxscore = max(self._maxscore, self._board[nx][ny])
        return True

    def __runLeft(self) -> bool:
        is_move = False
        for i in range(4):
            last = -1
            for j in range(1, 4):
                if self._board[i][j] != 0:
                    k = j
                    while k != 0 and self._board[i][k - 1] == 0:
                        self._board[i][k - 1] = self._board[i][k]
                        self._board[i][k] = 0
                        k = k-1
                        is_move = True
                    if k != 0 and self._board[i][k - 1] == self._board[i][k] and last != k-1:
                        self._board[i][k - 1] *= 2
                        self._board[i][k] = 0
                        self._totscore = self._totscore + self._board[i][k - 1]
                        self._maxscore = max(self._maxscore, self._board[i][k - 1])
                        is_move = True
        return is_move

    def __T1(self, flag) -> None:
        if flag:
            for i in range(4):
                for j in range(i):
                    self._board[i][j], self._board[j][i] = self._board[j][i], self._board[i][j]

    def __T2(self, flag) -> None:
        if flag:
            for i in range(4):
                for j in range(2):
                    self._board[i][j], self._board[i][3-j] = self._board[i][3-j], self._board[i][j]

    def isEnd(self) -> bool:
        for i in range(4):
            for j in range(4):
                if self._board[i][j] == 0:
                    return False
                if j != 0 and self._board[i][j-1] == self._board[i][j]:
                    notfree = False
                if i != 0 and self._board[i-1][j] == self._board[i][j]:
                    notfree = False
        return True

    def run(self, action):
        if action in [0, 1, 2, 3]:
            self.__T1(action % 2)
            self.__T2((action // 2) % 2)
            is_move = self.__runLeft()
            self.__T2((action // 2) % 2)
            self.__T1(action % 2)
            if is_move:
                self._round = self._round + 1
                self.__createNewCell()
        return self._board, self._totscore, self.isEnd()

    def restart(self) -> None:
        self._board = [[0 for j in range(4)] for i in range(4)]
        self._maxscore = 0
        self._totscore = 0
        self._round = 0
        self.__createNewCell()
        self.__createNewCell()