import motor_driver

motor = motor_driver(cobid = 3, channel='vcan0')
while True:
	x = input()
	motor.change_state(x)
