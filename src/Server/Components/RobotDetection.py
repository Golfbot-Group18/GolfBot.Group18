import math
import cv2
import numpy as np
from Components.DetectionMethods import *


def DetectRobot(frame):
    lower_green = np.array([50, 45, 80])
    upper_green = np.array([100, 150, 255])

    # lower_blue = np.array([0, 60, 90])
    # upper_blue = np.array([255, 100, 100])

    green_area = DetectColor(frame, lower_green, upper_green)
    # blue_area = DetectColor(frame, lower_blue, upper_blue)
    # tip =  DetectRobotEdge(frame)

    return green_area


def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def CalculateRobotTriangle(contour):
    # This function only works for a right-angled triangle on the robot
    # with precisely half the width of it in the middle

    # Creates a minimum area rectangle that wraps around
    # rect = cv2.minAreaRect(contour)
    # width, height = rect[1]

    # Approximates and straightens the contour lines so that it extracts the vertices of the shape
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approximated_points = cv2.approxPolyDP(contour, epsilon, True)

    # If the approximation returns a list longer than 3,
    # it means that the shape is not a triangle as it has more than 3 sides
    if len(approximated_points) != 3:
        return None

    # Reshapes the way the data is stored
    points = approximated_points.reshape((3, 2))
    pt1, pt2, pt3 = points[0], points[1], points[2]

    side_length_1 = euclidean_distance(pt1, pt2), (pt1, pt2)
    side_length_2 = euclidean_distance(pt1, pt3), (pt1, pt3)
    side_length_3 = euclidean_distance(pt2, pt3), (pt2, pt3)

    # Find the index and value of the hypotenuse (the longest side)
    lengths = [side_length_1, side_length_2, side_length_3]
    sorted_lengths = sorted(lengths, key=lambda x: x[0])

    return sorted_lengths


def CalculateRobotWidth(contour):
    sorted_lengths = CalculateRobotTriangle(contour)
    shortest_length = sorted_lengths[0]

    return shortest_length[0] * 2


def CalculateRobotHeading(contour):
    # Returns coordinates for tip of the robot
    sorted_lengths = CalculateRobotTriangle(contour)
    # side_length_1 = sorted_lengths[0]

    # Side length 2 is the adjacent side to the hypotenuse
    side_length_2 = sorted_lengths[1]
    # Side length 3 is the hypotenuse
    side_length_3 = sorted_lengths[2]

    # pt variables are unsorted points pt = (x,y) of the side lengths
    pt1, pt2 = side_length_3[1]
    pt3, pt4 = side_length_2[1]

    # Overlapping point is the point of overlap of the hypotenuse and adjacent

    if np.array_equal(pt3, pt1) or np.array_equal(pt3, pt2):
        overlapping_point = pt3
        starting_point = pt4

    elif np.array_equal(pt4, pt1) or np.array_equal(pt4, pt2):
        overlapping_point = pt4
        starting_point = pt3
    # Make it return the other point from side a so that we have a direction
    else:
        raise ValueError("Could not find overlapping point")

    return starting_point, overlapping_point
