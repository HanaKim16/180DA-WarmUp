import cv2
import numpy as np
from sklearn.cluster import KMeans

def get_central_rectangle(image, rectangle_size):
    h, w, _ = image.shape
    start_h = (h - rectangle_size) // 2
    start_w = (w - rectangle_size) // 2
    end_h = start_h + rectangle_size
    end_w = start_w + rectangle_size
    central_rectangle = image[start_h:end_h, start_w:end_w, :]
    return central_rectangle

def find_dominant_color(image, k):
    reshaped_image = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(reshaped_image)

    dominant_color = kmeans.cluster_centers_.astype(int)[np.argmax(np.unique(kmeans.labels_, return_counts=True)[1])]
    return dominant_color

# Example usage
video_feed = cv2.VideoCapture(0)
rectangle_size = 100  #adjust Size
num_clusters = 3  # Number of clusters for K-Means

while True:
    ret, frame = video_feed.read()
    if not ret:
        break

    central_rectangle = get_central_rectangle(frame, rectangle_size)
    dominant_color = find_dominant_color(central_rectangle, num_clusters)

    # Display the dominant color
    dominant_color_display = np.zeros((50, 50, 3), dtype=np.uint8)
    dominant_color_display[:, :] = dominant_color
    cv2.imshow('Q4 Find the Dominant Color', dominant_color_display)

    # Check for key press to exit the loop
    key = cv2.waitKey(1)
    if key == 27:  # 27 corresponds to the 'Esc' key
        break

video_feed.release()
cv2.destroyAllWindows()