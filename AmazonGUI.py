#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
from ClosedArea import ClosedArea
from chessboard import ChessBoard

WIDTH = 800
HEIGHT = 540
MARGIN = HEIGHT / 12                     #边缘留余
GRID = HEIGHT / 12                       #方格宽度：45
CHESS_PIECE = 45                         #棋子大小
ARROW_PIECE = 40                         #箭大小
EMPTY = 0
BLACK = 1
WHITE = 2
ARROW = 6
SELECT = 3
SETPIECE = 4
THROW = 5


import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton, QPlainTextEdit, QTextEdit
from PyQt5.QtCore import Qt, QSize, QDateTime
from PyQt5.QtGui import QPixmap, QIcon, QFont

ip = "127.0.0.1"
port = 52052
new_socket = socket.socket()  # 创建 socket 对象
new_socket.connect((ip, port))  # 连接
get_ai_board = [[EMPTY for n in range(10)] for m in range(10)]
back_ai_str = ''
winner = []
ai_down = True  # AI已下棋，主要是为了加锁，当值是False的时候说明AI正在思考，这时候玩家鼠标点击失效，要忽略掉 mousePressEvent
# ----------------------------------------------------------------------
# 定义线程类执行AI的算法
# ----------------------------------------------------------------------
class AI(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(int, int)
    # 构造函数里增加形参
    def __init__(self, board, myturn ,parent=None):
        super(AI, self).__init__(parent)
        self.board = board
        self.turn = myturn

    # 重写 run() 函数
    def run(self):
        send_str = ''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.turn == WHITE:
                    if self.board[i][j] == WHITE:
                        send_str += str(1)
                    elif self.board[i][j] == BLACK:
                        send_str += str(2)
                    else:
                        send_str+= str(self.board[i][j])
                else:
                    send_str += str(self.board[i][j])
        print('转换后发送的棋盘：'+send_str)
        new_socket.send(send_str.encode(encoding='utf-8'))  # 发生数据
        print('AI思考中......')
        global back_ai_str
        back_ai_str = new_socket.recv(4096).decode()  # 结束数据
        print("接收到AI决定：" + back_ai_str)
        self.finishSignal.emit(1, 2)


# ----------------------------------------------------------------------
# 重新定义Label类
# ----------------------------------------------------------------------
class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)     #开启鼠标跟踪

    def enterEvent(self, e):            #未使用：enter点击监听
        e.ignore()


