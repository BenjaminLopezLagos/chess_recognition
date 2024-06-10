# import the opencv library 
import cv2 
from perspective import perspective_change
from piece_detector import get_piece_and_color
from chess_recognition import recognize_board
import numpy as np

def makeGrid(img, rows, cols):
    # Define grid parameters
    height, width, _ = img.shape
    vertical_spacing = width // cols
    horizontal_spacing = height // rows

    # Draw vertical lines
    for i in range(1, cols):
        x = i * vertical_spacing
        cv2.line(img, (x, 0), (x, height), (0, 255, 0), 1)  # Green color

    # Draw horizontal lines
    for j in range(1, rows):
        y = j * horizontal_spacing
        cv2.line(img, (0, y), (width, y), (0, 255, 0), 1)  # Green color
    return img

def main(): 
    # define a video capture object 
    vid = cv2.VideoCapture(0) 
    # dots = [[80, 29], [480, 29], [81, 428], [480, 428]]
    dots = [[230, 83], [560, 83], [230, 412], [560, 412]]
    #dots = [[60, 30], [90, 30], [60, 60], [90, 60]]
    while(True): 
        
        # Capture the video frame 
        # by frame 
        ret, frame = vid.read()
        height, width, channels = frame.shape
        for dot in dots:
            frame = cv2.circle(frame, (dot[0], dot[1]), radius=2, color=(0, 0, 255), thickness=-1)
    
        transformed_frame = perspective_change(frame, dots)
        transformed_frame = cv2.resize(transformed_frame, (1000, 1000), interpolation=cv2.INTER_LINEAR)
        #transformed_frame = cv2.fastNlMeansDenoisingColored(transformed_frame,None,20,20,7,21) 

        
        # Define a sharpening kernel
        sharpening_kernel = np.array([[0, -1, 0],
                                    [-1,  5, -1],
                                    [0, -1, 0]])
        
        # Apply the sharpening kernel to the blurred image
        transformed_frame = cv2.filter2D(transformed_frame, -1, sharpening_kernel)
        #transformed_frame = cv2.flip(transformed_frame, 1)
        transformed_frame = makeGrid(transformed_frame, 8, 8)

        # Display the resulting frame 
        cv2.imshow('frame', frame)
        cv2.imshow('transformed frame', transformed_frame)
        
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('p'):
            recognize_board(transformed_frame)
            #print(get_piece_and_color(perspective_change(frame, dots)))
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()