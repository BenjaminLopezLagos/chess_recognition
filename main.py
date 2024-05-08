import cv2
import piece_detector

def makeGrid(img):
    for i in range(9):
        img = cv2.line(img, (0, i*50), (400,i*50), color=(160, 42, 240), thickness=1)
        img = cv2.line(img, (i*50, 0), (i*50, 400), color=(160, 42, 240), thickness=1)
        print(i)
    return img

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

# generates a dict containing a chess positions as key and its respective coordinates as value
def generate_board(squares, img):
    chess_board = {}
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
        piece = piece_detector.predict_piece(cropImage)
        current_board_position = cols[col_pos] + str(rows[row_pos])
        #chess_board[current_board_position] = cropImage # so i don't have to crop later
        chess_board[current_board_position] = piece
        #cv2.imwrite('./board_imgs/'+current_board_position+'_board.png', cropImage)

        row_pos -= 1

    return chess_board

#only works on a single row
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

def generate_fen(chess_board: dict):
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

    return '/'.join(fen_rows)


def main():
    path = 'tableronnmnm.png'
    img = cv2.imread(path)
    resized = cv2.resize(img, (960, 960))
    #resized = makeGrid(resized)
    squares = get_points(resized)
    chess_board = generate_board(squares, resized)

    fen = generate_fen(chess_board)
    print(fen)
    print(len(squares))
    print(chess_board)
    #resized = cv2.line(resized, (0,0), (50,0), color=(160, 42, 240), thickness=5)
    #cv2.imshow("number 1", img)
    cv2.imshow("board", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows


if __name__ == '__main__':
    main()
