#codkevin, lineas iniciales:230, ahora:144
import uros
from arlo_control_msgs import WheelsEncoders  # rosserial messages
from arlorobot import ArloRobot
import utime
import gc
from machine import Pin, ADC
import network
import _thread
from std_msgs import Float32, Bool
import machine

gc.enable()

"""
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect("covibot", "covibot1")
        while not wlan.isconnected():
            pass
"""
#do_connect()

utime.sleep(5)

class ArlorobotMove(object):
    def __init__(self):

        utime.sleep(1)

        # constants
        self.WHEEL_VELOCITY_TOPIC = "/wheels_vel"
        self.ESP_VELOCITY_TOPIC ="/esp_velocity"
        self.arlobot = ArloRobot(serial_id=2, baudrate=19200, tx=17, rx=16, pace=2)
        self.node = uros.NodeHandle(1, 115200, tx=1, rx=3)
        #self.node = uros.NodeHandle(1, 115200, tx=17, rx=16)
        # , tx=1, rx=3
        self.left_power = 0
        self.right_power = 0

        self.last_left_power = 0
        self.last_right_power = 0
        self.real_left_encoder = 0.0
        self.real_right_encoder = 0.0
        self.real_velocity = Float32()
    def wheel_velocity_callback(self, msg):
        self.left_power = msg.left_encoder
        self.right_power = msg.right_encoder
        self.left_power = int(self.left_power)
        self.right_power = int(self.right_power)

        if (
            self.last_left_power != self.left_power
            or self.last_right_power != self.right_power
        ):
            self.last_left_power = self.left_power
            self.last_right_power = self.right_power

        if self.left_power > 120:
            self.left_power = 120
        elif self.left_power < -120:
            self.left_power = -120

        if self.right_power > 120:
            self.right_power = 120
        elif self.right_power < -120:
            self.right_power = -120

    def process_list(self,input_list):
        if len(input_list) == 2:
            try:
                self.real_left_encoder = float(input_list[0])
                self.real_right_encoder = float(input_list[1])
                #print("Both elements can be converted to float:", input_list)
            except Exception as e:
                self.real_left_encoder = 1.0
                self.real_right_encoder = 1.0
                #print(f"Exception encountered: {e}")
        else:
            self.real_left_encoder = 1.0
            self.real_right_encoder = 1.0

    def start(self):  # threads init and running
        self.arlobot.clear_counts()
        self.node.subscribe(
            self.WHEEL_VELOCITY_TOPIC, WheelsEncoders, self.wheel_velocity_callback
        )
        self.arlobot.set_kp_constant(100)
        self.arlobot.set_ki_constant(80)
        #self.arlobot.go_speed(0,0)
        while True:
            #self.left_power, self.right_power

            #self.real_encoders.left_encoder = float(lectura[0])
            #self.real_encoders.right_encoder = float(lectura[1])
            #self.real_left_encoder.data = 15.9

            self.arlobot.go_speed(self.left_power, self.right_power)
            raw_velocity = self.arlobot.read_speeds()
            self.process_list(raw_velocity)
            #self.process_list(self.arlobot.read_speeds())
            left_vel = self.real_left_encoder / 300
            right_vel = self.real_right_encoder / 300
            self.real_velocity.data = float((left_vel + right_vel) * 0.5)
            #self.node.publish(self.ESP_VELOCITY_TOPIC,self.real_velocity)
            utime.sleep_ms(100)

my_arlobot = ArlorobotMove()

my_arlobot.start()

