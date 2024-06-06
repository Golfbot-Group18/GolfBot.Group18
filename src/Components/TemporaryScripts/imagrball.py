import os
import cv2
import numpy as np

# Get the current directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Provide the correct full path to the image file
image_path = os.path.join(script_dir, '..', 'Data', 'Images', 'test1.jpg')
# Load the image
img = cv2.imread(image_path)


# Function to detect red areas in the image
def detect_red(image):
    # Define the lower and upper bounds for the red color in HSV color space
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Apply morphological operations to remove noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Adjust the area threshold as needed
            cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)

    return image


# Function to detect eggs in the image
def detect_eggs(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Threshold the image to obtain binary image
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the grayscale image
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if len(contour) >=5:
            ellipsis=cv2.fitEllipse(contour)
            cv2.ellipse(image,ellipsis,(255,0,0),2)

            # Label the contour as "egg"
            label_position = (int (ellipsis[0][0]), int(ellipsis[0][1]))
            cv2.putText(image, "egg", label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return image


# Check if the image is loaded successfully
if img is None:
    print(f"Error: Unable to load the image from '{image_path}'.")
else:
    # Detect red areas in the image
    img_with_red = detect_red(img)

    # Detect eggs in the image
    img_with_eggs = detect_eggs(img.copy())

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Use Hough Circle Transform to detect circles
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=10,
        maxRadius=50
    )

    # If circles are found, draw them on the image
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i, circle in enumerate(circles[0, :]):
            # Draw the outer circle
            cv2.circle(img_with_red, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
            # Draw the center of the circle
            cv2.circle(img_with_red, (circle[0], circle[1]), 2, (0, 0, 255), 3)

            label_position = (circle[0] - 10, circle[1] - 10)
            cv2.putText(img_with_red, "ball", label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the image with circles and detected red areas
    cv2.imshow('Objects Detected', np.hstack((img_with_red, img_with_eggs)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
