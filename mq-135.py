import RPi.GPIO as GPIO
import time
import random
from paho.mqtt import client as mqtt_client
import os

DEV_MODE = os.environ.get('DEV_MODE', 'false').lower() in ['true', 'on', '1']

broker = '127.0.0.1'  # mqtt代理服务器地址
port = 1883
keepalive = 60     # 与代理通信之间允许的最长时间段（以秒为单位）              
topic = "/python/mqtt"  # 消息主题
client_id = f'python-mqtt-pub-{random.randint(0, 1000)}'  # 客户端id不能重复

def connect_mqtt():
    '''连接mqtt代理服务器'''
    def on_connect(client, userdata, flags, rc):
        '''连接回调函数'''
        # 响应状态码为0表示连接成功
        if rc == 0:
            print("Connected to MQTT OK!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # 连接mqtt代理服务器，并获取连接引用
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port, keepalive)
    return client

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq7_dpin = 26
mq7_apin = 0
led_pin = 21

#port init
def init():
    GPIO.setwarnings(False)
    GPIO.cleanup()			#clean up at the end of your script
    GPIO.setmode(GPIO.BCM)		#to specify whilch pin numbering system
    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(mq7_dpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, GPIO.LOW)

#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)	

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
                GPIO.output(mosipin, True)
        else:
                GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
                adcout |= 0x1

    GPIO.output(cspin, True)
    
    adcout >>= 1       # first bit is 'null' so drop it
    return adcout
#main ioop
def publish(client):
    while True:
        time.sleep(1)
        if DEV_MODE:
            voltage = round(random.uniform(0, 5), 2)
            info = {
                'timestamp': time.time(),
                'current_ad_value': str("%.2f"%(voltage)+" V")
            }
            client.publish(topic, info)
            continue
        raw_date=readadc(mq7_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
        if GPIO.input(mq7_dpin):
            print("not leak")
        else:
            voltage=(raw_date/1024.)*5
            print("Current AD vaule = " +str("%.2f"%(voltage)+" V"))
            info ={
                 'timestamp': time.time(),
                 'current_ad_value': str("%.2f"%(voltage)+" V")
            }
            client.publish(topic, info)
            if voltage > 2.0:
                GPIO.output(led_pin, GPIO.HIGH)
            else:
                GPIO.output(led_pin, GPIO.LOW)

def run():
    '''运行发布者'''
    client = connect_mqtt()
    # 运行一个线程来自动调用loop()处理网络事件, 非阻塞
    client.loop_start()
    publish(client)

if __name__ =='__main__':
    try:
        init()
        print("please wait...")
        time.sleep(20)
        run()
        pass
    except KeyboardInterrupt:
        pass

GPIO.cleanup()
         
         