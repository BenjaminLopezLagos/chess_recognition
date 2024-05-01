import cv2

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

def generate_fen_string(chess_board):
    pass

def main():
    chess_cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] 
    chess_rows = list(range(1,9))
    chess_board = {}
    path = 'board.jpg'
    img = cv2.imread(path)
    resized = cv2.resize(img, (400, 400))
    resized = makeGrid(resized)
    squares = get_points(resized)

    row_pos = len(chess_rows) - 1
    col_pos = 0
    for square in squares:
        if row_pos < 0:
            row_pos = len(chess_rows) - 1
            col_pos += 1
        print(square)
        print((row_pos, col_pos))
        x_start = square[0][0]
        x_end = square[1][0]
        y_start = square[0][1]
        y_end = square[2][1]
        cropImage = resized[ y_start: y_end , x_start: x_end] 

        current_board_position = chess_cols[col_pos] + str(chess_rows[row_pos])
        #chess_board[current_board_position] = cropImage # so i don't have to crop later
        chess_board[current_board_position] = square # stores coordinates but i have to crop the image
        #cv2.imwrite('./board_imgs/'+current_board_position+'_board.png', cropImage)

        row_pos -= 1

    print(len(squares))
    print(chess_board)
    #resized = cv2.line(resized, (0,0), (50,0), color=(160, 42, 240), thickness=5)
    #cv2.imshow("number 1", img)
    cv2.imshow("number 1 resized", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows


if __name__ == '__main__':
    main()
