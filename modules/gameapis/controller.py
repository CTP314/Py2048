from queue import Empty
import numpy as np
import copy
import random

class GameController():
    def __init__(self) -> None:
        self._board = [[0 for j in range(4)] for i in range(4)]
        self._maxscore = 0
        self._totscore = 0
        self._round = 0
        self._action_space = [0, 1, 2, 3]
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

    def __checkLeft(self, board):
        for i in range(4):
            last = -1
            for j in range(1, 4):
                if board[i][j] != 0:
                    k = j
                    while k != 0 and board[i][k - 1] == 0:
                        board[i][k - 1] = board[i][k]
                        board[i][k] = 0
                        k = k - 1
                        return True
                    if k != 0 and board[i][k - 1] == board[i][k] and last != k-1:
                        board[i][k - 1] *= 2
                        board[i][k] = 0
                        return True
        return False

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
                        k = k - 1
                        is_move = True
                    if k != 0 and self._board[i][k - 1] == self._board[i][k] and last != k-1:
                        self._board[i][k - 1] *= 2
                        self._board[i][k] = 0
                        self._totscore = self._totscore + self._board[i][k - 1]
                        self._maxscore = max(self._maxscore, self._board[i][k - 1])
                        is_move = True
        return is_move

    def __T1(self, board, flag) -> None:
        if flag:
            for i in range(4):
                for j in range(i):
                    board[i][j], board[j][i] = board[j][i], board[i][j]
        return board

    def __T2(self, board, flag) -> None:
        if flag:
            for i in range(4):
                for j in range(2):
                    board[i][j], board[i][3-j] = board[i][3-j], board[i][j]
        return board

    def isEnd(self) -> bool:
        for i in range(4):
            for j in range(4):
                if self._board[i][j] == 0:
                    return False
                if j != 0 and self._board[i][j-1] == self._board[i][j]:
                    return False
                if i != 0 and self._board[i-1][j] == self._board[i][j]:
                    return False
        return True

    def get_valid_actions(self):
        actions = []
        for action in [0, 1, 2, 3]:
            board = copy.deepcopy(self._board)
            board = self.__T1(board, action % 2)
            board = self.__T2(board, (action // 2) % 2)
            if self.__checkLeft(board):
                actions.append(action)
        if len(actions) == 0:
            actions = [0]
        return actions

    def run(self, action):
        if type(action) is not int:
            action = np.argmax(action)
        if action in [0, 1, 2, 3]:
            self._board = self.__T1(self._board, action % 2)
            self._board = self.__T2(self._board, (action // 2) % 2)
            is_move = self.__runLeft()
            self._board = self.__T2(self._board, (action // 2) % 2)
            self._board = self.__T1(self._board, action % 2)
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