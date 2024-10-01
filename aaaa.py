import cv2
import os
from datetime import datetime

# Create the specific folder if it doesn't exist
folder_name = "captured_images"
os.makedirs(folder_name, exist_ok=True)

# Start the webcam
cap = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Webcam Feed', frame)

    # Check if 's' is pressed to take a snapshot
    if cv2.waitKey(1) & 0xFF == ord('s'):
        # Generate a unique filename with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = os.path.join(folder_name, f"image_{timestamp}.png")
        
        # Save the image
        cv2.imwrite(file_path, frame)
        print(f"Image saved at: {file_path}")

    # Check if 'q' is pressed to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
