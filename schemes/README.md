# Circuit diagram

---

here you can find the circuit that integrates our robot, you can find a  simple but easy-to-understand explanation of it.
<br>
 <br>
![image](https://github.com/user-attachments/assets/35b1f848-39b5-4471-96bd-da7e45c2e8a4)


---
### Explanation:

---

1. Microcomputer (Jetson Nano B01): 
The central CPU & GPU board (upper board in the diagram) manages other components, 
mainly the JetRacer Pro expansion board. It receives signals, calculates and 
processes them, and sends the output to the other connected devices.

---

2. Motor control board (JetRacer Pro expansion board): 
Regulates and supplies power going to the microcomputer, servo motor, electronic 
speed controller and to the motor. It is powered by the 18650 lithium batteries. 
The power supply is connected to the Jetson Nano B01 through the power pin with two 5V pins and one 3.3V pin. 
The GND pin serves as the ground, connected to Jetson Nano’s GND. 
SCL and SDA are connected to the SCL and SDA on the Jetson Nano respectively. 
This module controls commands and data between the two boards.

---

3. Realsense D435i camera (Includes stereo depth camera, RGB color sensor, gyroscope and accelerometer): 
It is connected to and powered by the Jetson Nano board with a USB type c cable.

---

4. Cooling fan: 
Connected to the 5V pin of the Jetson Nano for power to run. 
GND: Ground, connected to Jetson Nano’s GND. 
Yellow cable connected to TACH of the Jetson Nano for the motherboard to sense the speed of the fan to ensure that the fan is working normally.

---

5. WP 1625 brushed electronic speed controller: 
It is connected to and powered by the motor control board. 
It also connects to and controls the voltage provided to the DC motor. 
It is connected to the motor driver outputs. 
The speed controller receives the 8.4V power supply from the Jetson Nano.

---

6. RC380 high speed carbon brushed DC motor (On top of the motor control board in the right diagram):
It is connected to the electronic speed controller.
It is powered by the motor control board indirectly with maximum 6V power supplied by the speed controller.

---

7. e6001 servo motor (In the right diagram):
Connected to the motor control board.
Signal Pin: Connects to the servo driver output signal pin on the back side of the Jetson Nano.
Power pin: 6V power supply power input to the servo, connected to the positive and negative charged pins on the Jetson Nano board.

---

8. Single key button:
A button connected to the Jetson Nano with USB cable to manually control the power supply of the board by the motor control board.

---

9. Power supply: 
Four 18650 batteries (two in parallel, two in series). Each 18560 lithium battery provides an operating range from 3.6V to 4.2V. By connecting the batteries in series, it supports maximum 8.4V to the motor control board and indirectly to the Jetson Nano. A battery voltage monitor will maintain the power supply to be 6V for other components. 
