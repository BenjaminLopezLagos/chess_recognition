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
import serial
import time

#ser = serial.Serial('COM3', 9600, timeout=1)  # Adjust the port as needed
#time.sleep(2)  # Wait for the connection to establish


def take_picture(camera: int = 1): # it uses an external camera by default but you can change it here
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
            take_picture()
            self.detected_board = chess_recognition.generate_board('scanned_board.png')
            fen = chess_recognition.generate_fen(self.detected_board[0], 'w')
            self.load_image_from_fen(fen)
        else:
            self.make_move()

    def check_win_state(self, board):
        # Check if the game ended after player's move
        if board.is_checkmate():
            self.cpu_move_details_lbl.setText("Checkmate! You win!")
            return True
        if board.is_stalemate():
            self.cpu_move_details_lbl.setText("Stalemate! The game is a draw.")
            return True
        if board.is_insufficient_material():
            self.cpu_move_details_lbl.setText("Draw due to insufficient material.")
            return True
        if board.is_fifty_moves():
            self.cpu_move_details_lbl.setText("Draw due to the fifty-move rule.")
            return True
        if board.is_repetition():
            self.cpu_move_details_lbl.setText("Draw due to threefold repetition.")
            return True
        
        return False

    def make_move(self):
        # player's turn 
        take_picture()
        self.detected_board = chess_recognition.generate_board('scanned_board.png')
        board_with_coordinates = self.detected_board[1]
        fen = chess_recognition.generate_fen(self.detected_board[0], 'w')
        self.load_image_from_fen(fen)
        move = ''
        board = chess.Board(fen)
        if self.check_win_state is True:
            return
        # CPU does its turn
        fen = chess_recognition.generate_fen(self.detected_board[0], 'b') #inmediately switch to cpu after the player finishes their turn
        self.bot.set_fen_position(board.fen())
        try:
            move = self.bot.get_best_move()
            ##### try adding a popup message here ######
        except:
            print('The CPU tried to do an invalid move.')
            return
        move_details = chess_recognition.get_piece_location_change_from_move(move)
        stockfish_from = move_details['from']
        stockfish_to = move_details['to']
        self.cpu_move_details_lbl.setText(json.dumps(move_details))
        # these are the coordinates for the piece that the arm has to move, as indicated by a1 and a2.
        print(chess_recognition.get_pos_center_coordinates(board_with_coordinates[stockfish_from])) #a1
        print(chess_recognition.get_pos_center_coordinates(board_with_coordinates[stockfish_to])) #a2
        ####### put arm movement here #######
        '''
        # Send the command to the Arduino
        ser.write(b'run_function\n')

        # Wait for the Arduino to signal completion
        while True:
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                if response == "done":
                    print("Arduino function execution completed.")
                    break
        '''
        take_picture()
        self.detected_board = chess_recognition.generate_board('scanned_board.png')
        fen = chess_recognition.generate_fen(self.detected_board[0], 'b')
        self.load_image_from_fen(fen)
        board = chess.Board(fen)
        if self.check_win_state is True:
            return
        #

if __name__ == "__main__":
    dots = camera_setup.main(0) # change the value in () so you can use an usb webcam.
    print(dots)
    print(camera_setup.dots)
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())