class Amazon(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 初始化棋盘
        self.chessboard = ChessBoard()  # 棋盘类
        self.isclosed = ClosedArea()

        # 设置背景
        self.background = LaBel(self)
        self.background.setPixmap(QPixmap('img/amazon_board.jpg'))
        self.background.setGeometry(0, 0, 540, 540)
        # 固定窗口：800*540
        self.resize(WIDTH, HEIGHT)                          # 固定大小 540*540  窗口可以随着内容自动变化长度
        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))    # 窗口最小的大小
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))    # 窗口最大的大小
        # 窗口初始化
        self.setWindowTitle("东秦晓亚")  # 窗口名称
        self.setWindowIcon(QIcon('img/icon.jpg'))  # 窗口图标

        #比赛信息
        self.info_txv = QLabel(self)
        self.info_txv.setText('比赛信息')
        self.info_txv.setFont(QFont('黑体', 15))
        self.info_txv.resize(100, 50)
        self.info_txv.move(620, 10)

        self.white_txv = QLabel(self)
        self.white_txv.setText('白棋(先手):')
        self.white_txv.setFont(QFont('宋体', 11))
        self.white_txv.resize(100, 50)
        self.white_txv.move(560, 60)

        self.white_edit = QTextEdit(self)
        self.white_edit.resize(140, 28)
        self.white_edit.setFont(QFont('宋体', 11))
        self.white_edit.move(650, 72)

        self.black_txv = QLabel(self)
        self.black_txv.setText('黑棋(后手):')
        self.black_txv.setFont(QFont('宋体', 11))
        self.black_txv.resize(100, 50)
        self.black_txv.move(560, 100)

        self.black_edit = QTextEdit(self)
        self.black_edit.resize(140, 28)
        self.black_edit.setFont(QFont('宋体', 11))
        self.black_edit.move(650, 112)
        self.black_edit.toPlainText()

        self.race_place_txv = QLabel(self)
        self.race_place_txv.setText('比赛地点:')
        self.race_place_txv.setFont(QFont('宋体', 11))
        self.race_place_txv.resize(100, 50)
        self.race_place_txv.move(560, 140)

        self.race_place_edit = QTextEdit(self)
        self.race_place_edit.resize(155, 28)
        self.race_place_edit.setFont(QFont('宋体', 11))
        self.race_place_edit.move(635, 150)
        self.race_place_edit.toPlainText()

        self.race_name_txv = QLabel(self)
        self.race_name_txv.setText('比赛名称:')
        self.race_name_txv.setFont(QFont('宋体', 11))
        self.race_name_txv.resize(100, 50)
        self.race_name_txv.move(560, 175)

        self.race_name_edit = QTextEdit(self)
        self.race_name_edit.resize(155, 28)
        self.race_name_edit.setFont(QFont('宋体', 11))
        self.race_name_edit.move(635, 187)

        self.chess_score_btn = QPushButton(self)  # 将变量初始化为按钮
        self.chess_score_btn.setIcon(QIcon('img/chess_score.png'))
        self.chess_score_btn.setIconSize(QSize(40, 40))
        self.chess_score_btn.resize(50, 50)  # 设置按钮大小
        self.chess_score_btn.move(620, 230)  # 设置按钮在窗口中的位置
        self.chess_score_btn.clicked.connect(self.chess_score)  # clicked。

        # 初始化悔棋Button
        self.regretBtn = QPushButton(self)  # 将变量初始化为按钮
        self.regretBtn.setIcon(QIcon('img/regret.png'))
        self.regretBtn.setIconSize(QSize(40, 40))
        self.regretBtn.resize(50, 50)  # 设置按钮大小
        self.regretBtn.move(560, 230)  # 设置按钮在窗口中的位置
        self.regretBtn.clicked.connect(self.regretGame)  # clicked。

        self.restartBtn = QPushButton(self)
        self.restartBtn.setIcon(QIcon('img/restart.png'))
        self.restartBtn.setIconSize(QSize(40, 40))
        self.restartBtn.resize(50, 50)
        self.restartBtn.move(680, 230)
        self.restartBtn.clicked.connect(self.restart)  # clicked。

        self.select_first_Btn = QPushButton(self)
        self.select_first_Btn.setIcon(QIcon('img/first_go.png'))
        self.select_first_Btn.setIconSize(QSize(40, 40))
        self.select_first_Btn.resize(50, 50)
        self.select_first_Btn.move(740, 230)
        self.select_first_Btn.clicked.connect(self.first_go)  # clicked。

        self.info_button_txv = QLabel(self)
        self.info_button_txv.setText('撤销    保存棋谱    重开    先后手')
        self.info_button_txv.setFont(QFont('宋体', 9))
        self.info_button_txv.resize(230, 15)
        self.info_button_txv.move(572, 285)

        self.commite_btn = QPushButton('提交对手信息', self)
        self.commite_btn.setFont(QFont('黑体', 10))
        self.commite_btn.setIcon(QIcon('img/ok.png'))
        self.commite_btn.setIconSize(QSize(30, 30))
        self.commite_btn.resize(130, 40)
        self.commite_btn.move(610, 320)
        self.commite_btn.clicked.connect(self.commite)  # clicked。

        self.tishi_txv = QLabel(self)
        self.tishi_txv.setText('请选择先后手')
        self.tishi_txv.setFont(QFont('宋体', 12))
        self.tishi_txv.resize(200, 100)
        self.tishi_txv.move(600, 375)

        # 初始化棋子、箭、选择框图片对象
        self.black = QPixmap('img/black.png')       # 将图片转换为Qt对象
        self.white = QPixmap('img/white.png')
        self.arrow = QPixmap('img/arrow.png')
        # 参数初始化
        self.piece_now = WHITE  # 黑棋先行
        self.my_turn = EMPTY   # 玩家先行
        self.x, self.y = 1000, 1000
        self.state = SELECT
        self.select_x, self.select_y = 1000, 1000
        self.setpiece_x,self.setpiece_y = 1000, 1000
        self.record = []
        self.file_title = ['#[AM]', '[先手未定]', '[后手未定]', '[输赢未定]', '[时间 地点]', '[比赛名称]']
        # 选择框标签初始化
        self.start_white_frame = LaBel(self)
        self.start_white_frame.setScaledContents(True)  # 图片大小根据标签大小可变
        self.start_black_frame = LaBel(self)
        self.start_black_frame.setScaledContents(True)  # 图片大小根据标签大小可变
        self.next_white_frame = LaBel(self)
        self.next_white_frame.setScaledContents(True)  # 图片大小根据标签大小可变
        self.next_black_frame = LaBel(self)
        self.next_black_frame.setScaledContents(True)  # 图片大小根据标签大小可变
        self.arrow_white_frame = LaBel(self)
        self.arrow_white_frame.setScaledContents(True)  # 图片大小根据标签大小可变
        self.arrow_black_frame = LaBel(self)
        self.arrow_black_frame.setScaledContents(True)  # 图片大小根据标签大小可变

        self.mouse_point = LaBel(self)  # 将鼠标图片改为棋子

        # 新建棋子标签，准备在棋盘上绘制棋子
        self.pieces = [LaBel(self) for i in range(100)]
        for piece in self.pieces:
            piece.setVisible(True)  # 图片可视
            piece.setScaledContents(True)  # 图片大小根据标签大小可变
        #更新棋盘UI
        self.ui_update(self.chessboard)
        self.mouse_point.raise_()  # 鼠标始终在最上层
        self.setMouseTracking(True)
        self.show()

    def mousePressEvent(self, e):  # 玩家下棋
        if e.button() == Qt.LeftButton and ai_down == True:    #Qt.LeftButton 判断鼠标左键是否按下
            x, y = e.x(), e.y()  #鼠标坐标
            i, j = self.coordinate_transform_pixel2map(x, y)        # 对应棋盘坐标，详见https://blog.csdn.net/weixin_34179968/article/details/86253342
            if not i is None and not j is None:                     # 棋子落在棋盘上，排除边缘，落在边缘为零
                #选择皇后
                if self.state == SELECT and self.my_turn != EMPTY:
                    #判断该位置有棋子
                    if self.chessboard.board()[i][j] == WHITE and self.piece_now == WHITE:
                        self.select_x, self.select_y = i, j
                        #画框
                        m, n = self.coordinate_transform_map2pixel(i, j)
                        self.start_white_frame.setPixmap(QPixmap('img/white_frame.png'))
                        self.start_white_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                        self.next_white_frame.clear()
                        self.arrow_white_frame.clear()
                        self.state = SETPIECE
                        self.record.append(str(chr(self.select_y + 97)) + str(10 - self.select_x))
                        print(str(self.record))
                        print("Select", '——>坐标:', self.select_x, self.select_y, '黑棋')
                    elif self.chessboard.board()[i][j] == BLACK and self.piece_now == BLACK:
                        self.select_x, self.select_y = i, j
                        # 画框
                        m, n = self.coordinate_transform_map2pixel(i, j)
                        self.start_black_frame.setPixmap(QPixmap('img/black_frame.png'))
                        self.start_black_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                        self.next_black_frame.clear()
                        self.arrow_black_frame.clear()
                        print("Select", '——>坐标:', self.select_x, self.select_y, '白棋')
                        self.state = SETPIECE
                        self.record.append(str(chr(self.select_y + 97)) + str(10 - self.select_x))
                        print(str(self.record))
                #移动皇后
                elif self.state == SETPIECE and self.my_turn != EMPTY:
                    # 判断该位置是空
                    if self.chessboard.board()[i][j] == EMPTY:
                        self.setpiece_x, self.setpiece_y = i, j
                        #更新棋子位置
                        self.chessboard.draw_xy(i, j, self.piece_now)
                        # 画框
                        m, n = self.coordinate_transform_map2pixel(i, j)
                        if self.piece_now == WHITE:
                            # 清空之前棋子位置
                            self.chessboard.board()[self.select_x][self.select_y] = EMPTY
                            self.next_white_frame.setPixmap(QPixmap('img/white_frame.png'))
                            self.next_white_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                            print("SetPiece", '——>坐标:', i, j, '白棋')
                        else:
                            # 清空之前棋子位置
                            self.chessboard.board()[self.select_x][self.select_y] = EMPTY
                            self.next_black_frame.setPixmap(QPixmap('img/black_frame.png'))
                            self.next_black_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                            print("SetPiece", '——>坐标:', i, j, '黑棋')
                        self.state = THROW
                        self.record.append(str(chr(self.setpiece_y+97)) + str(10-self.setpiece_x))
                        print(str(self.record))
                    else:
                        print("该位置有棋子或障碍")
                #放箭
                elif self.state == THROW and self.my_turn != EMPTY:
                    #该位置为空
                    if self.chessboard.board()[i][j] == EMPTY:
                        self.chessboard.draw_xy(i, j, ARROW)
                        # 画框
                        m, n = self.coordinate_transform_map2pixel(i, j)
                        if self.piece_now == WHITE:
                            self.arrow_white_frame.setPixmap(QPixmap('img/white_frame.png'))
                            self.arrow_white_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                            print("SetArrow",'——>坐标:', i, j, '白棋')
                            self.piece_now = BLACK

                        else:
                            self.arrow_black_frame.setPixmap(QPixmap('img/black_frame.png'))
                            self.arrow_black_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                            print("SetArrow",'——>坐标:', i, j, '黑棋')
                            self.piece_now = WHITE
                        self.state = SELECT
                        self.record.append(str(chr(j+97)) + str(10-i))
                        print(str(self.record))
                else:
                    QMessageBox.question(self, '提示', '请先选择先后手！', QMessageBox.Yes)
            # 更新UI界面
            self.ui_update(self.chessboard)
            winner = self.chessboard.anyone_win()
            if winner != EMPTY:
                self.gameover(winner)

    # 物理坐标——>逻辑坐标
    def coordinate_transform_map2pixel(self, i, j):
        # 从 chessMap 里的逻辑坐标到 UI 上的绘制坐标的转换
        return  MARGIN + (j+1) * GRID - CHESS_PIECE,MARGIN + (i+1) * GRID - CHESS_PIECE

    # 逻辑坐标——>物理坐标
    def coordinate_transform_pixel2map(self, x, y):
        # 从 UI 上的绘制坐标到 chessMap 里的逻辑坐标的转换
        i, j = int((y - MARGIN) / GRID), int((x - MARGIN) / GRID)
        # 有MAGIN, 排除边缘位置导致 i,j 越界
        if i < 0 or i >= 10 or j < 0 or j >= 10:
            return None, None
        else:
            return i, j

    # 更新UI界面
    def ui_update(self, chessboard):
        # 初始化棋盘棋子
        for i in range(len(chessboard.board())):
            for j in range(len(chessboard.board()[i])):
                if chessboard.board()[i][j] == BLACK:
                    self.pieces[i * 10 + j - 1].setPixmap(self.black)
                    x, y = self.coordinate_transform_map2pixel(i, j)
                    self.pieces[i * 10 + j - 1].setGeometry(x+2, y+3, ARROW_PIECE, ARROW_PIECE)  # 画出棋子
                    chessboard.draw_xy(i, j, BLACK)
                elif chessboard.board()[i][j] == WHITE:
                    self.pieces[i * 10 + j - 1].setPixmap(self.white)
                    x, y = self.coordinate_transform_map2pixel(i, j)
                    self.pieces[i * 10 + j - 1].setGeometry(x+2, y+3, ARROW_PIECE, ARROW_PIECE)  # 画出棋子
                    chessboard.draw_xy(i, j, WHITE)
                elif chessboard.board()[i][j] == ARROW:
                    self.pieces[i * 10 + j - 1].setPixmap(self.arrow)
                    x, y = self.coordinate_transform_map2pixel(i, j)
                    self.pieces[i * 10 + j - 1].setGeometry(x+2, y+2, ARROW_PIECE, ARROW_PIECE)  # 画出棋子
                    chessboard.draw_xy(i, j, ARROW)
                else :
                    self.pieces[i * 10 + j - 1].clear()
                    chessboard.draw_xy(i, j, EMPTY)
        self.update()
    # 悔棋
    def regretGame(self):
        if len(self.record) % 3 == 0 and len(self.record) != 0:  #取消放箭
            pop = self.record.pop()
            self.chessboard.draw_xy(10-int(pop[1:]), ord(pop[0])-97, EMPTY)
            self.ui_update(self.chessboard)
            if self.piece_now == BLACK:
                self.arrow_white_frame.clear()
                self.piece_now = WHITE
            else:
                self.arrow_black_frame.clear()
                self.piece_now = BLACK
            self.state = THROW

            print('取消放箭:'+str(self.record))

        elif len(self.record) %3 == 1 and len(self.record) != 0:   # 取消选择皇后
            pop = self.record.pop()
            # self.chessboard.draw_xy(10 - int(pop[1:]), ord(pop[0]) - 97, EMPTY)
            self.ui_update(self.chessboard)
            if self.piece_now == BLACK:
                self.start_black_frame.clear()
            else:
                self.start_white_frame.clear()
            self.state = SELECT

            print('取消选择皇后'+str(self.record))

        elif len(self.record) %3 == 2 and len(self.record) != 0: # 取消放置皇后
            pop = self.record.pop()
            self.chessboard.draw_xy(10 - int(pop[1:]), ord(pop[0]) - 97, EMPTY)
            if self.piece_now == BLACK:
                self.next_black_frame.clear()
                self.chessboard.draw_xy(10 - int(self.record[-1][1:]), ord(self.record[-1][0]) - 97, self.piece_now)
            else:
                self.next_white_frame.clear()
                self.chessboard.draw_xy(10 - int(self.record[-1][1:]), ord(self.record[-1][0]) - 97, self.piece_now)
            self.state = SETPIECE
            self.ui_update(self.chessboard)
            print('取消放置皇后:'+str(self.record))
        else: #列表为0
            QMessageBox.question(self, '提示', '已经是初始棋局！', QMessageBox.Yes )
        self.chessboard.delete_data(self.file_title)

        # 使用二维数组存储记录
        # self.pieces[self.step].clear()  # 消去棋子的方法，考虑将棋子的标签数扩大
        # 预留接口消去棋盘参数中的相应位置
    # 重开
    def restart(self):
        self.chessboard.reset()
        self.ui_update(self.chessboard)
        # 所有选择框初始化
        self.start_white_frame.clear()
        self.start_black_frame.clear()
        self.next_black_frame.clear()
        self.next_white_frame.clear()
        self.arrow_black_frame.clear()
        self.arrow_white_frame.clear()
        self.tishi_txv.setText('请选择先后手')
        self.piece_now = WHITE  # 黑棋先行
        self.my_turn = EMPTY    # 先手
        self.x, self.y = 1000, 1000
        self.state = SELECT
        self.select_x, self.select_y, self.select_x, self.select_y = 1000, 1000, 1000, 1000
        self.setpiece_x, self.setpiece_y = 1000, 1000
        self.record.clear()
        self.piece_now = WHITE  # 白棋先行
        global get_ai_board
        get_ai_board = [[EMPTY for n in range(10)] for m in range(10)]
        global ai_down
        ai_down = True
        self.white_edit.setReadOnly(False)
        self.black_edit.setReadOnly(False)
        self.race_place_edit.setReadOnly(False)
        self.race_name_edit.setReadOnly(False)
        self.chessboard.delete_data(self.file_title)
        QMessageBox.question(self, '提示', '初始化完成！', QMessageBox.Yes)
    # 确认信息
    def first_go(self):
        reply = QMessageBox.information(self, '选择', '我方AI为先手？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            print('yes')
            self.my_turn = WHITE
            global ai_down
            self.start_ai()
        else:
            print('no')
            global ai_down
            self.my_turn = BLACK
    # 提交对手信息
    def commite(self):
        if self.piece_now == self.my_turn:
            # 开启AI新进程
            global ai_down
            ai_down = False
            self.start_ai()
        else:
            self.tishi_txv.setText('请模仿对手下棋')
            print('对方走子')
    # 保存棋谱
    def chess_score(self):
        self.chessboard.delete_data(self.file_title)
        if self.white_edit.toPlainText() == '' or self.black_edit.toPlainText() == '' or self.race_name_edit.toPlainText() == '' or self.race_place_edit.toPlainText() == '':
            QMessageBox.question(self, '提示', '比赛信息不完整！', QMessageBox.Yes)

        else:
            print('保存棋谱')
            self.white_edit.setReadOnly(True)
            self.black_edit.setReadOnly(True)
            self.race_place_edit.setReadOnly(True)
            self.race_name_edit.setReadOnly(True)
            self.file_title[1] = '[' + self.white_edit.toPlainText() + ']'
            self.file_title[2] = '[' + self.black_edit.toPlainText() + ']'
            timestr = QDateTime.currentDateTime().toString()
            timelist = ['', '', '', '', '', '']
            j = 0
            for i in timestr:
                if i != ' ':
                    timelist[j] = timelist[j] + i
                else:
                    j = j + 1
            # self.file_title[3] = '['+winner+']'
            self.file_title[4] = '[' + timelist[4] + '/' + timelist[1][:len(timelist[1]) - 1] + '/' + timelist[
                2] + ' ' + timelist[3] + ' ' + self.race_place_edit.toPlainText() + ']'
            self.file_title[5] = '[' + self.race_name_edit.toPlainText() + ']'
            print('比赛信息：' + str(self.file_title))
            self.chessboard.add_file_title(self.file_title)
            j = 0
            for i in range(len(self.record)//6):
                self.chessboard.save_data(i+1, self.record[i*6:(i+1)*6])
                j=i
            if len(self.record)% 6 !=0:
                self.chessboard.save_data(j + 2, self.record[(j+1) * 6:])
            QMessageBox.question(self, '提示', '已保存！', QMessageBox.Yes)

    def gameover(self, winner):
        if winner == self.my_turn:
            if self.my_turn == BLACK:
                self.file_title[3] = '后手胜'
            else:
                self.file_title[3] = '先手胜'
            # self.sound_win.play()
            reply = QMessageBox.question(self, '提示', '我方胜利!')
            self.chess_score()
        else:
            # self.sound_defeated.play()
            if self.my_turn == BLACK:
                self.file_title[3] = '[先手胜]'
            else:
                self.file_title[3] = '[后手胜]'
            reply = QMessageBox.question(self, '提示', '我方失败!')
            self.chess_score()

    # 对AI程序返回进行判断
    def AI_draw(self,x, y):
        # 先将 字符串转换成列表
        global get_ai_board
        self.next_white_frame.clear()
        self.arrow_white_frame.clear()
        self.start_white_frame.clear()
        self.start_black_frame.clear()
        self.arrow_black_frame.clear()
        self.next_black_frame.clear()
        str_ai = ''
        print(self.my_turn)
        for i in range(100):

                if self.my_turn == WHITE:

                    if int(back_ai_str[i]) == WHITE:
                        str_ai += str(1)
                    elif int(back_ai_str[i]) == BLACK:
                        str_ai += str(2)
                    else:
                        str_ai += back_ai_str[i]
                else:
                    str_ai += back_ai_str[i]
        print('转换后接收的棋盘:'+str_ai)
        start, end, arrow = [1,2], [1,2], [1,2]
        for i in range(10):
            for j in range(10):
                get_ai_board[i][j] = int(str_ai[i*10+j])
                if get_ai_board[i][j] != self.chessboard.board()[i][j]:

                    m, n = self.coordinate_transform_map2pixel(i, j)
                    # 白方
                    if self.my_turn == WHITE:
                        if self.chessboard.board()[i][j] == WHITE and self.chessboard.board()[i][j] != get_ai_board[i][j]:
                            start = [str(chr(j + 97)), str(10 - i)]
                            print('白棋起点：', start)
                            # self.record.append(str(chr(j + 97)) + str(10 - i))
                            self.start_white_frame.setPixmap(QPixmap('img/white_frame.png'))
                            self.start_white_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                        if get_ai_board[i][j] == WHITE:
                            end = [str(chr(j + 97)), str(10 - i)]
                            print('白棋落点：', end)
                            self.next_white_frame.setPixmap(QPixmap('img/white_frame.png'))
                            self.next_white_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                        elif get_ai_board[i][j] == ARROW:
                            arrow = [str(chr(j + 97)), str(10 - i)]
                            print('箭:', arrow)
                            # self.record.append(str(chr(j + 97)) + str(10 - i))
                            # print(str(self.record))
                            self.arrow_white_frame.setPixmap(QPixmap('img/white_frame.png'))
                            self.arrow_white_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                    # 黑方
                    else:
                        if self.chessboard.board()[i][j] == BLACK and self.chessboard.board()[i][j] != get_ai_board[i][j]:
                            start = [str(chr(j + 97)), str(10 - i)]
                            print('黑棋起点：', start)
                            self.start_black_frame.setPixmap(QPixmap('img/black_frame.png'))
                            self.start_black_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                        elif get_ai_board[i][j] == BLACK:
                            end = [str(chr(j + 97)), str(10 - i)]
                            print('黑棋落点：', end)
                            self.next_black_frame.setPixmap(QPixmap('img/black_frame.png'))
                            self.next_black_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
                        else:
                            arrow = [str(chr(j + 97)), str(10 - i)]
                            print('箭:', arrow)
                            self.arrow_black_frame.setPixmap(QPixmap('img/black_frame.png'))
                            self.arrow_black_frame.setGeometry(m, n, CHESS_PIECE, CHESS_PIECE)
        for i in range(10):
            for j in range(10):
                self.chessboard.board()[i][j] = get_ai_board[i][j]
        self.tishi_txv.setText('请模仿对手下棋')
        self.ui_update(self.chessboard)
        self.record.append(str(start[0])+str(start[1]))
        self.record.append(str(end[0])+str(end[1]))
        self.record.append(str(arrow[0])+str(arrow[1]))

        if back_ai_str[100] == '1':
            print('我方胜利')
            # global winner
            # if self.my_turn == BLACK:
            #     winner = winner + self.black_edit.toPlainText() +'赢'
            # else:
            #     winner = winner + self.white_edit.toPlainText() +'赢'
            self.gameover(self.my_turn)
        elif back_ai_str[100] == '2':
            print('我方失败')
            # if self.my_turn == BLACK:
            #     winner = winner + self.white_edit.toPlainText() +'赢'
            # else:
            #     winner = winner + self.black_edit.toPlainText() +'赢'
            self.gameover(10)
        print(get_ai_board)

    def start_ai(self):
        self.tishi_txv.setText('AI思考中......')
        self.AI = AI(self.chessboard.board(),self.my_turn)  # 新建线程对象，传入棋盘参数
        self.AI.finishSignal.connect(self.AI_draw)  # 结束线程，传出参数
        self.AI.start()  # run
        if self.my_turn == BLACK:
            self.piece_now = WHITE
        else:
            self.piece_now = BLACK
        global ai_down
        ai_down = True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Amazon()
    sys.exit(app.exec_())