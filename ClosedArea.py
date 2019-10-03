ARROW = 6
EMPTY = 0
BLACK = 1
WHITE = 2
OK = 3     # 该点可走

class ClosedArea(object):
    def __init__(self):
        self.str_empty = []
        self.stone = []         # 棋子位置
        self.last_stone = []    # 最终封闭的棋子
        self.step = 0
        self.board_char = [[[EMPTY for n in range(10)] for m in range(10)],  [[EMPTY for n in range(10)] for m in range(10)], [[EMPTY for n in range(10)] for m in range(10)], [[EMPTY for n in range(10)] for m in range(10)], [[EMPTY for n in range(10)] for m in range(10)], [[EMPTY for n in range(10)] for m in range(10)], [[EMPTY for n in range(10)] for m in range(10)], [[EMPTY for n in range(10)] for m in range(10)]]  # 8*10*10的八张棋盘
        self.__dir = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        #                (左      右)      (上       下)     (左下     右上)      (左上     右下)

    def is_closed(self, board):
        self.step = 0
        self.stone.clear()
        self.last_stone.clear()
        self.str_empty.clear()
        # 把棋盘解析成只有障碍和空白的棋盘
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == ARROW:     # 所有的箭都置为障碍
                    self.board_char[0][i][j] = ARROW
                    self.board_char[1][i][j] = ARROW
                    self.board_char[2][i][j] = ARROW
                    self.board_char[3][i][j] = ARROW
                    self.board_char[4][i][j] = ARROW
                    self.board_char[5][i][j] = ARROW
                    self.board_char[6][i][j] = ARROW
                    self.board_char[7][i][j] = ARROW
                else:
                    self.board_char[0][i][j] = EMPTY
                    self.board_char[1][i][j] = EMPTY
                    self.board_char[2][i][j] = EMPTY
                    self.board_char[3][i][j] = EMPTY
                    self.board_char[4][i][j] = EMPTY
                    self.board_char[5][i][j] = EMPTY
                    self.board_char[6][i][j] = EMPTY
                    self.board_char[7][i][j] = EMPTY

        # 对棋盘上每个颜色的棋子进行一次位置遍历
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == BLACK or board[i][j] == WHITE:  # 当前为棋子时搜索可走的点
                    self.search(i, j)
                    self.stone.append([board[i][j], i, j])
        return self.get_closed_stone(), self.board_char                 # 对每个棋子与对手棋子进行比较

    # 从某一点进行搜索，返回当前棋子的全部可达点
    def search(self, i, j):
        # 知道当前棋子 坐标、整体局面  求出它能到达的点
        self.str_empty.clear()
        self.str_empty.append([i, j])
        for point in self.str_empty:
            for directions in self.__dir:  # 对米字的八个方向进行判断是否有下棋的空间
                for direction in directions:
                    state, next_x, next_y = self.get_xy_on_direction_state(point, direction)
                    # 查询到该状态为空
                    if state == EMPTY:
                        self.board_char[self.step][next_x][next_y] = OK   #该点设置成可走状态
                        if [next_x, next_y] not in self.str_empty:
                            self.str_empty.append([next_x, next_y])
        self.step += 1

    # 获取某方向点状态
    def get_xy_on_direction_state(self, point, direction):  # 获取指定点的指定方向的状态
        if point is not False:
            xy = self.get_next_xy(point, direction)
            if xy is not False:
                x, y = xy
                return self.board_char[self.step][x][y], x, y
        return 200, 100, 100

    # 获取某方向坐标
    def get_next_xy(self, point, direction):  # 获取指定点的指定方向的坐标
        x = point[0] + direction[0]
        y = point[1] + direction[1]
        if x < 0 or x >= 10 or y < 0 or y >= 10:
            return False
        else:
            return x, y

    # 得到封闭棋子
    def get_closed_stone(self):
        for i in range(8):
            connected = False
            for j in range(8):
                if i != j and self.stone[i][0] != self.stone[j][0]:
                    if connected == False:
                        connected = self.is_connected(self.board_char[j], self.board_char[i])
            if connected == False:
                self.last_stone.append([self.stone[i], i])
        return self.last_stone

    def is_connected(self, a, b):
        for i in range(10):
            for j in range(10):
                if a[i][j] == b[i][j] and a[i][j] == OK and b[i][j] == OK:
                    return True
        return False
