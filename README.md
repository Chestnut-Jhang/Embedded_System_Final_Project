# Chuan-Jia Jhang' s final project: Mr. Bean Production Line
![](http://gitlab.larc-nthu.net/105061224/final_project/raw/master/P_20180620_202111_Cut.jpg)

## 1　Project Introduction

　The project is designed for five BOE BOT Cars to accomplish a production line.
 
　My part is the first stage. There are two cargos on the lane filled with red or green beans
 
　and the correspondent pictures of them are stick on cargos. The car will run following the lane 
 
　and detect the specific cargo to move it to the next locatinon. 
 
## 2　Project Description

### 2.1　Preparation

(1) Prepare a GitLab working directory and a new Mbed project.

　`git clone <URL>`

　URL is the GitLab project URL, for example: git@gitlab.larc-nthu.net:105061224/final_project.git

　`mbed new BOE_BOT_Car`

(2) Add "4DGL-uLCD-SE" library to the current project

　`mbed add https://os.mbed.com/users/4180_1/code/4DGL-uLCD-SE/`

(3) Add "parallax" library to the current project

　`mbed add http://gitlab.larc-nthu.net/embedded_lab/parallax`

(4) Prepare some equipments and materials for the machine.

Equipment|Quantity
---------|--------
K64F board|1
Udoo Neo Board|1
USB Hub|1
Continuous Servo|4
Wheel|2
Gear|2
Camera|1
uLCD|1
Wires|many
Clamps|2
Boxes|2

### 2.2　Line Configuration

Equipment|Ground|Vcc|Digital Pin
---------|------|---|-----------
servo for right wheel|ground|6V (battery)|D12
servo for left wheel|ground|6V (battery)|D11
servo for right clamp|ground|6V (battery)|D7
servo for left clamp|ground|6V (battery)|D6
uLCD|ground|5V|RX->D0, TX->D1, RES->D2

### 2.3　Control the Equipments to Run the Car

(1) Go into the Mbed project **BOE_BOT_Car**.

　`cd ~/final_project/BOE_BOT_Car`

(2) Start VS code to edit **main.cpp**.

　`code main.cpp &`

(3) Copy the codes in **"final_project/BOE_BOT_Car/main.cpp"**.

　The code will run on K64F and is written to receive all the messages from Udoo_Neo. After receiving,
 
　it controls all the equipments in the car according to the messages.

(4) Compile the program.

　`sudo mbed compile -m K64F -t GCC_ARM -f`

(5) Push the reset button on the microcontroller.

　**Because K64F is connected to Udoo Neo, you have to push the reset button every time you run the python code**

　**to receive the message sent from Udoo Neo to execute the program normally.**
 
### 2.4 Udoo Neo receives message using MQTT, and K64F does using RPC Call
 
(1) Start VS code to edit **udoo_center.py**.

　`code udoo_center.py &`

(2) Copy the codes in **"final_project/lane_following/udoo_center.py"**.

　The code will run on the Udoo_Neo and is written to receive the messages from PC
 
　including position of the car and tasks the car should accomplish.
 
　After receiving, Udoo_Neo sends messages to K64F to tell what it should do at that time.

(3) Compile the program.

　`sudo python3 udoo_center.py`

(4) Connect the power for the BOE BOT Car.

(5) Execute the PC center.

　`sudo python3 mqtt_clipu.py`

(6) After the above instructions, the BOE BOT Car will successfully execute all the tasks.

(7) Notice:

　Because types of cameras and position of them on the cars are different between each car, the pictures they 
 
　capture may also be different. Therefore, you can use **color_show.py** in **"final_project/lane_following"** 
 
　to see the range of colors on pictures in HLS and HSV and correct the parameters of function **get_range()** 
 
　in **udoo_center.py**.
 
　`sudo python3 color_show.py`
 
　If you can't sure if the range you set on **udoo_center.py** is valid, you can use **draw_line.py** in 
 
　**"final_project/lane_following"** to test if the line is drawn successfully under this range.
 
　`sudo python3 draw_line.py`

### 2.5　Demo Video

　Video link: `https://drive.google.com/file/d/1waZzVGSLaNBcLPkk6MueRnyPoWsNytPN/view?usp=sharing`

　The video displays the operation of the machine with all things mentioned above.

## 3 The details for the operation of codes

　At the beginning, PC sends a message to Udoo Neo about the position of the cargos and what cargo it shold move.

　Then, PC sends the position of car continually. When car is on the way to the position of cargo, Udoo Neo sends
 
　messages to K64F to make car run following the lane. When car gets to the assigned position, Udoo Neo will tell
 
　the K64F to move the cargo. The process is that the car turns right to let the camera look at the picture stick on
 
　the cargo, and using Keras to detect if the cargo is the assigned one. If yes, car will move it to the next position
 
　to accomplish a cycle of operation. If not, car will resume to move to the next cargo and detect if the cargo is right.
 
　Finally, car will go back to the start position to do the next work (this part has not been finnished).

## 4　Difficulties for the Mr.Bean Production Line

### 4.1　RPC Call

　The difficulties for RPC call is the delay time between two boards. Initially, I found the car detected the right line on 

　the lane, but it doesn't correct its direction of moving. Then, I check the code in main.cpp, and found there is a second 

　delay before receiving the RPC call. Due to this delay, K64F can't receive the right message and do lane following. After 

　I comment this delay, car can do a perpect following as expected.

### 4.2　Surroundings dependence is very strong

　Before the demo, our group did the final project almost in the work station. Because the surrounding in the demo space 
 
　and workstation is very different, we can't do lane following at that time. After a correction, the car can do the same 
 
　as in the workstation.