# Team Hero Pong
This is the official repository of the Hero Pong Team for the 2025 WRO Future Engineers. In this repository, you can find everything related to our robot.

## Our repository

* `t-photos` contains 2 photos of the team (an official one and one funny photo with all team members)
* `v-photos` contains 6 photos of the vehicle (from every side, from top and bottom)
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `schemes` contains one or several schematic diagrams in form of JPEG, PNG or PDF of the electromechanical components illustrating all the elements (electronic components and motors) used in the vehicle and how they connect to each other.
* `src` contains code of control software for all components which were programmed to participate in the competition
* `other` is for other files which can be used to understand how to prepare the vehicle for the competition. It may include documentation how to connect to a SBC/SBM and upload files there, datasets, hardware specifications, communication protocols descriptions etc. If there is nothing to add to this location, the directory can be removed.

## Team members

<p align="center">
  <img src="https://github.com/user-attachments/assets/adf2b5d0-bb73-4cb8-8a1d-684fb89e8408" alt="Imagen 1" width="500">
</p>

## Members from left to right:

---

## Cheng Tsun To:
### Age: 15

He is passionate about robotics. His main role in the team is to design and come up with ideas in terms of the chassis and model of the robot. He also gives ideas on the use of components such as the microcomputer and the motor, as well as programming. 

## Mak Ching Long:
### Age: 16

He is the main programmer of the team. He's good at programming, especially in Python. He's also good at communicating with others so he can explain the program to the team and teammates can work together more easily. His role in the team is the programming of the robot, as well as documenting the whole process of the robot.

## Hui Chit Ming:
### Age: 15

He is optimistic and often cheers up the team. He brings the team together and allows us to overcome challenges. His role in the team is to do some of the Python programming and mainly document the repository of the robot.

<br>
 <br>


 > [!NOTE]
