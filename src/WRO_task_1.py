import pyrealsense2 as rs
import numpy as np
import cv2
import time
from jetracer.nvidia_racecar import NvidiaRacecar
from realsense_depth_Copy1copy import DepthCamera  # Import the DepthCamera class

# Initialize DepthCamera and car
car = NvidiaRacecar()
dc = DepthCamera()


#error fixing list
speed = 0.21
front_dist = 575 # when hint the front wall
wall_safe_distance_right = 400
wall_safe_distance_left = 400
# Define points for middle, left, and right regions
#all y value of the point
y = 180
point_mid = (320, y)
point_mid_left = (300, y)
point_mid_right = (340, y)
point_mid_left1 = (280, y)
point_mid_right1 = (360, y)

point_left = (100, y)
point_left_left = (80, y)
point_left_right = (120, y)
point_left_left1 = (60, y)
point_left_right1 = (140, y)

point_right = (560, y)
point_right_left = (540, y)
point_right_right = (580, y)
point_right_left1 = (520, y)
point_right_right1 = (600, y)

last_left = None
last_right = None
last_mid = None

# List of points for visualization with corresponding colors
points_mid = [point_mid, point_mid_left, point_mid_right, point_mid_left1, point_mid_right1]
points_left = [point_left, point_left_left, point_left_right, point_left_left1, point_left_right1]
points_right = [point_right, point_right_left, point_right_right, point_right_left1, point_right_right1]

# Initialize video writer
# Assuming color_image is 640x480 (adjust if different)
frame_width = 640
frame_height = 480
fps = 30  # Frames per second for the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi file
out = cv2.VideoWriter('output.avi', fourcc, fps, (frame_width, frame_height))

# Initialize direction 
right_direction = True
got_direction = False

#line color
blue_lower = np.array([83,124,89])
blue_upper = np.array([103,224,189])
orange_lower = np.array([0,118,109])
orange_upper = np.array([12,218,209])

steering_value = -1
loop = 0

#area of the find direction
#area of the find direction
roi_x, roi_y, roi_w, roi_h = 120, 140, 350, 300  # Center of 640x480 frame
# Define ROIs for red and green blocks
red_roi_x, red_roi_y, red_roi_w, red_roi_h = 0, 100, 640, 480  # Full screen
green_roi_x, green_roi_y, green_roi_w, green_roi_h = 0, 100, 640, 480  # Full screen

#stable the car
def stable(x,y):                #x stand for current gyro value while y stand for road number
    global right_direction
    if right_direction == True: #when it is going right directionn for all time   
        if x >0+y*90:           #too right
            car.steering=-0.3*steering_value   #turing left
        elif x <0+y*90:         #too right turing right
            car.steering=0.3*steering_value 
        else:                   #won't happen lol, but ensure the system have no bug, when it is 100% st.line. remian steering = 0
            car.steering = 0*steering_value 
    else:                       #when it is going left directionn for all time               
        if x >0-y*90:           #too right turing left
            car.steering=-0.3*steering_value 
        elif x <0*-y*90:        #too left turing right
            car.steering=0.3*steering_value 
        else:                   #won't happen lol, but ensure the system have no bug, when it is 100% st.line. remian steering = 0
            car.steering = 0*steering_value         


car.throttle = speed

