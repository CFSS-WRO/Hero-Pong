import pyrealsense2 as rs
import numpy as np
import cv2
import time
from jetracer.nvidia_racecar import NvidiaRacecar
from realsense_depth_Copy1copy import DepthCamera  # Import the DepthCamera class

#value cab change
speed =  0.1903
front_dist = 1050

steerign_value = -1

loop = 0
red_logic = False
green_logic = False
passed_all_block_check = False

mixed_loop = 0
completed_first_roll = False
# Initialize DepthCamera and car
car = NvidiaRacecar()
dc = DepthCamera()

check = 0

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
#Turing_for_block= False

#line color
'''
school

blue_lower = np.array([101, 60, 50])
blue_upper = np.array([121, 160, 115])
orange_lower = np.array([168, 65, 61])
orange_upper = np.array([179, 165, 161])
green_lower = np.array([38,115,52])
green_upper = np.array([58, 215, 152])
'''
blue_lower = np.array([90,80,50])
blue_upper = np.array([110,180,140])
orange_lower = np.array([165,60,75])
orange_upper = np.array([179,160,175])
red_lower1 = np.array([169,205,76])
red_upper1 = np.array([179,255,176])
green_lower = np.array([36,99,50])
green_upper = np.array([56,199,144])


'''
red_lower2 = np.array([170, 120, 70])
red_upper2 = np.array([180, 255, 255])
'''


#start up
dist_red, dist_green = 0,0
checked_is_behind_line = False
checked_is_behind_line2 = False
flag_block_based_on = 0
last_left = None
last_right = None
last_mid = None
last_block = None

#area of the find direction
roi_x, roi_y, roi_w, roi_h = 220, 140, 350, 300  # Center of 640x480 frame
# Define ROIs for red and green blocks
red_roi_x, red_roi_y, red_roi_w, red_roi_h = 0, 100, 640, 480  # Full screen
green_roi_x, green_roi_y, green_roi_w, green_roi_h = 0, 100, 640, 480  # Full screen

#function
#stable the car
def stable(x,y):                #x stand for current gyro value while y stand for road number
    global right_direction
    if right_direction == True: #when it is going right directionn for all time   
        if x >0+y*90:           #too right
            car.steering=-0.3*steerign_value   #turing left
        elif x <0+y*90:         #too right turing right
            car.steering=0.3*steerign_value
        else:                   #won't happen lol, but ensure the system have no bug, when it is 100% st.line. remian steering = 0
            car.steering = 0*steerign_value
    else:                       #when it is going left directionn for all time               
        if x >0-y*90:           #too right turing left
            car.steering=-0.3*steerign_value
        elif x <0*-y*90:        #too left turing right
            car.steering=0.3*steerign_value
        else:                   #won't happen lol, but ensure the system have no bug, when it is 100% st.line. remian steering = 0
            car.steering = 0*steerign_value      
