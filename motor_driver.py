import can
import cantools
from threading import Thread

class motor_driver():
    def __init__(self, cobid = 0, interface='socketcan', channel='can0', bitrate=500000, dicfile = 'file2.dbc'):
        self.cobid = cobid
        self.interface = interface
        self.channel = channel
        self.bitrate = bitrate
        self.bus = can.ThreadSafeBus(interface= self.interface, channel=self.channel, bitrate=self.bitrate)
        self.dicfile = dicfile
        self.can_db = cantools.database.load_file(dicfile)

        self._base_can_frames = {'motor_config_1' : 1, 'motor_config_2' : 2, 'motor_config_3' : 3, 'motor_out_elec': 4,  
                                 'motor_out _mec' : 5, 'transition': 6, 'motor_sp' : 7}

        self._motor_elec_out ={'Ua': 0.0, 'Ub': 0.0, 'current': 0.0, 'electrical_angle': 0.0}
        self._motor_mec_out ={'shaft_angle': 0.0, 'shaft_angle_sp': 0.0, 'shaft_velocity': 0.0}
        self._transition_table = [[0, 2, 0, 0, 0, 0, 0],[0, 0, 1, 3, 0, 0, 0],
                                  [0, 0, 0, 0, 2, 4, 0], [0, 0, 0, 0, 0, 0, 2]]
        self._states_table = [[1 , 2, 0, 0],[1, 2, 3, 4],
                             [0, 2, 3, 4], [1, 0, 0, 4]]
        print('len ' + str(len(self._transition_table[0])))
        self._motor_states ={'init': 1, 'preoperational': 2, 'running': 3, 'stop': 4}
        self._current_state = 1
        self._gearbox_ratio = 6.0
        self.motor_command_frame = 7 
        self.fsm_transition_frame = 5
        self._motor_position = 0.0
        self.dmesg = self.can_db.encode_message(self.motor_command_frame,{'angle_sp' : 200.0})
        print(self.motor_command_frame)
        self.send_msg(self.motor_command_frame + self.cobid , self.dmesg)
        print("sendede")
        #Thread(target = self.read_bus()).start() #read bus is a blocking fnc, so needs threading
    
    def change_state(self, transition):
        if 1 <= transition <len(self._transition_table[0]):
            if self._transition_table[self._current_state - 1][transition] != 0:
                
                self._current_state = self._transition_table[self._current_state - 1][transition]
                self.send_msg(self.motor_command_frame + self.cobid , [transition])
                
            else:
             print('Incorrect transition')
    def send_config_1(self, P_controller = 2.0, I_controller = 0.01, D_controller = 0):
        real_frame = self.cobid + self._base_can_frames['motor_config_1']
        canConfig1 = self.can_db.encode_message(self._base_can_frames['motor_config_1'],{'P_control' : P_controller,
                                                                                         'I_control': I_controller,  'D_control' : D_controller})
        self.send_msg(real_frame ,canConfig1)
        
    def send_config_2(self, P_vel = 2.0, I_vel = 0.01, D_vel = 0, Vel_lim  = 20.0):
        real_frame = self.cobid + self._base_can_frames['motor_config_2']
        canConfig2 = self.can_db.encode_message(self._base_can_frames['motor_config_2'],{'P_vel' : P_vel, 
                                                                                         'I_vel': I_vel,  'D_vel' : D_vel,  'Vel_lim' : Vel_lim})
        self.send_msg(real_frame ,canConfig2)
        
    def send_config_3(self, Volt_lim = 20.0, V_aling = 7.0, Calibrate = 0, Zero_angle_elec  = 0.0):
        real_frame = self.cobid + self._base_can_frames['motor_config_3']
        canConfig3 = self.can_db.encode_message(self._base_can_frames['motor_config_3'],{'Volt_lim' : Volt_lim, 'V_aling': V_aling,  
                                                                                         'Calibrate' : Calibrate,  'Zero_angle_elec' : Zero_angle_elec})
        self.send_msg(real_frame ,canConfig3)
    def send_transition(self, transition = 0):
        real_frame = self.cobid + self._base_can_frames['transition']
        canConfig3 = self.can_db.encode_message(self._base_can_frames['transition'],{'Transition' : transition})
        self.send_msg(real_frame ,canConfig3)
    def send_command(self, angle):
        print('cur_state ' +str(self._current_state))
        if  self._current_state == self._motor_states['running']: 
            angle = angle*self._gearbox_ratio
            encoded_message = self.can_db.encode_message(self.motor_command_frame ,{'angle_sp' : angle})
            self.send_msg(self.motor_command_frame + self.cobid , encoded_message)
        else:
            print('Only send commands on running mode!')
            
    def get_motor_angle(self):
        return self._motor_mec_out["shaft_angle"]/self._gearbox_ratio
    
    def read_bus(self):
        while True:
            msg = self.bus.recv(1)
            if msg is not None:
                    pass
                    #self.send_msg(0x001, self.dmesg)

                    print(msg)
                    #self.can_db.decode_message(msg.arbitration_id-self.cobid, msg.data)

                    try:
                        print(msg.arbitration_id-self.cobid)
                        print(self._base_can_frames["motor_out_elec"])
                        if (msg.arbitration_id-self.cobid) == self._base_can_frames["motor_out_elec"]:
                            print('rec motor elec')
                            self._motor_elec_out = self.can_db.decode_message((msg.arbitration_id-self.cobid), msg.data)
                            print(self._motor_elec_out )
                        elif (msg.arbitration_id-self.cobid) == self._base_can_frames["motor_out_mec"]:
                            print('rec motor mec')
                            self._motor_mec_out = self.can_db.decode_message((msg.arbitration_id-self.cobid), msg.data)
                            print(self._motor_mec_out )

                    except:
                        print("Error reading can message")

    def send_msg(self,frame,msg):
        msg = can.Message(arbitration_id=frame, data=msg, is_extended_id=False)
        try:
            self.bus.send(msg)
        except (ValueError, TypeError) as e:
            print("Wrong CAN message data: " +  str(e))
        except can.CanError as e:
            print(" Failed to send CAN message: " + str(e))
            
    def close_bus(self):
        self.bus.shutdown()
        
    def init_motor(self, P_controller = 1.0, I_controller = 0.01, 
                   D_controller = 0, Volt_limit = 20):
        init_cobid = self.base_can_frames['toInit'] + self.cobid
        msg = self.can_db.encode_message(0x1,{'position' : 10,'speed': 13,  'FB3' : 0})
        self.send_msg(init_cobid, msg)
        pass
    
    def preop_motor(self, is_calibrated = False, direction = 1, 
                   D_controller = 0, Volt_limit = 20):
        pass       
    
    def prueba(self, fuera = 'dentro'):
        print(fuera)

if __name__ == '__main__':
    print('Hola')
    motor = motor_driver(cobid = 0, channel='can0')
    print(motor.cobid)
    motor.send_config_1(P_controller=300.0, I_controller=0.1,D_controller=0.0)
    motor.send_config_2()
    motor.send_config_3()
    motor.send_transition(1)
    motor.change_state(1)
    motor.send_transition(3)
    motor.change_state(3)

    motor.send_command(20.0)
    print("mode " + str(motor._current_state))
    motor.close_bus()
    #motor.send_command(15.3)
    #while True:
    #    x = input()
    #    motor.change_state(int(x))
    #    print("mode " + str(motor._current_state))
    #motor.close_bus()
    #motor.prueba()