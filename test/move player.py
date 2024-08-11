import cv2
import numpy as np

# Initialize global variables
drawing = False  # True if mouse is pressed
roi_selected = False  # True if ROI has been completed
moving = False  # True if moving the ROI
ix, iy = -1, -1
roi = (0, 0, 0, 0)
roi_image = None
moving_offset_x, moving_offset_y = 0, 0
origin = (0, 0)  # Starting point for the arrow

# Desired dimensions for the displayed video
desired_width = 1000
desired_height = 600

# Mouse callback function
def draw_roi(event, x, y, flags, param):
    global ix, iy, drawing, roi_selected, moving, roi, roi_image, moving_offset_x, moving_offset_y, origin

    if event == cv2.EVENT_LBUTTONDOWN:
        if roi_selected and (ix <= x <= ix + roi[2]) and (iy <= y <= iy + roi[3]):
            moving = True
            moving_offset_x = ix - x
            moving_offset_y = iy - y
            origin = (ix + roi[2]//2, iy + roi[3]//2)  # Update origin when starting to move
        elif not roi_selected:
            drawing = True
            ix, iy = x, y
            roi = (ix, iy, 0, 0)  # Initialize roi size to 0

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            roi = (ix, iy, x - ix, y - iy)
        elif moving:
            ix, iy = x + moving_offset_x, y + moving_offset_y

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            roi_selected = True
            roi = (ix, iy, x - ix, y - iy)
            roi_image = frame[iy:iy + roi[3], ix:ix + roi[2]].copy()  # Copy the selected ROI
            origin = (ix + roi[2]//2, iy + roi[3]//2)  # Set origin for the arrow
        elif moving:
            moving = False

# Video capture
cap = cv2.VideoCapture('./')  # Adjust path to your video file
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', draw_roi)

# Boolean to control the pause state
paused = True
frame = None

while True:
    if not paused or frame is None:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to desired dimensions
        frame = cv2.resize(frame, (desired_width, desired_height))

    temp_frame = frame.copy()
    if roi_image is not None:
        temp_frame[iy:iy + roi[3], ix:ix + roi[2]] = roi_image
        if moving:
            cv2.arrowedLine(temp_frame, origin, (ix + roi[2]//2, iy + roi[3]//2), (0, 0, 0), 2)  # Thinner arrow
            cv2.rectangle(temp_frame, (ix, iy), (ix + roi[2], iy + roi[3]), (255, 255, 255), 1)  # White rectangle

    if drawing or moving:
        cv2.rectangle(temp_frame, (ix, iy), (ix + roi[2], iy + roi[3]), (0, 0, 0), 1)  # Red rectangle while drawing

    # Show the current frame
    cv2.imshow('Video', temp_frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('p'):  # Press 'p' to toggle pause
        paused = not paused
    elif key == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()