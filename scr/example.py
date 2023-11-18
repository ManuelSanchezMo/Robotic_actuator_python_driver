import motor_driver 
if __name__ == '__main__':
    motor = motor_driver.motor_driver(cobid = 10, channel='can0')
    print(motor.cobid)
    motor.send_config_1(P_controller=300.0, I_controller=0.1,D_controller=0.0)
    print('conse')
    motor.send_config_2()
    motor.send_config_3()
    motor.send_transition(1)
    motor.change_state(1)
    motor.send_transition(3)
    motor.change_state(3)

    motor.send_command(20.0)
    print("mode " + str(motor._current_state))
    motor.send_command(15.3)
    #motor.close_bus()
    while True:
        #pass
        #x = input()
        #motor.change_state(int(x))
        print("mode " + str(motor._current_state))  
        print(motor.motor_mec_out)
        print(motor.motor_elec_out)

    #motor.close_bus()
    #motor.prueba()