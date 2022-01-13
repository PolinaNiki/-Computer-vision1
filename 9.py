import random
import cv2
import numpy as np


def get_range(color_name):
    
    color_ranges = {
        'yellow':   ([15, 120, 85], [40, 255, 255]),
        'green':    ([65, 135, 55], [85, 255, 255]),
        'blue':     ([95, 165, 90], [105, 255, 255])
    }

    (lower, upper) = color_ranges[color_name]

    return (
        np.array(lower, dtype="uint8"), 
        np.array(upper, dtype="uint8")
    )

def get_pos(img, ball):
    
    (lower, upper) = get_range(ball)
    mask = cv2.dilate(
        cv2.erode(
            cv2.inRange(img, lower, upper), 
            None, 
            iterations=2
        ), 
        None, 
        iterations=2
    )

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
    if len(contours) > 0:
        biggest = max(contours, key=cv2.contourArea)
        (ball_x, ball_y), radius = cv2.minEnclosingCircle(biggest)
        if radius > 15:
            cv2.circle(image, (int(ball_x), int(ball_y)), int(radius), (255, 255, 255), 3)
        else:
            ball_x = None
    else:
        ball_x = None

    return ball_x

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

balls = ["blue", "green", "yellow"]
balls_out = balls.copy()
balls_pos = [None, None, None]
random.shuffle(balls)
random.shuffle(balls_out)

while cam.isOpened():
    
    ret, image = cam.read()
    image_blur = cv2.GaussianBlur(image, (11, 11), 0)
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)

    if (
        (balls_pos[0] is not None) and 
        (balls_pos[1] is not None) and 
        (balls_pos[2] is not None) and 
        (balls_pos[0] < balls_pos[1] < balls_pos[2])
    ):
        cv2.putText(image, "You won", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (40, 40, 40), 1, cv2.LINE_8)
    else:
        for (i, ball) in enumerate(balls):
            balls_pos[i] = get_pos(image_hsv, ball)
            cv2.putText(image, f"Show the balls in your own order (try to guess) {' '.join(balls_out)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (40, 40, 40), 1, cv2.LINE_8)
    
    cv2.imshow("Camera", image)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()