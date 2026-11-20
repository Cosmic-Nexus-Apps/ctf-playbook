#!/usr/bin/env python3
"""Sign MAVLink2, arm, take off and fly to a target (ArduPilot SITL).

Usage:
  python mavlink_signed.py <host> <key_hex_64chars> <lat> <lon> <alt_m>

The drone only accepts signed commands when signing is enabled; without
setup_signing() every arm/mission/param command is silently ignored.
"""
import sys
import time
from pymavlink import mavutil

host = sys.argv[1]
key = bytes.fromhex(sys.argv[2])
lat = float(sys.argv[3])
lon = float(sys.argv[4])
alt = float(sys.argv[5])

m = mavutil.mavlink_connection("udpout:%s:14550" % host)
m.mav.heartbeat_send(6, 8, 0, 0, 0)
print("waiting for vehicle heartbeat...")
while True:
    hb = m.recv_match(type="HEARTBEAT", blocking=True, timeout=15)
    if hb and hb.get_srcSystem() == 1:
        print("connected: system", m.target_system, "component", m.target_component)
        break

m.setup_signing(key)
print("signing key loaded")

# GUIDED mode (ArduCopter custom mode 4)
m.mav.set_mode_send(m.target_system,
                    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 4)
time.sleep(1)

m.mav.command_long_send(m.target_system, m.target_component,
                        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
                        1, 0, 0, 0, 0, 0, 0)
time.sleep(2)
m.mav.command_long_send(m.target_system, m.target_component,
                        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,
                        0, 0, 0, 0, 0, 0, alt)
time.sleep(5)

m.mav.set_position_target_global_int_send(
    0, m.target_system, m.target_component,
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
    0b0000111111111000, int(lat * 1e7), int(lon * 1e7), alt,
    0, 0, 0, 0, 0, 0, 0, 0)

t0 = time.time()
while time.time() - t0 < 180:
    msg = m.recv_match(blocking=True, timeout=2)
    if not msg:
        continue
    if msg.get_type() == "STATUSTEXT":
        text = str(msg.text)
        print("STATUSTEXT:", text)
        if "FLAG{" in text:
            break