def detect_line(x):
    color_roi = color_image[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    depth_roi = depth_image[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

    # Convert ROI to HSV
    hsv_roi = cv2.cvtColor(color_roi, cv2.COLOR_BGR2HSV)

    # Create masks
    blue_mask = cv2.inRange(hsv_roi, blue_lower, blue_upper)
    orange_mask = cv2.inRange(hsv_roi, orange_lower, orange_upper)

    # Find contours
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Function to get Y-coordinate of a contour's midpoint
    def get_contour_mid_y(contour, roi_y_offset):
        if cv2.contourArea(contour) > 50:
            x, y, w, h = cv2.boundingRect(contour)
            mid_y = int(y + h / 2) + roi_y_offset
            return mid_y
        return None

    # Function to calculate average depth of a contour
    def get_contour_depth(contour, depth_roi):
        mask = np.zeros_like(depth_roi)
        cv2.drawContours(mask, [contour], -1, 255, -1)
        depth_values = depth_roi[mask == 255]
        if len(depth_values) > 0:
            return np.mean(depth_values) / 1000.0  # Convert to meters
        return None

    # Process blue contours
    blue_mid_y = None
    blue_depth = None
    if blue_contours:
        largest_blue = max(blue_contours, key=cv2.contourArea)
        if cv2.contourArea(largest_blue) > 25:
            blue_mid_y = get_contour_mid_y(largest_blue, roi_y)
            blue_depth = get_contour_depth(largest_blue, depth_roi)
            contour_offset = largest_blue + np.array([roi_x, roi_y])
            cv2.drawContours(color_image, [contour_offset], -1, (255, 0, 0), 2)

    # Process orange contours
    orange_mid_y = None
    orange_depth = None
    if orange_contours:
        largest_orange = max(orange_contours, key=cv2.contourArea)
        if cv2.contourArea(largest_orange) > 25:
            orange_mid_y = get_contour_mid_y(largest_orange, roi_y)
            orange_depth = get_contour_depth(largest_orange, depth_roi)
            contour_offset = largest_orange + np.array([roi_x, roi_y])
            cv2.drawContours(color_image, [contour_offset], -1, (0, 165, 255), 2)

    # Draw ROI rectangle
    if x == 1:
        cv2.rectangle(color_image, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)

    # Return based on x value
    if x == 100:
        #print(f"Blue line Mid Y: {blue_mid_y}, Depth: {blue_depth:.2f} meters")
        #print(f"Orange line Mid Y: {orange_mid_y}, Depth: {orange_depth:.2f} meters")
        return blue_mid_y, orange_mid_y, blue_depth, orange_depth
    else:
        if blue_depth and orange_depth:
            print(f"Blue line distance: {blue_depth:.2f} meters")
            print(f"Orange line distance: {orange_depth:.2f} meters")
            if blue_depth > orange_depth:
                print("Blue line is farther.")
                return 1
            elif orange_depth > blue_depth:
                print("Orange line is farther.")
                return 2
            else:
                print("Lines at same distance.")
                return 3
        elif blue_depth:
            print(f"Blue line distance: {blue_depth:.2f} meters (Orange not detected)")
            return 4
        elif orange_depth:
            print(f"Orange line distance: {orange_depth:.2f} meters (Blue not detected)")
            return 5
        else:
            print("No lines detected.")
            return 6
        
def detect_block_position_for_action(dist_red, red_mid_y, blue_mid_y, orange_mid_y, blue_depth, orange_depth,bottom):
    global flag_block
    if dist_red >= 999999999999999999999999999999 or red_mid_y is None: #"No red block detected", "No red block detected"
        flag_block_based_on = 1
        flag_block = False
        
        
    blue_position = "Unknown"
    orange_position = "Unknown"
    
    behind_blue = False
    behind_orange = False
    print("bottom and orange_mid_y are: ",bottom,blue_mid_y,orange_mid_y)
    # Compare with blue line
    if blue_mid_y is not None:
    # Allow some vertical tolerance (e.g., 50 pixels) to consider the block aligned with the line
        if bottom <  blue_mid_y:
            blue_position = "Behind blue line"
            behind_blue =  True
    # Compare with orange line
    if orange_mid_y is not None:
        if bottom < orange_mid_y:

            orange_position = "Behind orange line"
            behind_orange = True
    if behind_blue == True or behind_orange== True: #the block is behind the line:
        return True
    else:
        return False
i = 0

while True:
    
    i = i+1
    if i == 4:
        car.throttle = speed
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # Get frames using DepthCamera
    success, depth_image, color_image, accel, gyro, ts = dc.get_frame()
    if not success:
        continue       
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    if got_direction == False:
        detecting = detect_line(1)
        if detecting ==1:
            got_direction = True
            right_direction = True
        elif detecting ==2:
            got_direction = True
            right_direction = False
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
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#  
    # Find color blocks using ROIs
    # Crop to red and green ROIs
    red_roi = color_image[red_roi_y:red_roi_y+red_roi_h, red_roi_x:red_roi_x+red_roi_w]
    green_roi = color_image[green_roi_y:green_roi_y+green_roi_h, green_roi_x:green_roi_x+green_roi_w]

    # Convert ROIs to HSV
    red_hsv = cv2.cvtColor(red_roi, cv2.COLOR_BGR2HSV)
    green_hsv = cv2.cvtColor(green_roi, cv2.COLOR_BGR2HSV)

    # Create masks for red and green
    red_mask = cv2.inRange(red_hsv, red_lower1, red_upper1)
    '''
    red_mask2 = cv2.inRange(red_hsv, red_lower2, red_upper2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    '''
    green_mask = cv2.inRange(green_hsv, green_lower, green_upper)

    # Function to get center of colored pixels in ROI
    def get_roi_center(mask, roi_x_offset, roi_y_offset):
        # Find non-zero pixels (colored pixels)
        coords = np.column_stack(np.where(mask > 0))
        if len(coords) > 50:  # Minimum pixel threshold to avoid noise
            # Calculate average x, y (center of mass)
            avg_y, avg_x = np.mean(coords, axis=0)
            # Adjust for ROI offset to get coordinates in full image
            center_x = int(avg_x + roi_x_offset)
            center_y = int(avg_y + roi_y_offset)
            return np.array([center_x, center_y])
        return None

    # Get centers of red and green blocks
    red_center = get_roi_center(red_mask, red_roi_x, red_roi_y)
    green_center = get_roi_center(green_mask, green_roi_x, green_roi_y)

    # Calculate midpoint (x, y only) if both centers are found
    flag_block_based_on = 2
    flag_block = False

# Function to safely get depth value with boundary checking
    def get_depth_safe(depth_image, x, y, width=640, height=480):
        if 0 <= x < width and 0 <= y < height:
            return depth_image[y, x]
        return 0

    # Function to calculate average depth within a contour
    def get_contour_depth(contour, depth_image, roi_x_offset, roi_y_offset, width=640, height=480):
        # Create a mask for the contour
        mask = np.zeros_like(depth_image, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, -1)
        # Adjust for ROI offset
        depth_values = depth_image[mask == 255]
        non_zero_values = depth_values[depth_values > 0]
        if len(non_zero_values) > 10:  # Ensure enough valid pixels
            # Filter outliers (e.g., within 1.5 standard deviations)
            mean = np.mean(non_zero_values)
            std = np.std(non_zero_values)
            valid_values = non_zero_values[(non_zero_values >= mean - 1.5 * std) & (non_zero_values <= mean + 1.5 * std)]
            return np.mean(valid_values) if len(valid_values) > 0 else 0
        return 0
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#RED
# Red block and Green block detection logic   
# Red block and Green block detection logic   
    if red_mask is not None and green_mask is not None:
        contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        red_blocks = []
        # Process each contour to get center and depth
        for contour in contours_red:
            area_red = cv2.contourArea(contour)
            if area_red > 50:  # Stricter area threshold to reduce noise
                # Get bounding box and center
                x, y, w, h = cv2.boundingRect(contour)
                center_x = int(x + w / 2) + red_roi_x  # Adjust for ROI offset
                center_y = int(y + h / 2) + red_roi_y
                center = np.array([center_x, center_y])

                # Calculate depth within the contour
                avg_depth = get_contour_depth(contour, depth_image, red_roi_x, red_roi_y)

                if avg_depth > 0:  # Only include blocks with valid depth
                    red_blocks.append({
                        'center': center,
                        'area': area_red,
                        'depth': avg_depth,
                        'contour': contour
                    })
        contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        green_blocks = []

        # Process each contour to get center and depth
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:  # Stricter area threshold to reduce noise
                # Get bounding box and center
                x, y, w, h = cv2.boundingRect(contour)
                center_x = int(x + w / 2) + green_roi_x  # Adjust for ROI offset
                center_y = int(y + h / 2) + green_roi_y
                center = np.array([center_x, center_y])

                # Calculate depth within the contour
                avg_depth = get_contour_depth(contour, depth_image, green_roi_x, green_roi_y)

                if avg_depth > 0:  # Only include blocks with valid depth
                    green_blocks.append({
                        'center': center,
                        'area': area,
                        'depth': avg_depth,
                        'contour': contour
                    })
        # Select the closest red block (with area as tie-breaker)
        green_logic = False
        red_logic = False
        passed_all_block_check = False
        
        if red_blocks and green_blocks:
            mixed_loop = 1
        # Add a 'source' key to each block to track its origin
            for block in red_blocks:
                block['source'] = 'red'
            for block in green_blocks:
                block['source'] = 'green'
            block_list = red_blocks + green_blocks
            # Sort by depth, then by area (larger area wins for similar depths)
            selected_block = min(block_list, key=lambda b: (b['depth'], -b['area']))
            source = selected_block['source']
            if source == "red":
                red_logic = True
                green_logic = False
            else:
                red_logic = False
                green_logic = True
            passed_all_block_check = True
        elif red_blocks:
            red_logic = True
            green_logic = False
            mixed_loop = 2
        elif green_blocks:
            red_logic = False
            green_logic = True
            mixed_loop = 3
    # Red block detection logic
    if red_logic == True:
        # Find contours of red blocks
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        red_blocks = []

        # Process each contour to get center and depth
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 150:  # Stricter area threshold to reduce noise
                # Get bounding box and center
                x, y, w, h = cv2.boundingRect(contour)
                center_x = int(x + w / 2) + red_roi_x  # Adjust for ROI offset
                center_y = int(y + h / 2) + red_roi_y
                center = np.array([center_x, center_y])
                bottom_y = int(y + h + red_roi_y)

                # Calculate depth within the contour
                avg_depth = get_contour_depth(contour, depth_image, red_roi_x, red_roi_y)

                if avg_depth > 0:  # Only include blocks with valid depth
                    red_blocks.append({
                        'center': center,
                        'area': area,
                        'depth': avg_depth,
                        'contour': contour,
                        'bottom' : bottom_y
                    })

        # Select the closest red block (with area as tie-breaker)
        if red_blocks:
            # Sort by depth, then by area (larger area wins for similar depths)
            selected_block = min(red_blocks, key=lambda b: (b['depth'], -b['area']))
            midpoint = selected_block['center']
            dist_red = selected_block['depth']
            red_area = selected_block['area']
            red_bottom = selected_block['bottom']

            print(f"Selected Red Block - Midpoint: {midpoint}, Depth: {dist_red:.1f} mm, Area: {red_area}")

            # Draw ROIs and center on color image
            cv2.rectangle(color_image, (red_roi_x, red_roi_y), (red_roi_x + red_roi_w, red_roi_y + red_roi_h), (0, 0, 255), 2)
            cv2.rectangle(color_image, (green_roi_x, green_roi_y), (green_roi_x + green_roi_w, green_roi_y + green_roi_h), (0, 255, 0), 2)
            cv2.circle(color_image, (int(midpoint[0]), int(midpoint[1])), 5, (0, 0, 255), -1)
            # Draw contour for debugging
            cv2.drawContours(color_image, [selected_block['contour'] + np.array([red_roi_x, red_roi_y])], -1, (255, 0, 0), 2)

            # Steering control
            mid_y_of_line = detect_line(100)
            checked_is_behind_line = detect_block_position_for_action(dist_red, midpoint[0], mid_y_of_line[0], mid_y_of_line[1], mid_y_of_line[2], mid_y_of_line[3],red_bottom)
            if avg_mid <800:
                checked_is_behind_line = False
                                                                      
            #or (500 < midpoint[0] < 640 and dist_red < 300)
            if red_area < 100  or checked_is_behind_line == True :
                flag_block_based_on = 3
                flag_block = False
            else:
                if avg_right <275 and avg_left > avg_right + 200 :
                    car.steering= -1*steerign_value #turn left
                      
                    loop = 1
                    flag_block_based_on = 4
                    flag_block = True
                elif midpoint[0] > 120:
                    if midpoint[0] >= 270:
                        loop = 2 
                        car.steering = 0.4*steerign_value
                        flag_block_based_on = 5
                        flag_block = True
                        loop = 21
                        print("Steering right for red block")
                        '''
                        if avg_mid <= 1150:
                            car.steering = 1*steerign_value
                            flag_block = True
                            loop = 21
                            print("Steering right for red block")
                        else:
                            flag_block = False
                            loop = 22
                        '''
                    else:
                        loop = 3
                        car.steering = (midpoint[0] - 120) / 200*steerign_value
                        print("Adjusting steering for red block")
                        flag_block_based_on = 6
                        flag_block = True     
                    last_block = "red"
                else:
                    loop = 4
                    car.steering = 0
                    flag_block_based_on = 7
                    flag_block = False
                    
        else:
            loop = 4
            dist_red = 9999999999999999999999999999999
            red_area = 9999999999999999999999999999999
            flag_block_based_on = 8
            flag_block = False
            print("No valid red blocks detected")
            loop = 7
    
    #else:
    #    loop = 5
    #    dist_red = 9999999999999999999999999999999
    #    red_area = 9999999999999999999999999999999
    #    flag_block = False
    #    print("Red mask is None")
    #    loop = 8
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#GREEN1

    elif green_logic == True:
        # Find contours of red blocks
        contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        green_blocks = []

        # Process each contour to get center and depth
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 150:  # Stricter area threshold to reduce noise
                # Get bounding box and center
                x, y, w, h = cv2.boundingRect(contour)
                center_x = int(x + w / 2) + green_roi_x  # Adjust for ROI offset
                center_y = int(y + h / 2) + green_roi_y
                center = np.array([center_x, center_y])
                bottom_y = int(y + h + green_roi_y)

                # Calculate depth within the contour
                avg_depth = get_contour_depth(contour, depth_image, green_roi_x, green_roi_y)

                if avg_depth > 0:  # Only include blocks with valid depth
                    green_blocks.append({
                        'center': center,
                        'area': area,
                        'depth': avg_depth,
                        'contour': contour,
                        'bottom': bottom_y
                    })
        # Select the closest green block (with area as tie-breaker)
        if green_blocks:
            # Sort by depth, then by area (larger area wins for similar depths)
            selected_block = min(green_blocks, key=lambda b: (b['depth'], -b['area']))
            midpoint_green = selected_block['center']
            dist_green = selected_block['depth']
            green_area = selected_block['area']
            green_bottom = selected_block['bottom']

            print(f"Selected green Block - Midpoint: {midpoint_green}, Depth: {dist_green:.1f} mm, Area: {green_area}")

            # Draw ROIs and center on color image
            cv2.rectangle(color_image, (green_roi_x, green_roi_y), (green_roi_x + green_roi_w, green_roi_y + green_roi_h), (0, 0, 255), 2)
            cv2.rectangle(color_image, (green_roi_x, green_roi_y), (green_roi_x + green_roi_w, green_roi_y + green_roi_h), (0, 255, 0), 2)
            cv2.circle(color_image, (int(midpoint_green[0]), int(midpoint_green[1])), 5, (0, 0, 255), -1)
            # Draw contour for debugging
            cv2.drawContours(color_image, [selected_block['contour'] + np.array([green_roi_x, green_roi_y])], -1, (255, 0, 0), 2)

            # Steering control
            mid_y_of_line = detect_line(100)
            checked_is_behind_line2 =  detect_block_position_for_action(dist_green, midpoint_green[0], mid_y_of_line[0], mid_y_of_line[1], mid_y_of_line[2], mid_y_of_line[3],green_bottom) 
            if avg_mid <800:
                checked_is_behind_line2 = False
            if green_area < 50  or checked_is_behind_line2 == True: 
                flag_block_based_on = 9
                flag_block = False
            else:
                if dist_green > 3200:
                    flag_block = False
                if avg_left <275: #too right
                    car.steering= 1*steerign_value
                    loop = 41
                    flag_block_based_on = 10
                    flag_block = True
                elif midpoint_green[0] <521:
                    if midpoint_green[0] <= 30:
                        loop = 42 
                        #if avg_mid <= 1150:
                        car.steering = -1*steerign_value
                        flag_block_based_on = 11
                        flag_block = True
                        
                        print("Steering right for green block")
                        #else:
                         #   flag_block = False
                          #  loop = 42
                    else:
                        loop = 43
                        car.steering = -1*(midpoint_green[0] - 120) / 200*steerign_value
                        print("Adjusting steering for green block")
                        flag_block_based_on = 12
                        flag_block = True
                    last_block = "green"
                else:
                    loop = 44
                    
                    flag_block_based_on = 13
                    if dist_green >3200:
                        flag_block = False
                        #dist_green = None
                    else:  
                    #if completed_first_roll == False:
                        car.steering = -1*steerign_value
                        flag_block = True
                    #elif :
                     #  flag_block = False
                
        else:
            dist_green = 9999999999999999999999999999999
            green_area = 9999999999999999999999999999999
            flag_block_based_on = 14
            flag_block = False
            print("No valid green blocks detected")
            loop = 47
    else:
        loop = 45
        dist_green = 9999999999999999999999999999999
        green_area = 9999999999999999999999999999999
        flag_block_based_on =15
        flag_block = False
        print("green mask and red mask is None")
        loop = 48
    
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #controling the movment
    detecting = detect_line(0)
    
    if flag_block == True:
        pass
    
    elif ((avg_left <front_dist + 80 and avg_right-100<front_dist) or (avg_right <front_dist + 80 and avg_left-100<front_dist)) and avg_mid <front_dist and red_center is None: #when facing the wall
        completed_first_roll = True
        if right_direction == True:
            if loop == 151 or loop == 152 or loop == 13 or loop ==14 or loop == 12:
                car.steering = -1*steerign_value
            else:
                car.steering = 1*steerign_value
                loop = 9
        else:
            car.steering = -1*steerign_value
            loop = 10
    elif right_direction == True:
        if avg_left < 550 and avg_mid > front_dist: # when too left
            if avg_left < 315:
                car.steering =  0.7*steerign_value
                loop = 11
            else:
                car.steering = -1*(550-avg_left)/550*steerign_value
                loop = 12
        elif avg_right < 650 : #and avg_mid > front_dist: when too right
            if avg_right < 375:
                car.steering = -1*steerign_value
                loop = 13
            else:
                car.steering = -1*(650-avg_right)/650*steerign_value
                loop = 14
            print("left")
        else:
            if last_block == "red":
                car.steering = 0.6 *steerign_value
                last_block = None
                loop = 151
            #elif last_block == "green":
             #   car.steering = -0.6 *steerign_value
              #  last_block = None
               # loop = 156
            else:
                if avg_left < 400:
                    car.steering = 1*steerign_value
                    loop = 153
                else:
                    if last_block == "green": 
                        car.steering = -0.5*steerign_value
                        check = check + 1
                        if check >2:
                            
                            last_block = None
                        loop = 155
                    
                    else:
                        car.steering = 0.4*steerign_value
                        if check >=2:
                            
                            last_block = None
                        last_block = None
                        loop = 152
    else:    
        if avg_right < 700 and avg_mid > front_dist: #when too right
            if avg_right < 275:
                car.steering = -0.7*steerign_value
                loop = 16
            else:
                car.steering = -1*(700-avg_right)/700*steerign_value
                loop = 17
            print("left")
        elif avg_left < 700 and avg_mid > front_dist: # when too left
            if avg_left < 380:
                car.steering = 1*steerign_value
                loop = 18
                print("3")
            else:
                car.steering = 1*(700-avg_left)/700*steerign_value
                loop = 19
            print("right")

        else:
            if red_center is not None:
                pass
            elif green_center is not None:
                pass
            else:
                car.steering = 0
            loop = 20
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
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


    # Middle distance (Blue text)
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
    # Red block distance (Red text)
    red_block_text = f"Red Block: {dist_red:.1f} mm" if red_center is not None else "Red Block: Not detected"
    cv2.putText(vis_image, red_block_text, (10, text_offset_y + 120), font, font_scale, (0, 0, 255), thickness)

    # Green block distance (Green text)
    green_block_text = f"Green Block: {dist_green:.1f} mm" if green_center is not None else "Green Block: Not detected"
    cv2.putText(vis_image, green_block_text, (10, text_offset_y + 150), font, font_scale, (0, 255, 0), thickness)
    
    flag_block_text = f"flag_block: {flag_block} "
    cv2.putText(vis_image, flag_block_text, (10, text_offset_y + 180), font, font_scale, (0, 0, 255), thickness)
    
    loop_text = f"loop: {loop} "
    cv2.putText(vis_image, loop_text, (10, text_offset_y + 210), font, font_scale, (0, 0, 255), thickness)
    
    mixed_loop_text = f"mix_loop: {mixed_loop} "
    cv2.putText(vis_image, mixed_loop_text, (10, text_offset_y + 240), font, font_scale, (0, 0, 255), thickness)
    
    block_result_text = f"checked_is_behind_line: {checked_is_behind_line} {checked_is_behind_line2} "
    cv2.putText(vis_image, block_result_text, (10, text_offset_y + 270), font, font_scale, (0, 0, 255), thickness)
    
    flag_block_based_text = f"checked_is_behind_line: {flag_block_based_on} "
    cv2.putText(vis_image, flag_block_based_text, (10, text_offset_y + 300), font, font_scale, (0, 0, 255), thickness)
    
    
    cv2.line(vis_image, (120, 0), (140, frame_height), (255, 255, 255), 2)
    cv2.line(vis_image, (520, 0), (520, frame_height), (255, 255, 255), 2)
    cv2.line(vis_image, (194, 0), (194, frame_height), (255, 255, 255), 2)
    # Write the frame to the video file
    out.write(vis_image)

    # Display the image with points and text
    cv2.imshow("Points Visualization", vis_image)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        car.throttle = 0      
        break
    print(flag_block)
    checked_is_behind_line = False
    checked_is_behind_line2 = False
# Release resources
out.release()  # Release the video writer
dc.release()
cv2.destroyAllWindows()
