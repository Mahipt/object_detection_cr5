import cv2
import cv2.aruco as aruco

# Initialize the webcam at index 4
cap = cv2.VideoCapture(4)

# Load the predefined dictionary for ArUco markers
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

# Define the physical positions based on the problem statement
physical_positions = {
    0: (0, 0, 0),                  # ArUco 0 at (0, 0, 0)
    1: (0.6858, 0, 0),             # ArUco 1 at (0.6858, 0, 0)
    2: (0.6858, 0.3302, 0),        # ArUco 2 at (0.6858, 0.3302, 0)
    3: (0, 0.3302, 0)              # ArUco 3 at (0, 0.3302, 0)
}

if not cap.isOpened():
    print("Error: Could not open video stream from webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the markers in the frame
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # If markers are detected
    if ids is not None:
        # Draw the markers on the frame
        aruco.drawDetectedMarkers(frame, corners, ids)

        # Output the detected marker IDs and their physical positions
        detected_positions = []
        for marker_id in ids.flatten():
            if marker_id in physical_positions:
                position = physical_positions[marker_id]
                detected_positions.append((marker_id, position))
        
        print("Detected marker positions:")
        for marker_id, position in detected_positions:
            print(f"Marker ID {marker_id}: Position {position}")
    
    # Display the resulting frame
    cv2.imshow("ArUco Marker Detection", frame)

    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
