# import the opencv library 
import cv2 
from perspective import perspective_change
from piece_detector import get_piece_and_color
from chess_recognition import recognize_board

def main(): 
    # define a video capture object 
    vid = cv2.VideoCapture(0) 
    dots = [[80, 29], [480, 29], [81, 428], [480, 428]]
    while(True): 
        
        # Capture the video frame 
        # by frame 
        ret, frame = vid.read()
        height, width, channels = frame.shape
        print((height, width))
        for dot in dots:
            frame = cv2.circle(frame, (dot[0], dot[1]), radius=1, color=(0, 0, 255), thickness=-1)
    
        transformed_frame = perspective_change(frame, dots)
        transformed_frame = cv2.resize(transformed_frame, (960, 960))
        # Display the resulting frame 
        cv2.imshow('frame', frame)
        cv2.imshow('transformed frame', transformed_frame)
        
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            recognize_board(transformed_frame)
            #print(get_piece_and_color(perspective_change(frame, dots)))
            break
    
    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()