from pymavlink import mavutil
import time
master1 = mavutil.mavlink_connection('udpbcast:0.0.0.0:14550', source_system=1)
master2 = mavutil.mavlink_connection('udpbcast:0.0.0.0:14550', source_system=2)

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
	master2.mav.heartbeat_send(2,1,1,1,1)
	master2.mav.global_position_int_send(
	0,
	38.750667 * 1e7,
	-77.445565 * 1e7,
	0,
	0,
	0,
	0,
	0,
	0)
	master2.mav.gps_raw_int_send(
	0,
	3,
	38.750667 * 1e7,
	-77.445865 * 1e7,
	0,
	1,
	1,
	0,
	0,
	7)
	time.sleep(1)
