import cv2
import tensorflow as tf

# Load the model
model = tf.keras.models.load_model('/best_.pt')


image = cv2.imread('/Screenshot (3).png')
detections = model.detect(image)

for detection in detections:
    # Extract detection details
    # (e.g., bounding box coordinates, confidence score)
    pass

# Display the results
# (e.g., draw bounding boxes on the image)