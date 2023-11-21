import motor_driver 
import numpy as np
if __name__ == '__main__':
    motor = motor_driver.motor_driver(cobid = 10, channel='vcan0')
    print(motor.cobid)
    motor.send_config_1(P_controller=300.0, I_controller=0.1,D_controller=0.0)
    motor.send_config_2( P_vel = 2.0, I_vel = 0.01, D_vel = 0, Vel_lim  = 20.0)  
    motor.send_config_3( Volt_lim = 20.0, V_aling = 7.0, Calibrate = 0, Zero_angle_elec  = 0.0)
    motor.send_transition(1)
    motor.send_transition(3)
    x = np.linspace(1, 10, num=10)
    y = np.sin(x)
    for n in range(y.size):
        print(n)
        motor.send_command(y[n])
        print(motor.motor_mec_out)
        print(motor.motor_elec_out)
    print('ended')
    motor.shutdown()
