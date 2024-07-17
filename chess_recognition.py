import cv2
import piece_detector
import chess
from stockfish import Stockfish
from itertools import islice

def get_points(img):
    height, width, _ = img.shape

    # Calculate the size of each square
    square_size_width = width // 8
    square_size_height = height // 8

    squares = []
    # Loop over the image and create the squares
    for i in range(8):
        for j in range(8):
            # Calculate the coordinates of the four corners of the square
            top_left = (i * square_size_width, j * square_size_height)
            top_right = ((i + 1) * square_size_width, j * square_size_height)
            bottom_left = (i * square_size_width, (j + 1) * square_size_height)
            bottom_right = ((i + 1) * square_size_width, (j + 1) * square_size_height)
            
            # Add the square to the list
            squares.append([top_left, top_right, bottom_left, bottom_right])    
    return squares

# generates a dict containing a chess positions as key and its piece as value
def generate_board(img):
    if isinstance(img, str) is True:
        img = img = cv2.imread(img)
    img = cv2.resize(img, (1000, 1000))
    squares = get_points(img)
    chess_board_pieces = {}
    chess_board_squares = {}
    cols = list(map(chr, range(ord('a'), ord('h')+1)))
    rows = list(range(1,9))
    row_pos = len(rows) - 1
    col_pos = 0
    for square in squares:
        if row_pos < 0:
            row_pos = len(rows) - 1
            col_pos += 1
        print(square)
        print((row_pos, col_pos))
        
        x_start = square[0][0]
        x_end = square[1][0]
        y_start = square[0][1]
        y_end = square[2][1]
        cropImage = img[ y_start: y_end , x_start: x_end]
        piece = piece_detector.get_piece_and_color(cropImage)
        current_board_position = cols[col_pos] + str(rows[row_pos])
        #chess_board[current_board_position] = cropImage # so i don't have to crop later
        chess_board_pieces[current_board_position] = piece
        chess_board_squares[current_board_position] = [x_start, x_end, y_start, y_end]
        cv2.imwrite('./board_imgs/'+current_board_position+'_boarddd.png', cropImage)

        row_pos -= 1

    return (chess_board_pieces, chess_board_squares)

def chess_row_to_fen(chess_row: list):
    none_count = 0
    fen_list = []
    for i in range(len(chess_row)):
        if chess_row[i] == 'none':
            none_count += 1
        else:
            if none_count > 0:
                fen_list.append(none_count)
                none_count = 0
            fen_list.append(chess_row[i])
    if none_count > 0:
        fen_list.append(none_count)
    return ''.join(map(str, fen_list))

def generate_fen(chess_board: dict, current_turn: str = 'w'):
    fen_rows = []
    cols = list(map(chr, range(ord('a'), ord('h')+1)))
    rows = list(range(1,9))
    rows.sort(reverse=True)

    for row in rows:
        current_row = []
        for col in cols:
            pos = col + str(row)
            current_row.append(chess_board[pos])
        fen_current_row = chess_row_to_fen(current_row)
        fen_rows.append(fen_current_row)

    fen = '/'.join(fen_rows)
    return ' '.join([fen, current_turn])

def get_piece_location_change_from_move(move: str):
    cleaned_move = move
    if len(move) > 4:
        cleaned_move = move[:-1]
    res_first = ''.join(islice(cleaned_move, None, len(cleaned_move) // 2))
    res_second = ''.join(islice(cleaned_move, len(cleaned_move) // 2, None))
    
    move_details = {'from': res_first, 'to': res_second}
    if len(move) > 4:
        move_details['promotion'] = move[-1]

    return move_details

def get_pos_center_coordinates(square_corners, length_px=1000, length_cm=25):
    # para x necesito hacer que la medida sea [-x , 0, +x]
    x = ((square_corners[0] + square_corners[1]) / 2)  - length_px + (length_px / 2)
    y = length_px - ((square_corners[2] + square_corners[3]) / 2)
    center_px = (x, y)
    print(center_px)

    x_cm = (x *  length_cm) / length_px
    y_cm = (y *  length_cm) / length_px
    center_cm = (x_cm, y_cm)
    
    return center_cm

def recognize_board(img, turn='w'):
    #img = cv2.imread(img_path)
    #resized = makeGrid(resized)
    chess_board = generate_board(img)
    board_with_pieces = chess_board[0]
    board_with_coordinates = chess_board[1]

    #current_turn = 'w'

    print('before move')
    fen = generate_fen(board_with_pieces, turn)
    print(fen)
    print(board_with_pieces)
    print(board_with_coordinates)
    print(get_piece_location_change_from_move('d3d4r')) #testing promotions
    board = chess.Board(fen)
    print(board)
    #cv2.imshow("board", resized)
    
    """
    print('after move. now using stockfish')
    stockfish.set_fen_position(board.fen())
    move = stockfish.get_best_move()
    print(move)
    stockfish_move_pos = get_piece_location_change_from_move(move)
    stockfish_from = stockfish_move_pos['from']
    print(get_pos_center_coordinates(board_with_coordinates[stockfish_from])) #testing
    board.push_uci(move)

    print(board)
    print(board.fen())

    print('Legal moves:')
    print(board.legal_moves)
    user_move = input('')
    #board.push_uci(user_move)
    """

    #resized = cv2.line(resized, (0,0), (50,0), color=(160, 42, 240), thickness=5)
    #cv2.imshow("number 1", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows


if __name__ == '__main__':
    img = 'php2JxaUR.png'
    recognize_board(img)
