from pymavlink import mavutil
import time
master1 = mavutil.mavlink_connection('udp:0.0.0.0:7777', source_system=1)

while True:
	master1.mav.heartbeat_send(1,1,1,1,1)
	master1.mav.global_position_int_send(
	0,
	38.750565 * 1e7,
	-77.445863 * 1e7,
	0,
	0,
	0,
	0,
	0,
	50)
	master1.mav.gps_raw_int_send(
	0,
	3,
	38.750565 * 1e7,
	-77.445863 * 1e7,
	0,
	1,
	1,
	0,
	50,
	6)
	master1.mav.scaled_pressure_send(
		0,
		0,
		0,
		0)
	time.sleep(1)
