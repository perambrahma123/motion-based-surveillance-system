import cv2
import numpy as np
from datetime import datetime
import winsound
import time

def motion_detection():
    cap = cv2.VideoCapture(0)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    
    # Video writer setup
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None
    
    # Recording status
    is_recording = False
    motion_frames_counter = 0
    RECORD_SECONDS = 5  # Duration to record after motion
    
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 30, 255, cv2.THRESH_BINARY)  # Increased threshold
        dilated = cv2.dilate(thresh, None, iterations=3)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        
        for contour in contours:
            # Increased area threshold to ignore smaller movements
            if cv2.contourArea(contour) < 8000:  # Increased from 5000 to 8000
                continue
                
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
            # Display "Motion Detected!" text
            text = "MOTION DETECTED!"
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame1, text, (10, 50), font, 1, (0, 0, 255), 2)
            
            # Play alert sound
            winsound.Beep(2500, 100)
            
            # Start recording if not already recording
            if not is_recording:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                video_filename = f'motion_video_{timestamp}.avi'
                out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))
                is_recording = True
                print(f"Started recording: {video_filename}")
                motion_frames_counter = fps * RECORD_SECONDS  # Record for RECORD_SECONDS seconds
        
        # Display recording status
        if is_recording:
            cv2.putText(frame1, "Recording...", (10, frame_height - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            out.write(frame1)
            motion_frames_counter -= 1
            
            # Stop recording after specified duration
            if motion_frames_counter <= 0:
                is_recording = False
                out.release()
                print("Stopped recording")
        
        # Display current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(frame1, current_time, (frame_width - 200, frame_height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('Motion Detector', frame1)
        
        frame1 = frame2
        ret, frame2 = cap.read()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    if out is not None:
        out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    motion_detection()