> To see the funny photo [here](https://github.com/kieviceb/TERRENATOR-WRO-2024/tree/main/t-photos)


<br>


## Components


| <img src="https://github.com/user-attachments/assets/641dbab1-b12c-40ba-bcb9-73b2401fa7ed" alt="Alt 1" width="200"/> | <img src="https://github.com/user-attachments/assets/0c14f0a2-f720-42db-9fbb-cf9034cb6cf6" alt="Alt 1" width="200"/> | <img src="https://github.com/user-attachments/assets/f03dd1c9-fa48-42ad-b609-4f839e0a1de0" alt="Alt 1" width="200"/> | 
| :------------: |:-------------:| :------------:|
|[Jetson Nano B01 x1](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)|JetRacer Pro expansion board x1|cooling fan x1|
| <img src="https://github.com/user-attachments/assets/308fefe0-61c9-4e8f-8fdd-20f77f33addc" width="200"/> | <img src="https://github.com/user-attachments/assets/e10e6040-a7e2-48da-b08b-5fb837d980a7" alt="Alt 1" width="200"/> | <img src="https://github.com/user-attachments/assets/f05c69cc-1995-411a-ae74-88c3eef60139" alt="Alt 1" width="200"/> |
| [WP 1625 brushed electronic speed controller x1](https://www.hobbywing.com/en/products/quicrun-wp-1625-brushed53) |[RC380 high speed carbon brushed DC motor x1](https://www.aliexpress.com/i/1005003661229027.html)|[e6001 servo motor](https://www.amazon.com/-/zh_TW/dp/B06XF7MFPJ) |
| <img src="https://github.com/user-attachments/assets/bb4f38f3-5291-4a82-b1b4-f688ee4dfd86" width="200"/> |<img src="https://github.com/user-attachments/assets/c0dde0e4-c927-452a-8d0b-1cc9c07cd210" alt="Alt 1" width="200"/> |<img src="https://github.com/user-attachments/assets/0e900534-9620-4852-a608-f126c70fc098" width="200"/> |
|[Realsense D435i camera x1](https://www.intelrealsense.com/depth-camera-d435i/)|[8.4V 18650 battery ×4](https://www.steameshop.com/product/18650/?srsltid=AfmBOoq64uuFMYHSZRhLKaVYFERjOLc22R510Y9Ci-HTcJxwL2meLc1y6ps)|[Single key button x1](https://www.amazon.co.uk/Programmable-User-Defined-Button-Customized-Combination/dp/B08SQGWZN4?th=1) |
| <img src="https://github.com/user-attachments/assets/585c5ace-ae6b-40d9-ba9d-0225de282e81" width="200"/> 
| [Wireless-AC8265 chip x1](https://www.waveshare.com/wireless-ac8265.htm) |

## Introduction

After deep investigation and consideration, we decided to search for suitable components and build them by ourselves. We used metal as the main material for most of the components since they do not break so easily and can fully simulate actual vehicles. We tried to make the robot lighter and more efficient and minimize its size. We stumbled upon different model shapes and ended up with an idea of the shape of a race car with lightweight construction and aerodynamic design to create the most efficient autonomous vehicle. Besides, we decided to use Nvidia Jetson Nano as the motherboard due to its ability to carry out complex calculations and parallel processing quickly. It’s also versatile and portable enough to control the vehicle.

## Circuit Diagram

<p align="center">
  <img src="https://github.com/user-attachments/assets/17807b2c-e8e5-45d5-86e3-0f7c1fa7c916" alt="Imagen 1" width="500">
</p>

This circuit diagram represents the connections of the robotic system powered by four 18650 batteries and is controlled and processed by an Jetson Nano B01 motherboard. It consists only one camera for obstacle detection and direction determination, a servo motor for steering, and a DC motor for torque and speed using a on-board motor driver. The camera also consists of multiply kinds of sensors such s RGB sensor, gyroscope and accelerometer. The Jetson Nano B01 board is connected to the JetRacer Pro expansion board, which is the motor control board. It provides and regulates power transferred to other components.
<br>
 <br>


 > [!NOTE]
>For more details go to the schemes README by clicking [here](https://github.com/CFSS-WRO/WRO2425/blob/main/schemes/README.md)


<br>


---


### Mobility management

### 1- Movement

- Motor: Our driving motor consists of a [RC380 high speed carbon brushed DC motor](https://www.aliexpress.com/i/1005003661229027.html) with gearbox powers the rear axle which can run up to 15000 revolutions per minute. It is controlled via car.throttle (Ranged from -1 to 1) in the Navigation Module. Negative value means backwards while 0 means no movement. Besides, the motor is powerful and capable of powering four wheels to run at the same time.
<p align="center">
  <img src="https://github.com/user-attachments/assets/fad5ef22-f7fe-4a69-8b6e-41da49685577" alt="Imagen 1" width="400">
</p>

The carbon brushes in the motor have good electrical conductivity. This provides reliable and constant power to the car every time when used.

- Electronic speed controller ([WP 1625 brushed](https://www.hobbywing.com/en/products/quicrun-wp-1625-brushed53)): A brushed DC motor usually runs continuously as long as adequate voltage is applied to the vehicle. To control how fast the motor spins, the brushed ESC simply chops the voltage. When the motor’s speed exceeds the designated maximum speed set in the Navigation Module, it reduces the voltage being transferred to the motor and hence controls the speed of the car. Therefore, this can conserve enough energy to power the car.

<p align="center">
  <img src="https://github.com/user-attachments/assets/08971778-bc06-44f3-b101-dcce93132fcf" alt="Imagen 1" width="400">
</p>

### 2- Steering
 
- Steering system: The steering system is controlled by a servo motor. We chose to use [e6001 servo](https://www.amazon.com/-/zh_TW/dp/B06XF7MFPJ) which is a metal gear. It can withstand and output high power (6kg/cm torque) while maintaining its reasonably small size, weight and high portability. It controls the front axle using Ackerman steering geometry, controlled via car.steering (Ranged from -1 to 1) in the Navigation Module.

<p align="center">
  <img src="https://github.com/user-attachments/assets/1217d6f5-a701-48f2-973d-56203400c31b" alt="Imagen 1" width="300">
</p>

- Steering method: We use Ackerman steering as the method of steering. Unlike differential steering, this method requires one servo motor only, and it is attached to the front axle so that it offers a good balance of control, higher stability, and effectiveness. Apart from that, we made the front and rear axle differentials so that the steering is more flexible. This also reduces tire skidding and ensures a firm grip is maintained between the wheels and the mat. The diagram below shows the differences between Ackerman steering and differential steering vehicles:
<p align="center">
  <img src="https://github.com/user-attachments/assets/9fa1718e-56e3-4a8f-9472-a1f04b0856e1" alt="Imagen 1" width="250">
</p>

### Caemra and sensor management

### 1- Power system
- Battery: Four [18650 batteries](https://www.steameshop.com/product/18650/?srsltid=AfmBOoq64uuFMYHSZRhLKaVYFERjOLc22R510Y9Ci-HTcJxwL2meLc1y6ps) (10400mAh, two in parallel, two in series) provide ~77 Wh to all sensors and the Nvidia Jetson Nano mother board which can support 3-minute rounds. The batteries we use have large capacity and no memory effect which allows maximized power for controlling the system. 
-	Onboard protection circuit: HY2120+AOD514 lithium battery protection circuit which can prevent overcharge, over-discharge, overcurrent, and short circuits.
-	Onboard battery voltage monitor: FP5139 automatic buck-boost voltage regulator circuit delivers stable 5V voltage to Jetson Nano. 
-	Onboard AINA219 acquisition chip: Real-time monitoring of battery voltage and charging current.
<p align="center">
  <img src="https://github.com/user-attachments/assets/d353da49-aeb4-4cb8-a5cb-9e693ac85e92" alt="Imagen 1" width="250">
</p>

### 2- Camera and sensors
We had thought of using typical popular widely used sensors at first. However, at last we used Intel RealSense D435i depth camera as the main sensor for our vehicle due to its high versatility and resolution. It consists of multiply ways of detecting objects. Therefore, it’s a new challenge that we may face while trying out this complex camera. The main reason we chose this camera is the fact that it has IMU installed. Most of the widely used cameras do not include gyroscope or accelerometer. Compared to other camera or sensors, this camera is versatile and multi-functioned. It is capable to carry out different measurements at the same time, which is more cost-effective. Besides, its wide field of view allows it to cover more area and less blind spots. Therefore, we ended up using RealSense D435i as the main sensor of the car.

<p align="center">
  <img src="https://github.com/user-attachments/assets/483be46d-bef5-4593-a3ba-b03cc1d4b545" alt="Imagen 1" width="400">
</p>



- Stereo depth camera: It is capable of processing image depth at up to 90 frames per second, it updates the object depth positions every 11.1 milliseconds, making it the ideal camera for tracking objects when the car is moving at such high speed. The camera runs a global shutter sensor which provides great low‑light sensitivity allowing robots to navigate spaces with the lights off. Therefore, this can minimize the effect of the disturbance of light in the surrounding environment. Unlike typical ultrasonic sensors, it can detect objects from a farther distance, which enhances the effectiveness of object detection. On the other hand, there are fewer blind spots in our camera when compared to those of ultrasonic sensors. LiDAR sensors are also another widely used type of sensor used in robotics. However, it required much more energy to run and has less details in-depth data compared to our stereo camera.
<p align="center">
  <img src="https://github.com/user-attachments/assets/0e1613c7-a394-453a-bc6e-d5edb2a98360" alt="Imagen 1" width="250">
  <img src="https://github.com/user-attachments/assets/16fb3ef4-1755-4df2-b9c5-3eb3c8674062" alt="Imagen 2" width="250">
</p>
The invalid depth band (blind spot) is very small

- RGB colour sensor: The sensor detects the colour of objects with the technology of rolling shutter. Although rolling shutter is usually used for capturing still images, it’s more energy-efficient compared to global shutter sensor and it’s capable enough to sense the colour of blocks and colour lines in both tasks. The sensor’s high RGB frame and sensor resolution also plays a major role in enhancing the efficient detection of colours. Another reason we used this camera is because the RGB colour sensor has a slightly smaller angle of view than the depth camera. Compared to other widely used sensors such as raspberry pi sc1174  stereo camera, its field of view is smaller which actually benefits the sensing of objects in the tasks. As a result, different colours in the surroundings would not affect the detection of the RGB camera which enables accurate determination of different colour for the tasks.
- Gyroscope: The IMU installed in the camera allows it to refine its depth awareness in any situation even when the camera moves and allows point-cloud alignment. The IMU combines multiple sensors with gyroscopes to sense angular orientation and angular velocity. It detects both rotation and movement of the camera in 3 axes, pitch, yaw and roll using a three-dimensional coordinate system. Axes ACC-X, ACC-Y, ACC-Z. The ACC-X axis points to the right, ACC-X points up and ACC-X points vertically upwards from the top surface of the sensor. Clockwise rotation around the $\overrightarrow{Ω_X}$ (roll), $\overrightarrow{Ω_Y}$  (pitch) or $\overrightarrow{Ω_Z}$  (yaw) axes is considered as positive, which means counterclockwise rotation is considered as negative. These measurements allow the camera to detect direction of rotation and rotation angles so that it can measure the distance of the blocks and walls at different angles in both tasks. We also tried to make use of the image direction stabilization function to send information to the servo to change the direction of the wheels in accordance to the nearby blocks and walls. For our vehicle, Only $\overrightarrow{Ω_Z}$ is essential for the direction determination. We set value 0 as horizontal forward of the car. The sector at the right is set as positive while the left side is considered as negative. Whenever the value is biased to one side (positive/negative), we programmed the servo to run with values of the another side until the value is resulted in 0, which is horizontally forward. When the vehicle moves near the corners of the field, the camera only senses a wall in the front  at a close distance and it will sense the gyroscope to give a changed $\overrightarrow{Ω_Z}$ value and therefore it can enable the servo to turn and change the direction of the vehicle.

- Accelerometer: The IMU installed in the camera also combines with an accelerometer which is essential for our robot. It senses linear axis orientation and acceleration.  It determines whether the camera is going faster or slower and therefore it can provide instruction to the camera to adjust its image capture rate and for anti-blur capturing. This ensures that stable and still images at every frame can be captured clearly. Apart from that, it serves another important purpose in dealing with the fluctuation problem of electricity and power supply to the servo and motor. At first, our vehicle faces the problem of insufficient supply of power to the car. We tried to minimize the weight and utilize batteries with larger capacity. However, the problem wasn’t solved until we tried to tune the accelerometer. We found out that it can measure the change in velocity (acceleration) of an object over time. Therefore, we can make use of the accelerometer to send signals to control the speed of the car. Since the power supply to the car changes whenever it starts moving and fluctuates from time to time when running, the power supply management is very important to ensure that the vehicle can run flawlessly. Therefore, whenever the speed of the car exceeds the designated maximum car speed, we programmed the vehicle to give signal to the Electronic Speed Controller and adjust the speed of the servo and motor. Hence, this ensures that adequate power is conserved for the car to power all the components of the car throughout the whole tasks.

<p align="center">
  <img src="https://github.com/user-attachments/assets/e23e0a92-adfc-4575-8f2b-2450a388ddff" alt="Imagen 1" width="400">
</p>

# Code and programming
## Assignment
### Python Library: 
```ino
import pyrealsense2 as rs
import numpy as np
import cv2
import time
from jetracer.nvidia_racecar import NvidiaRacecar
from realsense_depth_Copy1copy import DepthCamera
```
 
1.	Pyrealsense: Used to send data and information of the objects sensed by the camera to the Jetson Nano
2.	cv2: Allows the image captured by the camera to be transferred to data in the Python code.
4.	NvidiaRacecar from realsense_depth_Copy1copy: It gives information, data and a determining standard for the realsense D435i camera to give essential information for the direction determination of the servo and the movement of the motor.

| Variables  | Function/description |
| -------------- | -------------- |
| speed  | The speed of the car |
| front_dist  | The range of dangerous distance|
| steering_value  | Due to the reason that we have 2 different kinds of models of servo. For model A, the right direction of the steering value is –1, while for model B, the right direction value is 1.  In order to make this code change to different models more easily, we add this variable. By changing the value in this variable be 1 or –1, the steering direction can be corrected easily |
| loop  | It stands for whether the "if statement" the car is currently working on, so that we can fix the bug more easily  |
| mixed loop  | The same as “loop”, it stands for which "if statement" it is, but only for identifying the red blocks and green blocks  |
| flag_block | When it is True, it means that a block was captured by the camera |
| flag_block_based_on  | To check which "if statement" has run the code and made the value of flag_block change, for easier debugging| red_logic  | When it is True, it will run the part for the red block obstacle avoidance | green_logic  |   When it is True, it will run the part for the green block obstacle avoidance | got_direction  | To check is the car know the direction of car travel, when got direction is True, it will detecting line ( orange and blue) if it is False, it will stop decting line
  | right_direction  | It stands for the direction of the car's travel. True stands for right, False stands for left
  | passed_all_block_check  | When it is True, it means there are 2 blocks with different colours in front of the camera
  |blue_lower = np.array([90,80,50]) blue_upper = np.array([110,180,140]) orange_lower = np.array([0,87,108]) orange_upper = np.array([11,187,208]) red_lower1 = np.array([169,205,76]) red_upper1 = np.array([179,255,176]) green_lower = np.array([36,99,50]) green_upper = np.array([56,199,144])|In order to make the camera note that which RGB valuen it stand for different colour, we assigned different kinds of list for the upper limit and lower limit of the colour| 
last_left = None / last_right = None  last_mid = None / last_block = None| Since our depth camera sometimes cannot obtain the distance successfully, we will store the last value it got successfully and use that value if the distance cannot be obtained | dist_red, dist_green |  Distance of the red block and green block
 | checked_is_behind_line checked_is_behind_line2  | If these values are True, that means the block is behind the line, we can ignore it until the car pass through the blue or orange line|  
## Strategy for open challenge

### Servo configuration:


```ino
if x >0-y*90:           #too right turing left
            car.steering=-0.3*steering_value 
        elif x <0*-y*90:        #too left turing right
            car.steering=0.3*steering_value 
        else:                  
            car.steering = 0*steering_value         
```       
This initializes the servo and ensures that the specific angles for left, right turns. The car steering value ranges from -1 to 1, using the gyroscope, clockwise which means moving to the right is considered positive and counterclockwise means negative to the left direction.


### Camera and sensors’ object detection and obstacle determination:
```ino
points_mid = [point_mid, point_mid_left, point_mid_right, point_mid_left1, point_mid_right1]
points_left = [point_left, point_left_left, point_left_right, point_left_left1, point_left_right1]
points_right = [point_right, point_right_left, point_right_right, point_right_left1, point_right_right1]
```
The above code is a list of points for visualization with corresponding colors. 
We had set several dots on the camera to sense the image colour depth (black) so that when the car drives near a turning corner, the camera will give signals to the Jetson Nano motherboard and it allows the servo to work in accordance to the situation. We added data and information to the monitor connected to the car for better vision and for easier understanding of what the program is at so that it is easy to know where did the car error occurred during our process of coding. We came up with the idea of adding more dots on the screen for better and more accurate determination of the distance of the nearest wall from the car. At last, we added 5 dots for each left, centre and right sector of the camera. Our program calculates the average black colour depth of each sector separately. It will then compare the 3 values to determine if the vehicle is moving in the wrong direction or to an unfavourable direction. The average depth values at these points help assess distances to lane boundaries and obstacles. If the car is too close to an obstacle ahead (avg_mid < 550 mm) or side walls (avg_left or avg_right < 700 mm), it steers sharply away (car.steering = -1 to 1). Otherwise, it uses proportional steering based on how close it is to the left or right boundary to stay centered. If it is too close to the left boundary, steer right proportionally. If it is too close to the right boundary, steer left proportionally.
The steering values will smoothly vary between -1 and 1 in accordance to distance deviations. We will exclude the extreme values and 0, which is ‘junk data’ in this situation so that the average is not affected by other extreme polar values. Middle points centered at around x = 320,	Left points at around x = 100 and right points at around x = 560. By this method, this reduces the risk of the disturbance of lights in the surrounding environment from affecting the determination of black walls.	The gyroscope also plays a big role in this task. Whenever the car is too farther away from the horizontal forward track, the car will adjust itself to the opposite direction to keep the car moving forward and not hitting the walls.



## References
- https://www.intelrealsense.com/depth-camera-d435i/
- https://spectrum.ieee.org/lidar-on-achip#:~:text=Most%20groups%20developing%20autonomous%20vehicles%20see%20lidar%20as,more%20fidelity%20than%20can%20be%20done%20with%20cameras
- https://developer.nvidia.com/embedded/jetson-nano
- https://developer.download.nvidia.com/assets/embedded/secure/jetson/Nano/docs/NV_Jetson_Nano_Developer_Kit_User_Guide.pdf?__token__=exp=1751552084~hmac=e63bf29d233df0d843b6c97e4486a0eed943069fe968967cf5e0ea8cd218808c&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ9
- https://youtu.be/F3G0sUz3_Jw?si=XnzUtsvSodAnV4Uu
- https://wro-association.org/wp-content/uploads/WRO-2025-Future-Engineers-Self-Driving-Cars-General-Rules.pdf









