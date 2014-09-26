import re
import binascii
from binascii import a2b_hex, b2a_hex

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

# macros 

@webiopi.macro
def SOSSequence(sequence):
	GPIO.outputSequence(SEQ, 100, sequence)

@webiopi.macro
def serialTX(etat):        #solution bytearray
	data = ""
	dataTx = b''
	
	etat = re.sub('[:]', '', etat)     #typiquement "025402033"
	dataTx = bytearray(etat,"utf-8")	
	dataTx = b'0a' + binascii.b2a_hex(dataTx)  #typiquement b'30323534303230333'
	dataTx += b'0d'
	serial.writeBytes(dataTx) # write a byte array
	webiopi.sleep(1)
	
	if(serial.available() > 0):      #decodage pour tests avec loopback
		datas = serial.readBytes(22) # LF + 9Xdata + CR = 11. X2 = 22
		datas = binascii.a2b_hex(datas)
		data = datas.decode("utf-8")
		#data+=", ".join("0x%X" % i for i in datas)
	return data
	
@webiopi.macro
def serialTXbak(etat):           #solution en string
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
	#return returnData()
	return data
	

@webiopi.macro
def returnData():
	data = ""
	if (serial.available() > 0):
		data = serial.readString()        # read available data as string
	return data
