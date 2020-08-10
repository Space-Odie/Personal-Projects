#Title:Greener_Pi
#By: Ian O'Donnell
#Date: 8/9/20

#Inputs: Moisture Sensor
#Outputs: LEDs

#Imports
import RPi.GPIO as GPIO
import time
import spidev

#initialize Pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
delay = 0.5

#initialize LED
LED = 7
GPIO.setup(LED, GPIO.OUT, initial = GPIO.LOW)
LED_State = GPIO.input(LED)

#Initialize Moisture Sensor 
Moisture_Sensor = 0
spi = spidev.SpiDev()
spi.open(0, 0)
Dry = 400
Moist = 500
State_Change = []

#read analog to digital convertor
def adc_handler(adcnum):
	if adcnum > 7 or adcnum < 0:
		return -1
	r = spi.xfer2([1, 8 + adcnum <<4, 0])
	data = ((r[1] & 3) << 8) + r[2]
 	
	time.sleep(delay)
	return data

#print out values for user
def PrintOut(State_Change, Status, analog_value):
	if State_Change == True:
		print('Light is now ON' if LED_State == True 
		else 'Light is now OFF')
	print('---------------------')
	print('Analog Value is: {}\n Status is: {}'.format(analog_value, Status))
	time.sleep(5)

def get_analog_value():
	return  adc_handler(Moisture_Sensor)

def main():
	while True:	#always run
	#TODO Configure DeadBand + Dry / Moist Levels
		analog_value = get_analog_value()

		if analog_value <= Dry:
			GPIO.output(LED, GPIO.HIGH) #Turn on LED
			Status = 'Dry'
			State_Change = 1

			while analog_value < Moist: #Run until Moist
				PrintOut(State_Change, Status, analog_value)
				State_Change = 0
				get_analog_value()

		if analog_value >= Moist:
			GPIO.output(LED, GPIO.LOW) #Turn off LED
			Status = 'Moist'
			State_Change = 1

			while analog_value > Dry: #Run until Dry
				PrintOut(State_Change, Status, analog_value)
				State_Change = 0
				get_analog_value()

#GPIO.add_event_detect(LED, GPIO.BOTH) ## Not using this callback method

if __name__== '__main__': main()
