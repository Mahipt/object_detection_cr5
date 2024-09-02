import cv2
import os
from datetime import datetime
import shutil

class Image_Taker: 
    def __init__(self): 
        # Initialize the webcam
        self.cap = cv2.VideoCapture(4)  # Replace 0 with the correct index if needed

        if not self.cap.isOpened():
            print("Error: Could not open video stream from webcam.")
            exit()
    
    def interactive_window(self): 
        if os.path.exists("calibrate_images"): 
            print(f"Images path calibrate_images exist, do you want to remove it")
            print("Type Y to remove; N to keep it")
            inputChar = input() 
            if inputChar == 'Y': 
                shutil.rmtree("calibrate_images")
        print("Images will be store in \'./calibrate_images\'")
        
        print("Press 'h' to capture an image and 'q' to quit.")

        image_folder = 'calibrate_images'
        # check whether the image folder has been found (create one if necessary)
        if not os.path.exists(image_folder): 
            print(f"Create image folder {image_folder}")
            os.mkdir(image_folder)

        image_index = 0 # image index
        image_prefix = 'calibrate_images/captured_image_'
        while True:
            try: 
                # Capture frame-by-frame
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Error: Failed to capture image.")
                    break

                # Display the live video feed
                cv2.imshow("Live Video Feed", frame)

                # Wait for a key press
                key = cv2.waitKey(1) & 0xFF

                if key == ord('h'):
                    # increase the image index
                    image_index += 1
                    image_path = image_prefix + str(image_index) + '.jpg'
                    # Save the captured image as a .jpg file when 'h' is pressed
                    cv2.imwrite(image_path, frame)
                    print(f"Image saved as {image_path}")
                elif key == ord('q'):
                    # Exit the loop when 'q' is pressed
                    break
            except BaseException as e: 
                # Release the capture and close any OpenCV windows
                self.cap.release()
                cv2.destroyAllWindows()
                raise e

        # Release the capture and close any OpenCV windows
        self.cap.release()
        cv2.destroyAllWindows()
    
        # Capture frame-by-frame
    def take_image(self, path: str | None): 
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            return
        # Display the live video feed
        cv2.imshow("Live Video Feed", frame)
        
        cur_time = datetime.now()
        image_prefix = "snap_shots_folder"
        image_name = '_'.join([str(cur_time.year), str(cur_time.month), str(cur_time.date), str(cur_time.hour), str(cur_time.second)])
        if path is None: 
            print(f"Didn't assign any folder, image will be store under path: {image_prefix}")
            if not os.path.exists(image_prefix):  
                os.mkdir(image_prefix)
        
        image_path = image_prefix + '/' + image_name + '.jpg'
        cv2.imwrite(image_path, frame)
        print(f"Image saved as {image_path}")

if __name__ == "__main__":
    # create image taker object
    try: 
        img_taker_obj = Image_Taker()
        img_taker_obj.interactive_window()
    except BaseException as e: 
        raise e