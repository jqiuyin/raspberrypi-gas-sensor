import RPi.GPIO as GPIO
import time

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
def main():
    init()
    print("please wait...")
    time.sleep(20)
    while True:
        raw_date=readadc(mq7_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
        
        if GPIO.input(mq7_dpin):
            print("not leak")
            time.sleep(0.5)
        else:
            voltage=(raw_date/1024.)*5
            print("Current AD vaule = " +str("%.2f"%(voltage)+" V"))
            if voltage > 2.0:
                GPIO.output(led_pin, GPIO.HIGH)
            else:
                GPIO.output(led_pin, GPIO.LOW)
            time.sleep(0.5)

if __name__ =='__main__':
    try:
        main()
        pass
    except KeyboardInterrupt:
        pass

GPIO.cleanup()
         
         