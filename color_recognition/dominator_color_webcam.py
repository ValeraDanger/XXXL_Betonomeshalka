# Python code for Multiple Color Detection


import numpy as np
import cv2
import pprint

# Capturing video through webcam

# Start a while loop
def recognize_color(imageFrame):
    color_squares = np.zeros(5)
    cv2.imshow("cropped", imageFrame)
    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    # Set range for red color and
    # define mask
    red_lower = np.array([0, 0, 0], np.uint8)
    red_upper = np.array([5, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for green color and
    # define mask
    green_lower = np.array([41, 130, 0], np.uint8)
    green_upper = np.array([90, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    # Set range for blue color and
    # define mask
    blue_lower = np.array([96, 51, 0], np.uint8)
    blue_upper = np.array([121, 255, 201], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    orange_lower = np.array([6, 0, 0], np.uint8)
    orange_upper = np.array([17, 255, 191], np.uint8)
    orange_mask = cv2.inRange(hsvFrame, orange_lower, orange_upper)

    yellow_lower = np.array([17, 0, 0], np.uint8)
    yellow_upper = np.array([24, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame,
                              mask=red_mask)

    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                mask=green_mask)

    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                               mask=blue_mask)

    yellow_mask = cv2.dilate(yellow_mask, kernal)
    res_yellow = cv2.bitwise_and(imageFrame, imageFrame,
                               mask=yellow_mask)

    orange_mask = cv2.dilate(orange_mask, kernal)
    res_orange = cv2.bitwise_and(imageFrame, imageFrame,
                               mask=orange_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            color_squares[0] += w * h
        # Creating contour to track green color

    contours, hierarchy = cv2.findContours(green_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            color_squares[1] += w * h

        # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            color_squares[2] += w * h

        # Creating contour to track red color
    contours, hierarchy = cv2.findContours(yellow_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            color_squares[3] += w * h

        # Creating contour to track red color
    contours, hierarchy = cv2.findContours(orange_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            color_squares[4] += w * h


    if (np.argmax(color_squares) == 0):
        print("Red")
        return 'R'
    elif (np.argmax(color_squares) == 1):
        print("Green")
        return 'G'
    elif (np.argmax(color_squares) == 2):
        print("Blue")
        return 'B'
    elif (np.argmax(color_squares) == 3):
        print("Yellow")
        return 'Y'
    elif (np.argmax(color_squares) == 4):
        print("Orange")
        return 'O'