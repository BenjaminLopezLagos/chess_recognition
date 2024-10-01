import sys
import PIL.Image
from PyQt6.QtGui import QPixmap, QImage, QFont
from PyQt6.QtWidgets import QApplication, QLabel, QTextEdit, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QThread, pyqtSignal as Signal, pyqtSlot as Slot
import cv2
import chess
import chess.svg
import cairo
from PIL import Image, ImageDraw, ImageFont, ImageQt
import requests
import chess_recognition
from stockfish import Stockfish
import numpy as np
import json
import camera_setup

def take_picture(camera: int = 1):
    vid = cv2.VideoCapture(camera)
    current_frame = 0
    while(current_frame < 90):
        ret, frame = vid.read()
        current_frame += 1
    transformed_frame = camera_setup.perspective_change(frame, camera_setup.dots)
    transformed_frame = cv2.resize(transformed_frame, (1000, 1000), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite('scanned_board.png', transformed_frame)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.detected_board = ({}, {})

        self.bot = Stockfish("notebook using stockfish/stockfish/stockfish-windows-x86-64-avx2.exe")
        self.bot.set_depth(20)#How deep the AI looks
        self.bot.set_skill_level(20)#Highest rank stockfish
        self.bot.get_parameters()
        
        self.game_begin = False
        self.current_player = 'w'

        self.VBL = QVBoxLayout()

        self.board_lbl = QLabel()
        self.VBL.addWidget(self.board_lbl)

        self.insert_move_lbl = QTextEdit()
        self.VBL.addWidget(self.insert_move_lbl)

        self.make_turn_btn = QPushButton("Make Turn")
        self.make_turn_btn.clicked.connect(self.go_to_next_game_state)
        self.VBL.addWidget(self.make_turn_btn)
        
        self.cpu_move_details_lbl = QLabel()
        self.VBL.addWidget(self.cpu_move_details_lbl)

        self.setLayout(self.VBL)


    def load_image_from_fen(self, fen):
        #self.board = chess.Board(fen)
        url = f'https://chess-board.fly.dev/?fen={fen}&size=600&theme=default&frame=false&piece=cburnett'
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            with open('test.png', 'wb') as f:
                for chunk in response:
                    f.write(chunk)
        img = Image.open('test.png')
        qimg = ImageQt.ImageQt(img)
        self.board_lbl.setPixmap(QPixmap.fromImage(qimg))

    def go_to_next_game_state(self):
        fen = ''
        if self.game_begin is False:
            self.game_begin = True 
            '''
            ### This block is simulating taking a picture and scanning the board in its starting position ###
            fen = f'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR {self.current_player}' #starting_fen
            url = f'https://chess-board.fly.dev/?fen={fen}&size=600&theme=default&frame=false&piece=cburnett'
            print(url)
            response = requests.get(url)
            if response.status_code == 200:
                with open('test.png', 'wb') as f:
                    for chunk in response:
                        f.write(chunk)
            ### End simulation block ###
            '''
            take_picture()
            self.detected_board = chess_recognition.generate_board('scanned_board.png')
            fen = chess_recognition.generate_fen(self.detected_board[0], self.current_player)
            self.load_image_from_fen(fen)
        else:
            self.make_move()

    def make_move(self):
        player = self.current_player
        next_player = ''
        board_with_coordinates = self.detected_board[1]
        fen = chess_recognition.generate_fen(self.detected_board[0], player)
        move = ''
        board = chess.Board(fen)

        if player == 'b':
            self.bot.set_fen_position(board.fen())
            move = self.bot.get_best_move()
            move_details = chess_recognition.get_piece_location_change_from_move(move)
            stockfish_from = move_details['from']
            stockfish_to = move_details['to']
            self.cpu_move_details_lbl.setText(json.dumps(move_details))
            print(chess_recognition.get_pos_center_coordinates(board_with_coordinates[stockfish_from]))
            print(chess_recognition.get_pos_center_coordinates(board_with_coordinates[stockfish_to]))
            next_player = 'w' #change to human player
        if player == 'w':
            move = self.insert_move_lbl.toPlainText()
            next_player = 'b' #change to cpu player
            
        #board.push_uci(move) #reminder: move to player == b when this uses a camera
        print(board.fen())
        
        '''
        ### This block is simulating taking a picture and scanning the board after a move ###
        url = f'https://chess-board.fly.dev/?fen={board.fen()}&size=600&theme=default&frame=false&piece=cburnett'
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            with open('test.png', 'wb') as f:
                for chunk in response:
                    f.write(chunk)
        ### End simulation block ###
        '''
        take_picture()
        self.detected_board = chess_recognition.generate_board('scanned_board.png')
        fen = chess_recognition.generate_fen(self.detected_board[0], next_player)
        self.load_image_from_fen(fen)
        self.current_player = next_player

if __name__ == "__main__":
    dots = camera_setup.main(1)
    print(dots)
    print(camera_setup.dots)
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())