while True:

    # Get frames using DepthCamera
    success, depth_image, color_image, accel, gyro, ts = dc.get_frame()
    if not success:
        continue
        
        
    if got_direction == False:
        # Crop to ROI
        car.throttle = 0
        color_roi = color_image[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        depth_roi = depth_image[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Convert ROI to HSV for color detection
        hsv_roi = cv2.cvtColor(color_roi, cv2.COLOR_BGR2HSV)

        # Create masks for blue and orange
        blue_mask = cv2.inRange(hsv_roi, blue_lower, blue_upper)
        orange_mask = cv2.inRange(hsv_roi, orange_lower, orange_upper)

        # Find contours for blue and orange lines in ROI
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Function to calculate average depth of a contour in ROI
        def get_contour_depth(contour, depth_roi):
            mask = np.zeros_like(depth_roi)
            cv2.drawContours(mask, [contour], -1, 255, -1)
            depth_values = depth_roi[mask == 255]
            if len(depth_values) > 0:
                return np.mean(depth_values) / 1000.0  # Convert to meters
            return None

        # Process blue contours
        blue_depth = None
        for contour in blue_contours:
            if cv2.contourArea(contour) > 20:  # Adjusted for smaller ROI
                blue_depth = get_contour_depth(contour, depth_roi)
                # Draw contour on ROI (or offset for full image)
                contour_offset = contour + np.array([roi_x, roi_y])  # Adjust for ROI position
                cv2.drawContours(color_image, [contour_offset], -1, (255, 0, 0), 2)

        # Process orange contours
        orange_depth = None
        for contour in orange_contours:
            if cv2.contourArea(contour) > 10:  # Adjusted for smaller ROI
                orange_depth = get_contour_depth(contour, depth_roi)
                # Draw contour on ROI (or offset for full image)
                contour_offset = contour + np.array([roi_x, roi_y])  # Adjust for ROI position
                cv2.drawContours(color_image, [contour_offset], -1, (0, 165, 255), 2)
        # Draw rectangle around ROI on full image
        cv2.rectangle(color_image, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
        # Compare distances
        if blue_depth and orange_depth:
            print(f"Blue line distance in ROI: {blue_depth:.2f} meters")
            print(f"Orange line distance in ROI: {orange_depth:.2f} meters")
            if blue_depth > orange_depth:
                print("Blue line is farther in ROI.")
                got_direction = True
                right_direction = True
            elif orange_depth > blue_depth:
                print("Orange line is farther in ROI.")
                got_direction = True
                right_direction = False
            else:
                print("Blue and orange lines are at the same distance in ROI.")
        elif blue_depth:
            print(f"Blue line distance in ROI: {blue_depth:.2f} meters (Orange not detected)")
            got_direction = True
            right_direction = False
        elif orange_depth:
            print(f"Orange line distance in ROI: {orange_depth:.2f} meters (Blue not detected)")
            got_direction = True
            right_direction = True
        else:
            print("No lines detected in ROI.")
        car.throttle = speed
    else:
        car.throttle = speed
    '''
    else:
        # Crop to ROI
        color_roi = color_image[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        depth_roi = depth_image[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Convert ROI to HSV for color detection
        hsv_roi = cv2.cvtColor(color_roi, cv2.COLOR_BGR2HSV)

        # Create masks for blue and orange
        blue_mask = cv2.inRange(hsv_roi, blue_lower, blue_upper)

        # Find contours for blue and orange lines in ROI
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Function to calculate average depth of a contour in ROI
        def get_contour_depth(contour, depth_roi):
            mask = np.zeros_like(depth_roi)
            cv2.drawContours(mask, [contour], -1, 255, -1)
            depth_values = depth_roi[mask == 255]
            if len(depth_values) > 0:
                return np.mean(depth_values) / 1000.0  # Convert to meters
            return None

        # Process blue contours
        blue_depth = None
        for contour in blue_contours:
            if cv2.contourArea(contour) > 50:  # Adjusted for smaller ROI
                blue_depth = get_contour_depth(contour, depth_roi)
                # Draw contour on ROI (or offset for full image)
                contour_offset = contour + np.array([roi_x, roi_y])  # Adjust for ROI position
                cv2.drawContours(color_image, [contour_offset], -1, (255, 0, 0), 2)

        # Compare distances
        if blue_depth:
            print(f"Blue line distance in ROI: {blue_depth:.2f} meters")
        else:
            print("No lines detected in ROI.")
    '''      
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # Get depth values for middle points
    dist_mid = depth_image[point_mid[1], point_mid[0]]
    dist_mid_left = depth_image[point_mid_left[1], point_mid_left[0]]
    dist_mid_right = depth_image[point_mid_right[1], point_mid_right[0]]
    dist_mid_left1 = depth_image[point_mid_left1[1], point_mid_left1[0]]
    dist_mid_right1 = depth_image[point_mid_right1[1], point_mid_right1[0]]
    
    # Calculate average for middle, excluding 0 values
    mid_values = [dist_mid, dist_mid_left, dist_mid_right, dist_mid_left1, dist_mid_right1]
    valid_mid = [v for v in mid_values if v != 0]
    avg_mid = sum(valid_mid) / len(valid_mid) if valid_mid else 0
    
    #handling avg equal case
    if last_mid is not None and avg_mid <1:
        avg_mid=last_mid
    last_mid = avg_mid
    
    print("Middle:", mid_values, "Average:", avg_mid)
    

    
    # Get depth values for left points
    dist_left = depth_image[point_left[1], point_left[0]]
    dist_left_left = depth_image[point_left_left[1], point_left_left[0]]
    dist_left_right = depth_image[point_left_right[1], point_left_right[0]]
    dist_left_left1 = depth_image[point_left_left1[1], point_left_left1[0]]
    dist_left_right1 = depth_image[point_left_right1[1], point_left_right1[0]]
    
    # Calculate average for left, excluding 0 values
    left_values = [dist_left, dist_left_left, dist_left_right, dist_left_left1, dist_left_right1]
    valid_left = [v for v in left_values if v != 0]
    avg_left = sum(valid_left) / len(valid_left) if valid_left else 0
    #handling avg equal case
    if last_left is not None and avg_left <1:
        avg_left=last_left
    last_left = avg_left
    
    print("Left:", left_values, "Average:", avg_left)

    # Get depth values for right points
    dist_right = depth_image[point_right[1], point_right[0]]
    dist_right_left = depth_image[point_right_left[1], point_right_left[0]]
    dist_right_right = depth_image[point_right_right[1], point_right_right[0]]
    dist_right_left1 = depth_image[point_right_left1[1], point_right_left1[0]]
    dist_right_right1 = depth_image[point_right_right1[1], point_right_right1[0]]
    
    # Calculate  average for right, excluding 0 values
    right_values = [dist_right, dist_right_left, dist_right_right, dist_right_left1, dist_right_right1]
    valid_right = [v for v in right_values if v != 0]
    avg_right = sum(valid_right) / len(valid_right) if valid_right else 0
    #handling avg equal case
    if last_right is not None and avg_right <1:
        avg_right=last_right
    last_right = avg_right
    
    print("Right:", right_values, "Average:", avg_right)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#  
    #stop the car when it needed by holding a hand in front of the camera
    '''
    if avg_mid < 50:
        car.throttle = 0
    else:
        car.throttle = 0.2
    '''

    '''
    #testing part of gyro
    stable(current_gyro,road)
    '''


    #controling the movment
    if ((avg_left <front_dist and avg_right<front_dist+200) or (avg_right <front_dist and avg_left<front_dist+200)) and avg_mid <front_dist: #when facing the wall
        if right_direction == True:
            car.steering = 1*steering_value 
            loop = 1
        else:
            car.steering = -1*steering_value 
            loop = 2
        print("facing wall")
    elif right_direction == True:
        if avg_right < 650 and avg_mid > front_dist: #when too right
            if avg_right < wall_safe_distance_right:
                car.steering = -1*steering_value 
                loop = 5
            else:
                car.steering = -1*(650-avg_right)/650*steering_value 
                loop = 6
            print("left")
        elif avg_left < 650 and avg_mid > front_dist: # when too left
            if avg_left < wall_safe_distance_left:
                car.steering = 1*steering_value 
                loop = 3
            else:
                car.steering = 1*(650-avg_left)/650*steering_value 
                loop = 4
            print("right")

        else:
            car.steering = 0*steering_value 
            loop = 7
    else:
        
        if avg_right < 700 and avg_mid > front_dist: #when too right
            if avg_right < wall_safe_distance_right:
                loop = 8
                car.steering = -1*steering_value 
            else:
                loop = 9
                car.steering = -1*(700-avg_right)/700*steering_value 
            print("left")
        elif avg_left < 700 and avg_mid > front_dist: # when too left
            if avg_left < wall_safe_distance_left:
                loop = 10
                car.steering = 1*steering_value 
            else:
                loop = 11
                car.steering = 1*(700-avg_left)/700*steering_value 
            print("right")

        else:
            loop = 12
            car.steering = 0*steering_value 
    # Create a copy of the color image for visualization
    vis_image = color_image.copy()

    # Draw points on the image (color-coded: Blue for middle, Green for left, Red for right)
    for point in points_mid:
        cv2.circle(vis_image, point, 5, (255, 0, 0), -1)  # Blue for middle
    for point in points_left:
        cv2.circle(vis_image, point, 5, (0, 255, 0), -1)  # Green for left
    for point in points_right:
        cv2.circle(vis_image, point, 5, (0, 0, 255), -1)  # Red for right

    # Add text for average distances
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    text_offset_y = 30  # Starting y-coordinate for text

    # Middle distance (Blue text)2
    mid_text = f"Middle Avg: {avg_mid:.1f} mm"
    cv2.putText(vis_image, mid_text, (10, text_offset_y), font, font_scale, (255, 0, 0), thickness)

    # Left distance (Green text)
    left_text = f"Left Avg: {avg_left:.1f} mm"
    cv2.putText(vis_image, left_text, (10, text_offset_y + 30), font, font_scale, (0, 255, 0), thickness)

    # Right distance (Red text)
    right_text = f"Right Avg: {avg_right:.1f} mm"
    cv2.putText(vis_image, right_text, (10, text_offset_y + 60), font, font_scale, (0, 0, 255), thickness)
    
    sterring_text = f"steering: {car.steering:.1f} mm"
    cv2.putText(vis_image, sterring_text, (10, text_offset_y + 90), font, font_scale, (0, 255, 255), thickness)
    
    loop_text = f"loop: {loop} mm"
    cv2.putText(vis_image, loop_text, (10, text_offset_y + 120), font, font_scale, (0, 255, 255), thickness)

    # Write the frame to the video file
    out.write(vis_image)

    # Display the image with points and text
    cv2.imshow("Points Visualization", vis_image)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        car.throttle = 0
        break
        
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('2'):
        car.throttle = speed
# Release resources
out.release()  # Release the video writer
dc.release()
cv2.destroyAllWindows()