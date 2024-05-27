import cv2
import numpy as np

def perspective_change(img, points):
    height, width = img.shape[:2]
    points = np.float32(points)
    new_shape = np.float32([[0,0], [width,0], [0,height], [width,height]])
    #for i in range(0, 4):
        #cv2.circle(img, (int(points[i][0]), int(points[i][1])), 7, (0,0,255), cv2.FILLED)
    matrix = cv2.getPerspectiveTransform(points, new_shape)
    output = cv2.warpPerspective(img, matrix, (width,height))
    
    return output

"""
img = cv2.imread("resized.jpg")
points = np.float32([[63,40], [332,41], [12,275], [387,275]])

cv2.imshow("funcion", perspective_change(img, points))
cv2.waitKey(0)

cv2.imshow("original", img)
cv2.waitKey(0)
"""