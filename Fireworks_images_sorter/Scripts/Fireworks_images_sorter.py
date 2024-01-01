import cv2
import os
import shutil

def detect_fireworks(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #-----------------------------------------------------------------------------------#
    #           | Define a refined colour range for fireworks|                          #
    #           | ___________________________________________|                          #
    #                                                                                   #
    #              H   S    V            Key:                                           #
    #              |   |    |            ----                                           #
    #              |   |    |                                                           #
    #             \ / \ /  \ /                                                          #
    lower_color = (0, 100, 100)      #   H = Hue (0-179)                                #
    #              |   |    |                                                           #
    #              |   |    |            S = Saturation (0-255)                         #
    #             \ / \ /  \ /                                                          #
    upper_color = (20, 255, 255)     #   V = Value (0-255)                              #
    #-----------------------------------------------------------------------------------#
                
    # Create a mask to extract the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply morphological operations to reduce noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if fireworks are detected
    if contours:
        return True
    return False

def main(source_dir, detected_dir, undetected_dir):
    # Create destination directories if they don't exist
    if not os.path.exists(detected_dir):
        os.makedirs(detected_dir)
    if not os.path.exists(undetected_dir):
        os.makedirs(undetected_dir)

    # Iterate through files in source directory
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Adjust the image formats as needed
            image_path = os.path.join(source_dir, filename)

            # Check if fireworks are detected in the image
            if detect_fireworks(image_path):
                # Copy the image to the detected directory
                shutil.copy(image_path, os.path.join(detected_dir, filename))
                print(f"Fireworks detected in: {filename}. Image copied to detected directory.")
            else:
                # Copy the image to the undetected directory
                shutil.copy(image_path, os.path.join(undetected_dir, filename))
                print(f"No fireworks detected in: {filename}. Image copied to undetected directory.")

if __name__ == "__main__":
    # Replace 'source_directory_path', 'detected_directory_path', and 'undetected_directory_path'
    # with your actual paths
    source_directory_path = 'C:/Users/natha/Documents/Main/Programming/A.I/Projects/Image_sorter/Images/Source'
    detected_directory_path = 'C:/Users/natha/Documents/Main/Programming/A.I/Projects/Image_sorter/Images/Detected'
    undetected_directory_path = 'C:/Users/natha/Documents/Main/Programming/A.I/Projects/Image_sorter/Images/Undetected'

    main(source_directory_path, detected_directory_path, undetected_directory_path)
