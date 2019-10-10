#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ----------------------------------------------------------------------
# 定义棋子类型，输赢情况
# ----------------------------------------------------------------------
ARROW = 6
EMPTY = 0
BLACK = 1
WHITE = 2
ERROR = -2



# ----------------------------------------------------------------------
# 定义棋盘类，绘制棋盘的形状，切换先后手，判断输赢等
# ----------------------------------------------------------------------
class ChessBoard(object):
    def __init__(self):
        self.__board = [[EMPTY for n in range(10)] for m in range(10)]
        self.__board[0][3] = BLACK
        self.__board[0][6] = BLACK
        self.__board[3][0] = BLACK
        self.__board[3][9] = BLACK
        self.__board[6][0] = WHITE
        self.__board[6][9] = WHITE
        self.__board[9][3] = WHITE
        self.__board[9][6] = WHITE
        self.__dir = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        #                (左      右)      (上       下)     (左下     右上)      (左上     右下)

    def board(self):  # 返回数组对象
        return self.__board

    def draw_xy(self, x, y, state):  # 获取落子点坐标的状态
        self.__board[x][y] = state

    def get_xy_on_logic_state(self, x, y):  # 获取指定点坐标的状态
        return self.__board[x][y]

    def get_next_xy(self, point, direction):  # 获取指定点的指定方向的坐标
        x = point[0] + direction[0]
        y = point[1] + direction[1]
        if x < 0 or x >= 10 or y < 0 or y >= 10:
            return ERROR
        else:
            return x, y

    def get_xy_on_direction_state(self, point, direction):  # 获取指定点的指定方向的状态
        if point is not False:
            xy = self.get_next_xy(point, direction)
            if xy is not ERROR:
                x, y = xy
                return self.__board[x][y]
        return ERROR


    def reset(self):  # 重置
        self.__board = [[EMPTY for n in range(10)] for m in range(10)]
        self.__board[0][3] = BLACK
        self.__board[0][6] = BLACK
        self.__board[3][0] = BLACK
        self.__board[3][9] = BLACK
        self.__board[6][0] = WHITE
        self.__board[6][9] = WHITE
        self.__board[9][3] = WHITE
        self.__board[9][6] = WHITE

    def anyone_win(self):
        black = []
        white = []
        for i in range(10):  # 找到所有皇后的位置
            for j in range(10):
                if self.__board[i][j] == BLACK:
                    black.append([i, j])
                elif self.__board[i][j] == WHITE:
                    white.append([i, j])
        loss1 = 0
        loss2 = 0
        for directions in self.__dir:  # 对米字的八个方向进行判断是否有下棋的空间
            # print("这里有错")
            for direction in directions:
                # print(direction)
                for a in black:
                    point1 = (a[0], a[1])
                    temple1 = self.get_xy_on_direction_state(point1, direction)
                    # print(temple1)
                    if temple1 != 0:
                        loss1 = loss1 + 1
                        # print("1+%d" % loss1)
                for b in white:
                    point2 = (b[0], b[1])
                    # print(point2)
                    temple2 = self.get_xy_on_direction_state(point2, direction)
                    if temple2 != EMPTY:
                        loss2 = loss2 + 1
                    # print("2+%d"%loss2)
        # print("这里出错！！！ ")
        if loss1 == 32:
            # print("红棋赢")
            return WHITE
        elif loss2 == 32:
            # print("黑棋赢")
            return BLACK
        else:
            return EMPTY

    def add_file_title(self,list):  # 创建一个新的txt文件,并写入己方和对方的名称
            f = open("棋谱.txt", "w+", encoding="utf-8")
            stri = ''
            for i in list:
                stri = stri+i
            f.write(stri+';')
            f.close()

    def save_data(self, r, chess):  # 将数据写入文件
        f = open("棋谱.txt", "a+", encoding="utf-8")
        f.write('\n' + str(r) + ' ')
        if len(chess) == 1:
            f.write(chess[0])
        elif len(chess) == 2:
            f.write(chess[0]+ chess[1])
        elif len(chess) == 3:
            f.write(chess[0]+ chess[1] + '(' + chess[2] + ')')
        elif len(chess) == 4:
            f.write(chess[0]+ chess[1] + '(' + chess[2] + ')' + ' ' + chess[3])
        elif len(chess) == 5:
            f.write(chess[0]+ chess[1] + '(' + chess[2] + ')' + ' ' + chess[3]+ chess[4])
        elif len(chess) == 6:
            f.write(chess[0]+ chess[1] + '(' + chess[2] + ')' + ' ' + chess[3]+ chess[4]+'(' + chess[5] + ')')
        f.close()

    def delete_data(self, list):  # 悔棋
        f = open("棋谱.txt", "w", encoding="utf-8")
        self.add_file_title(list)
        f.write("")
        f.close()

