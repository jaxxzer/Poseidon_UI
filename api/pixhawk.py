#!/usr/bin/python -u

from flask import jsonify
import serial.tools.list_ports
from terminalprocess import TerminalProcess


from pymavlink import mavutil
import time

class PixhawkMonitor:
	def __init__(self):
		self.process = None
		self.readout = ''
		pixhawk_master = mavutil.mavlink_connection('udpin:0.0.0.0:7777', source_system=10)
		pixhawk_master.mav.set_callback(self.master_callback, pixhawk_master)
		
		if hasattr(pixhawk_master.mav, 'set_send_callback'):
			pixhawk_master.mav.set_send_callback(self.master_send_callback, pixhawk_master)
		
		self.depth = 0

	def master_callback(self):
		print 'sup'
		'''process mavlink message m on master, sending any messages to recipients'''
		
		mtype = m.get_type()
		
		print mtype
		
		if mtype == "SCALED_PRESSURE":
			self.depth = m.press_abs


	def master_send_callback(self):
		return
	
	def get_depth(self):
		return self.depth
		
	def device(self):
		ports = serial.tools.list_ports.comports()
		for port in ports:
			if port[1].find("PX4") != -1:
				return port
		return ['','','']

	def start(self):
		port = self.device()[0]
		cmd = "mavproxy.py --master "+port+",115200" # --out udpin:localhost:9000 --out udpbcast:192.168.2.255:14550"
		self.process = TerminalProcess()
		self.process.run(cmd)

	def status(self):
		if self.process is not None:
			if self.process.running():
				self.readout += self.process.read()

		status = ''
		board = self.device()[1]

		if self.readout.find("Ready to FLY") != -1:
			status = "Ready to Dive"
		else:
			status = "Initializing"

		i = self.readout.find("ArduSub V")
		eol = self.readout.find('\n',i)
		if i != -1:
			firmware = self.readout[i:eol]
		else:
			firmware = "Unknown firmware"

		i = self.readout.find("Frame")
		eol = self.readout.find('\n',i)
		if i != -1:
			frame = self.readout[i+7:eol]
		else:
			frame = "Unknown frame type"

		#print [board,firmware,frame,status]
		return {"board":board,"firmware":firmware,"frame":frame,"status":status}

	def stop(self):
		self.process.kill()
		
	def process(self):
		'''process packets from the MAVLink master'''
		print ('hey')
		#try:
		s = self.pixhawk_master.recv(16*1024)
			#		 except Exception:
			#			 time.sleep(0.1)
			#			 return
		# prevent a dead serial port from causing the CPU to spin. The user hitting enter will
		# cause it to try and reconnect
		if len(s) == 0:
			time.sleep(0.1)
			return
		
		
		
		msgs = self.pixhawk_master.mav.parse_buffer(s)
		
		for msg in msgs:
			print 'msg: %s' %msg.get_type()

if __name__ == "__main__":
	import time
	px = PixhawkMonitor()
	#px.start()
	loops = 0
	while loops < 30:
		loops += 1
		print px.update()
		time.sleep(1)
	px.stop()