'''
File: 	rot2proG.py
Author: Jaiden Ferraccioli
Brief: 	This class is a control interface for the SPID Elektronik rot2proG antenna rotor controller.
	This software was designed as an open source interface between the rotor controller and
	other systems. This can paired with an orbit propegator in order to extend usability and
	range of communication between an earth station and satellites or a communication station
	and a moving target. 
'''

import serial
import time
import os
'''
This class defines the control interface for the SPID Elektronik rot2proG antenna rotor controller.

Note: 	The controller will not change azimuth or elevation values unless the rotor is connected.

Setup:	The controller must be set to use the "SPID" protocol. To do this, press the 'S' button on the
	controller until it says 'PS' along with the current azimuth and elevation. Then the left or
	right buttons on the controller to change between protocols. Select the protocol saying 'SP' in
	the 'Horizontal' field of the controller. Once the controller is set to use the SPID protocol,
	we must put it into automated mode. To do this, press the 'F' button until the controller reads
	'A' along with the current azimuth and elevation. You are now ready to communicate with the
	rotor controller.
'''
class Rot2proG:

	pulse = 0
	debug = False
	max_az = float(360)
	min_az = float(-180)
	max_el = float(180)
	min_el = float(0)
	dev_path = '/dev/cu.usbserial-A4008X6p'

	'''
	This sets up the serial connection and pulse value.
	When set to true, the debugging parameter allows for information such as
	asimuth, elevation and pulse to be printed out when functions are called.
	Debugging defualts to False.
	'''
	def __init__(self, debugging=False):
		#self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=600, bytesize=8, parity='N', stopbits=1, timeout=None)
		self.ser = serial.Serial(port=self.dev_path, baudrate=600, bytesize=8, parity='N', stopbits=1, timeout=None)
		print(str(self.ser.name))
		self.status()
		self.debug = debugging
		if(self.debug):
			print(self.ser.name)
			print("Pulse: " + str(self.pulse) + "\n")

	'''
	This makes sure that the serial connection is closed when the class is deleted 
	or the program terminates
	'''
	def __del__(self):
		self.ser.close()

	def set_dev_path(self, path):
		print("Old Device Path: " + self.dev_path)
		old_path = self.dev_path
		try:
			self.ser.close()
			self.ser = serial.Serial(port=str(path), baudrate=600, bytesize=8, parity='N', stopbits=1, timeout=None)
			self.dev_path = str(path)

		except AttributeError:
			self.ser = serial.Serial(port=str(old_path), baudrate=600, bytesize=8, parity='N', stopbits=1, timeout=None)
			self.dev_path = self.ser.name
			print("Invalid Device path: " + path)
			print("Please Use a Valid Device Path: " + self.dev_path)
			pass
		print("New Device Path: " + self.dev_path)
		print("Serial: " + str(self.ser.name) + "\n")

	'''
	Send a STATUS command to the controller, which requests the current azimuth
	and elevation of the rotor. The azimuth, elevation and pulse are then computed,
	the pulse is set and the azimuth, elevation and pulse are returned as a list (first
	element being azimuth, the second being elevation, and the third being pulse).
	'''
	def status(self):
		cmd = ['\x57','\x00','\x00','\x00','\x00','\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x1f', '\x20']
		packet = "".join(cmd)
		
		self.ser.write(str.encode(packet))
		self.ser.flush()

		print(str.encode(packet))

		rec_packet = self.ser.read(12)

		print(rec_packet)

		az = (ord(rec_packet[1]) * 100) + (ord(rec_packet[2]) * 10) + ord(rec_packet[3]) + (ord(rec_packet[4]) / 10) - 360.0
		el = (ord(rec_packet[6]) * 100) + (ord(rec_packet[7]) * 10) + ord(rec_packet[8]) + (ord(rec_packet[9]) / 10) - 360.0
		ph = ord(rec_packet[5])
		pv = ord(rec_packet[10])

		ret = [az, el, ph]

		assert(ph == pv)
		self.pulse = ph

		if(self.debug):
			print("STATUS COMMAND SENT")
			print("Azimuth:   " + str(az))
			print("Elevation: " + str(el))
			print("PH: " + str(ph))
			print("PV: " + str(pv) + "\n")

		return ret

	'''
	Send a STOP command to the controller, which causes the rotor to stop moving and
	return the current azimuth, elevation and pulse of the rotor where it stopped. The
	azimuth, elevation and pulse are then computed, the pulse is set and the azimuth,
	elevation and pulse are returned as a list (first element being azimuth, sencond
	being elevation and the third being pulse).
	'''
	def stop(self):
		cmd = ['\x57','\x00','\x00','\x00','\x00','\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x0f', '\x20']
		packet = "".join(cmd)

		self.ser.write(packet)
		self.ser.flush()

		rec_packet = self.ser.read(12)

		az = (ord(rec_packet[1]) * 100) + (ord(rec_packet[2]) * 10) + ord(rec_packet[3]) + (ord(rec_packet[4]) / 10) - 360.0
		el = (ord(rec_packet[6]) * 100) + (ord(rec_packet[7]) * 10) + ord(rec_packet[8]) + (ord(rec_packet[9]) / 10) - 360.0
		ph = ord(rec_packet[5])
		pv = ord(rec_packet[10])

		ret = [az, el, ph]

		assert(ph == pv)
		self.pulse = ph

		if(self.debug):
			print("STOP COMMAND SENT")
			print("Azimuth:   " + str(az))
			print("Elevation: " + str(el))
			print("PH: " + str(ph))
			print("PV: " + str(pv) + "\n")

		return ret

	'''
	send a SET command to the controller, which causes the rotor to adjust its position
	to the azimuth and elevation specified by the azi and eli parameters respecitvely.
	The azi and eli parameters are floating point values that specify the desired position.
	There is no response to the SET command, thus nothing to return.
	'''
	def set(self, azi, eli):

		assert(float(azi) <= self.max_az)
		assert(float(azi) >= self.min_az)
		assert(float(eli) <= self.max_el)
		assert(float(eli) >= self.min_el)

		az = "0" + str(int(self.pulse * (float(azi) + 360)))
		el = "0" + str(int(self.pulse * (float(eli) + 360)))

		cmd = ['\x57', az[-4], az[-3], az[-2], az[-1], chr(self.pulse), el[-4], el[-3], el[-2], el[-1], chr(self.pulse), '\x2f', '\x20']
		packet = "".join(cmd)

		self.ser.write(packet)
		self.ser.flush()

		if(self.debug):
			print("SET COMMAND SENT")
			print("Sent: " + packet)
			print("Set Azimuth:   " + str(azi) + " (" + str(az) + ")")
			print("Set Elevation: " + str(eli) + " (" + str(el) + ")")
			print("Pulse: " + chr(self.pulse) + "\n")

		time.sleep(1)

	'''
	Calls the STATUS, STOP and SET functions multiple times
	in order to test the rot2proG class functionality
	'''
	def test(self):
		rot = Rot2proG(True)
		rot.status()
		rot.stop()
		rot.set(209, 13)
		rot.status()
		time.sleep(3)
		rot.status()
		time.sleep(10)
		rot.set(19, 144)
		rot.status()
		rot.stop()

	def cmd_mode(self):
		ext=0
		while(ext==0):
			try:
				cmd=str(raw_input("\033[92mrotor\033[0m> ")).strip()
				if cmd == "STATUS" or cmd == "status":
					pos=self.status()
					print("Azimuth:   " + str(pos[0]))
					print("Elevation: " + str(pos[1]))
					print("Pulse: " + str(pos[2]) + "\n")

				elif cmd == "STOP" or cmd == "stop":
					pos=self.stop()
					print("Azimuth:   " + str(pos[0]))
					print("Elevation: " + str(pos[1]))
					print("Pulse: " + str(pos[2]) + "\n")

				elif cmd == "SET" or cmd == "set":
					az=float(raw_input("Azimuth: "))
					el=float(raw_input("Elevation: "))
					try:
						self.set(az, el)
					except AssertionError:
						print("Choose an Azimuth between: " + str(self.min_az) + " - " + str(self.max_az))
						print("Choose an Elevation between: " + str(self.min_el) + " - " + str(self.max_el))
						print("ABORTING")
						pass
					print(" ")

				elif cmd == "DEV" or cmd == "dev" or cmd == "DEVICE" or cmd == "device":
					print("Rotor Controller: SPID Elektronik rot2proG")
					print("Device Path: " + str(self.dev_path))
					print("Protocol: SPID\n")

				elif cmd == "NEW DEVICE" or cmd == "new device":
					path=str(raw_input("Device Path: ")).strip()
					self.set_dev_path(path)
					print(" ")

				elif cmd == "CLEAR" or cmd == "clear":
					clear = lambda : os.system('clear')
					clear()

				elif cmd == "HELP" or cmd == "help":
					self.manual()

				elif cmd == "EXIT" or cmd == "exit":
					clear = lambda : os.system('clear')
					clear()
					ext=1

				else:
					raise ValueError("Not a valid command")

			except ValueError:
				print("Error: unknown command")
				print("Try 'help' for more information")

if __name__ == "__main__":
	rot = Rot2proG()
	rot.status()
	del rot
	print("Done")
