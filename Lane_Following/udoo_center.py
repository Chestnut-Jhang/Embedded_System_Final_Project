import sys
import serial, time
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
#from cv2.dnn import readNetFromTensorflow
#from cv2.dnn import blobFromImage
from sklearn.cluster import KMeans, DBSCAN
from calibrate import *
from draw_line import get_yellow, get_range
from get_contours import get_gray_countour, contour_dump
from select_contours import contour_largest, contour_leftest, remove_contour
from scipy.misc import imresize

posX = 0
posY = 0
cargo = 0
start = 0
def _control_center( center_point ):
	ang = np.arctan2( center_point[0], center_point[1] )
	print("ang = ", ang)
	turn = 1-abs(ang)
	if turn < 0.1: turn = 0.1
	if ang < 0: turn = -turn
	speed = int(20*abs(turn)+15)
	return speed, turn

def get_contour_center( contour ):
	moment_contour = cv2.moments(contour)
	if moment_contour['m00']:
		moment_contour_x = int(moment_contour['m10']/moment_contour['m00'])
		moment_contour_y = int(moment_contour['m01']/moment_contour['m00'])
		return (moment_contour_x, moment_contour_y)

def get_contour_from_image( img ):
	line_yellows = get_range( img, np.array([10,100,180], np.uint8), np.array([60,255,255], np.uint8), cv2.COLOR_BGR2HSV)  # u: 10/110/200 ; 40/255/255   f: 20/110/200 ; 40/255/255
	line_whites  = get_range( img, np.array([65,150,30], np.uint8), np.array([255,255,180], np.uint8), cv2.COLOR_BGR2HLS)  # u: 80/150/30 ; 255/255/130   f: 80/150/30 ; 255/255/150
	line_reds    = get_range( img, np.array([150,0,0], np.uint8), np.array([255,255,255], np.uint8), cv2.COLOR_BGR2HLS)
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert the color image to gray image
	contours = get_gray_countour(img_gray)
	contour_dump( "img3/contours_full" + str(int(time.time()*10)) + ".jpg", contours, img)
	_, contours = remove_contour( line_yellows, contours, 1 )
	if len(contours) == 0: return None
	# _, contours = remove_contour( line_whites, contours, -1 ) # u: ##   f: ~~
	if len(contours) == 0: return None
	contour_left = contour_largest(contours) # u: largest   f: leftest
	contour_dump( "img/contours_extracted" + str(int(time.time()*10)) + ".jpg", contour_left, img)
	return contour_left

def control( contour, s ):
	contour_center = get_contour_center(contour)
	if contour_center is None: return
	print("contour center = ", contour_center)
	control_vec = np.subtract( (np.shape(img)[1]/2, np.shape(img)[0]), contour_center )
	speed, turn = _control_center( control_vec )
	cmd = "/ServoTurn/run " + str(speed) + " " + "{0:.2f}".format(turn) + " \n"
	print("cmd = ", cmd)
	s.write(cmd.encode())
	print("speed, turn = ", speed, turn)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ee2405/id1")


def on_message(client, userdata, msg):
	global posX, posY, cargo, start
	start = 1
	str = msg.payload.decode("utf-8")
	arr = str.split(",")
	posX = int(arr[0])
	posY = int(arr[1])
	cargo = int(arr[2])
	print(msg.topic)
	print(msg.payload)
	if msg.payload == b"quit":
		client.disconnect()
	#return str(msg.payload).split(",")
if __name__ == "__main__":
	s = serial.Serial("/dev/ttyACM0")
	vc = cv2.VideoCapture(1)
	for i in range(0,20): vc.read()
	f = open("timer.txt", "w")

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("192.168.1.66", 1883, 60)
	client.loop_start()

	label = {0: 'neg', 1: 'pos'}
	while start == 0:
		pass
	print("OK0")

	while 1:
		#global posX, posY, cargo
		#posX = 30
		#posY = 400
		#cargo = 0
	
		if int(posX) <= 150 and int(posX) >= 50 and int(posY) <= 400 and int(posY) >= 300:
			s.write("m".encode())
			
			call = s.read(1)	
			print("OK1")	
			print(str(call)[2])

			if str(call)[2] == "D":
				net = cv2.dnn.readNetFromTensorflow("../deep_learning/model/model.pb")
				#cap = cv2.VideoCapture(1)
				#for i in range(0,20): cap.read() ###
				ret, frame = vc.read()
				frame = imresize(frame, (128,128))
				frame = cv2.dnn.blobFromImage(frame)
				net.setInput(frame)
				pred = net.forward()
				ans = pred[0, :, 0, 0].argmax(axis=-1)
				# ans = 0
				print("OK3")

				if ans == int(cargo):
					s.write("y".encode())
					print("OK4")
				else:
					s.write("n".encode())
					print("OK5")

				call = s.read(1)
		else:
			s.write("l".encode())
			start_time = time.time()
			_, img = vc.read()
			img = calibrate(img)

			contour = get_contour_from_image(img)
			if not contour is None: control(contour,s)
			f.write( "Line 267: " + str(time.time()-start_time)+"\n")
			# time.sleep(.3)
