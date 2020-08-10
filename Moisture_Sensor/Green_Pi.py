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
delay = 1.5

#initialize GREEN LED (Moist, L1)
L1 = 7
GPIO.setup(L1, GPIO.OUT, initial = GPIO.LOW)


#initialize RED LED (DRY, L2)
L2 = 11
GPIO.setup(L2, GPIO.OUT, initial = GPIO.LOW)


#initialize Moisture Sensor 
Moisture_Sensor = 0
spi = spidev.SpiDev()
spi.open(0, 0)
Dry = 400
Moist = 500
State_Change = []

#read analog to digital convertor
def ADC_Handler(adcnum):
	if adcnum > 7 or adcnum < 0:
		return -1
	r = spi.xfer2([1, 8 + adcnum <<4, 0])
	data = ((r[1] & 3) << 8) + r[2]
 	
	time.sleep(delay)
	return data

#print out values for user
def PrintOut(State_Change, Status, moisture_level):
	if State_Change == True:
	
		print('Green Light is now ON' if GPIO.input(L1) == True 
		else 'Green Light is now OFF')

		print('Red Light is now ON' if GPIO.input(L2) == True
		else 'Red Light is now OFF')

	print('---------------------')
	print('Moisture Value is: {}\n Status is: {}'.format(moisture_level, Status))
	time.sleep(delay)

def Get_Analog_Value():
	return  ADC_Handler(Moisture_Sensor)

def main():
	while True:	#always run
	#TODO Configure DeadBand + Dry / Moist Levels
		Moisture_Level = Get_Analog_Value()

		if Moisture_Level <= Dry:
			GPIO.output(L2, GPIO.HIGH) #Turn on Dry LED 
			GPIO.output(L1, GPIO.LOW)  #Turn off Moist LED
			Status = 'Dry'
			State_Change = 1

			while Moisture_Level < Moist: #Run until Moist
				PrintOut(State_Change, Status, Moisture_Level)
				State_Change = 0
				Moisture_Level = Get_Analog_Value()

		if Moisture_Level >= Moist:
			GPIO.output(L2, GPIO.LOW)  #Turn off Dry LED
			GPIO.output(L1, GPIO.HIGH) #Turn on Moist LED
			Status = 'Moist'
			State_Change = 1

			while Moisture_Level > Dry: #Run until Dry
				PrintOut(State_Change, Status, Moisture_Level)
				State_Change = 0
				Moisture_Level = Get_Analog_Value()


if __name__== '__main__': main()
