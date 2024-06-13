import os
import cv2
import numpy as np

from src.Server.Camera.Calibration import CalibrateCamera
from src.Server.Components.BallDetection import DetectBall
from src.Server.Components.EggDetection import DetectEgg
from src.Server.Components.RobotDetection import DetectRobot

#just a change to test git
# Get the current directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Provide the correct full path to the image file
image_path = os.path.join(script_dir, '..', 'Images', 'Robot_green.jpg')

# image_path = os.path.join(os.getcwd(), 'Images', 'test1.jpg')
# Load the image
frame = cv2.imread(image_path)

# Check if the image is loaded successfully
if frame is None:
    print(f"Error: Unable to load the image from '{image_path}'.")
else:
    new_frame = CalibrateCamera(frame)


    balls = DetectBall(frame)
    egg = DetectEgg(frame)
    robot_contour = DetectRobot(frame)
    # Draw the bounding rectangle on the original image
    if robot_contour is not None:
        cv2.drawContours(frame, [robot_contour], -1, (0, 255, 0), 2)
        for contour in robot_contour:
            for point in contour:
                x, y = point
                print(f"Green point: ({x}, {y})")

    # If balls are found, draw them on the image
    if balls is not None:
        balls = np.uint16(np.around(balls))
        print("Ball Coordinates:")
        for i, circle in enumerate(balls[0, :]):
            # Draw the outer circle
            cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
            # Draw the center of the circle
            cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)

            label_position = (circle[0] - 10, circle[1] - 10)
            cv2.putText(frame, "ball", label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            x, y, radius = circle
            print(f"Center coordinates: ({x}, {y}), Radius: {radius}")

    # If eggs are found, draw them on the image
    if egg is not None:
        egg = np.uint16(np.around(egg))
        print("Egg Coordinates:")
        for i, circle in enumerate(egg[0, :]):
            # Draw the outer circle
            cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
            # Draw the center of the circle
            cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)

            label_position = (circle[0] - 10, circle[1] - 10)
            cv2.putText(frame, "Egg", label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            x, y, radius = circle
            print(f"Center coordinates: ({x}, {y}), Radius: {radius}")



    # Display the image with detected circles and contours
    cv2.imshow('Objects Detected', frame)
    cv2.imshow('Undistorted', new_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()