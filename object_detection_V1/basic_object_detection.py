import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(4)  # Replace 0 with the correct index if needed

if not cap.isOpened():
    print("Error: Could not open video stream from webcam.")
    exit()

while True:
    try: 
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply a Gaussian blur to reduce noise and improve detection accuracy
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Threshold the image to get a binary image
        _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Approximate the contour to find shapes
            approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)

            # If the contour has 4 vertices, it's a rectangle
            if len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)
                if 0.95 <= aspect_ratio <= 1.05:  # Check if the aspect ratio is close to 1 for square
                    shape = "Square"
                else:
                    shape = "Rectangle"
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
                cv2.putText(frame, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Detect circles
            elif len(approx) > 4:
                area = cv2.contourArea(contour)
                (x, y), radius = cv2.minEnclosingCircle(contour)
                circularity = area / (np.pi * (radius ** 2))
                if 0.7 <= circularity <= 1.3:  # Circularity check
                    cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                    cv2.putText(frame, "Circle", (int(x) - 10, int(y) - int(radius) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Display the frame with detected shapes
        cv2.imshow("Circle and Rectangle Detection", frame)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except BaseException as e: 
        # Release the capture and close the windows
        cap.release()
        cv2.destroyAllWindows()
        raise e

# Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()
