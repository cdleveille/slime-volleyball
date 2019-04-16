#!/usr/bin/env python

"""
A module for getting input from Microsoft XBox 360 controllers via the XInput library on Windows.

Adapted from Jason R. Coombs' code here:
http://pydoc.net/Python/jaraco.input/1.0.1/jaraco.input.win32.xinput/
under the MIT licence terms

Upgraded to Python 3
Modified to add deadzones, reduce noise, and support vibration
Only req is Pyglet 1.2alpha1 or higher:
pip install --upgrade http://pyglet.googlecode.com/archive/tip.zip 
"""

import ctypes, sys, time
from operator import itemgetter, attrgetter
from itertools import count, starmap

# structs according to
# http://msdn.microsoft.com/en-gb/library/windows/desktop/ee417001%28v=vs.85%29.aspx

class XINPUT_GAMEPAD(ctypes.Structure):
	_fields_ = [
		('buttons', ctypes.c_ushort),  # wButtons
		('left_trigger', ctypes.c_ubyte),  # bLeftTrigger
		('right_trigger', ctypes.c_ubyte),  # bLeftTrigger
		('l_thumb_x', ctypes.c_short),  # sThumbLX
		('l_thumb_y', ctypes.c_short),  # sThumbLY
		('r_thumb_x', ctypes.c_short),  # sThumbRx
		('r_thumb_y', ctypes.c_short),  # sThumbRy
	]

class XINPUT_STATE(ctypes.Structure):
	_fields_ = [
		('packet_number', ctypes.c_ulong),  # dwPacketNumber
		('gamepad', XINPUT_GAMEPAD),  # Gamepad
	]

class XINPUT_VIBRATION(ctypes.Structure):
	_fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
				("wRightMotorSpeed", ctypes.c_ushort)]

class XINPUT_BATTERY_INFORMATION(ctypes.Structure):
	_fields_ = [("BatteryType", ctypes.c_ubyte),
				("BatteryLevel", ctypes.c_ubyte)]

xinput = ctypes.windll.xinput1_4
#xinput = ctypes.windll.xinput9_1_0  # this is the Win 8 version ?
# xinput1_2, xinput1_1 (32-bit Vista SP1)
# xinput1_3 (64-bit Vista SP1)

def get_bit_values(number, size=32):
	"""
	Get bit values as a list for a given number

	>>> get_bit_values(1) == [0]*31 + [1]
	True

	>>> get_bit_values(0xDEADBEEF)
	[1L, 1L, 0L, 1L, 1L, 1L, 1L, 0L, 1L, 0L, 1L, 0L, 1L, 1L, 0L, 1L, 1L, 0L, 1L, 1L, 1L, 1L, 1L, 0L, 1L, 1L, 1L, 0L, 1L, 1L, 1L, 1L]

	You may override the default word size of 32-bits to match your actual
	application.
	>>> get_bit_values(0x3, 2)
	[1L, 1L]

	>>> get_bit_values(0x3, 4)
	[0L, 0L, 1L, 1L]
	"""
	res = list(gen_bit_values(number))
	res.reverse()
	# 0-pad the most significant bit
	res = [0] * (size - len(res)) + res
	return res


def gen_bit_values(number):
	"""
	Return a zero or one for each bit of a numeric value up to the most
	significant 1 bit, beginning with the least significant bit.
	"""
	number = int(number)
	while number:
		yield number & 0x1
		number >>= 1

ERROR_DEVICE_NOT_CONNECTED = 1167
ERROR_SUCCESS = 0

class XInputJoystick():

	max_devices = 4

	def __init__(self, device_number, normalize_axes=True):
		values = vars()
		del values['self']
		self.__dict__.update(values)

		super(XInputJoystick, self).__init__()

		self._last_state = self.get_state()
		self.received_packets = 0
		self.missed_packets = 0

		# Set the method that will be called to normalize
		#  the values for analog axis.
		choices = [self.translate_identity, self.translate_using_data_size]
		self.translate = choices[normalize_axes]

	def translate_using_data_size(self, value, data_size):
		# normalizes analog data to [0,1] for unsigned data
		#  and [-0.5,0.5] for signed data
		data_bits = 8 * data_size
		return float(value) / (2 ** data_bits - 1)

	def translate_identity(self, value, data_size=None):
		return value

	def get_state(self):
		"Get the state of the controller represented by this object"
		state = XINPUT_STATE()
		res = xinput.XInputGetState(self.device_number, ctypes.byref(state))
		if res == ERROR_SUCCESS:
			return state
		if res != ERROR_DEVICE_NOT_CONNECTED:
			raise RuntimeError(
				"Unknown error %d attempting to get state of device %d" % (res, self.device_number))
		# else return None (device is not connected)

	def is_connected(self):
		return self._last_state is not None

	@staticmethod
	def enumerate_devices():
		"Returns the devices that are connected"
		devices = list(
			map(XInputJoystick, list(range(XInputJoystick.max_devices))))
		return [d for d in devices if d.is_connected()]

	def set_vibration(self, left_motor, right_motor):
		"Control the speed of both motors seperately"
		# Set up function argument types and return type
		XInputSetState = xinput.XInputSetState
		XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
		XInputSetState.restype = ctypes.c_uint

		vibration = XINPUT_VIBRATION(
			int(left_motor * 65535), int(right_motor * 65535))
		XInputSetState(self.device_number, ctypes.byref(vibration))

	def update_packet_count(self, state):
		"Keep track of received and missed packets for performance tuning"
		self.received_packets += 1
		missed_packets = state.packet_number - \
			self._last_state.packet_number - 1
		self.missed_packets += missed_packets

	def pollLeftStick(self, deadzone):
		state = self.get_state()
		if not state:
			return None
		val = getattr(state.gamepad, "l_thumb_x")
		val = self.translate(val, 2)
		if abs(val) > deadzone:
				return val * 2
		return 0.0

	def pollButtonA(self):
		state = self.get_state()
		if not state:
			return None
		buttons_state = get_bit_values(state.gamepad.buttons, 16)
		return buttons_state[3]