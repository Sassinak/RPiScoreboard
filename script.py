import re
import webiopi
from webiopi.devices.serial import Serial

GPIO = webiopi.GPIO
LIGHT = 11 #GPIO pin using BCM numbering
SEQ = 9

serial = Serial("ttyAMA0", 9600)
data = "niet"

#sequence = '01010100110011001100101010'

#setup called auto at webiopi startup
def setup():
	#set the GPIO used by the light to output
	GPIO.setFunction(LIGHT, GPIO.OUT)
	#GPIO.setFunction(SEQ, GPIO.OUT)
	GPIO.digitalWrite(LIGHT, GPIO.HIGH)
	#GPIO.digitalWrite(SEQ, GPIO.HIGH)

	# empty input buffer before starting processing
	while (serial.available() > 0):
		serial.readString()

def loop():
	# Toggle LED each 5 seconds
    value = not GPIO.digitalRead(LIGHT)
    GPIO.digitalWrite(LIGHT, value)

    webiopi.sleep(5)

# destroy function is called at WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(LIGHT, GPIO.LOW)
    GPIO.digitalWrite(SEQ, GPIO.LOW)


# macros sequence
@webiopi.macro
def SOSSequence(sequence):
	GPIO.outputSequence(SEQ, 100, sequence)

@webiopi.macro
def serialTX(etat):
	txdata = "LF "		# LF ici (10 ou 0xA)
	txString = re.sub('[:]', '', etat)
	for c in txString:
		txdata += str(int(c) + 30); #extraire int, ajouter 30, ajouter a la string
		txdata += " "
	txdata += "CR"		# CR (13 ou 0xD)
	serial.writeString(txdata)       # write a string

	data = ""
	webiopi.sleep(1)				#sinon delai dans les donnees, bizarre
	if (serial.available() > 0):
		data = serial.readString()        # read available data as string
	return data
	#return returnData()

@webiopi.macro
def returnData():
	data = ""
	if (serial.available() > 0):
		data = serial.readString()        # read available data as string
	return data
