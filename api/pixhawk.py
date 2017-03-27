#!/usr/bin/python -u

from flask import jsonify
import serial.tools.list_ports
from terminalprocess import TerminalProcess
import threading



from pymavlink import mavutil
import time

class PixhawkMonitor(threading.Thread):
	def __init__(self, run_event):
		threading.Thread.__init__(self)
		self.run_event = run_event
		self.process = None
		self.readout = ''
		#self.pixhawk_master = mavutil.mavlink_connection('udpin:0.0.0.0:7777', source_system=10)
		self.pixhawk_master = mavutil.mavlink_connection('/dev/ttyACM0', source_system=10)
		self.pixhawk_master.mav.set_callback(self.master_callback, self.pixhawk_master)
		
		if hasattr(self.pixhawk_master.mav, 'set_send_callback'):
			self.pixhawk_master.mav.set_send_callback(self.master_send_callback, self.pixhawk_master)
		
		self.depth = 0


	def master_callback(self, m, master):
		'''process mavlink message m on master, sending any messages to recipients'''
		
		mtype = m.get_type()
				
		if mtype == "SCALED_PRESSURE2":
			self.depth = m.press_abs
			print 'hi'


	def master_send_callback(self):
		return
	
	def get_depth(self):
		return self.depth
		
		
	def mavlink_process(self):
		'''process packets from the MAVLink master'''
		try:
			s = self.pixhawk_master.recv(16*1024)
		except Exception:
			time.sleep(0.1)
			return
		# prevent a dead serial port from causing the CPU to spin. The user hitting enter will
		# cause it to try and reconnect
		if len(s) == 0:
			time.sleep(0.1)
			return
		
		msgs = self.pixhawk_master.mav.parse_buffer(s)


	def run(self):
		while self.run_event.is_set():
			try:
				self.mavlink_process()
			except (KeyboardInterrupt, SystemExit):
				self.run_event.clear()