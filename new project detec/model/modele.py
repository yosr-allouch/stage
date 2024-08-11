import cv2
from best_.pt import ObjectDetectionModel


# Load your model
model = ObjectDetectionModel('./best_.pt')

# Function to handle frame processing
def process_frame(frame):
    # Detect objects in the frame
    detections = model.detect(frame)
    
    # Interact with the detections
    # For example, move a detected object
    # This part will depend on how you want to interact with the objects
    
    return frame

# Load your video
cap = cv2.VideoCapture('path/to/your/video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Display the frame
    cv2.imshow('Frame', frame)
    
    key = cv2.waitKey(1)
    if key == ord('p'):  # Pause video on pressing 'p'
        paused_frame = process_frame(frame)
        cv2.imshow('Paused Frame', paused_frame)
        cv2.waitKey(0)  # Wait indefinitely until a key is pressed
    
    elif key == ord('q'):  # Quit video on pressing 'q'
        break

cap.release()
cv2.destroyAllWindows()