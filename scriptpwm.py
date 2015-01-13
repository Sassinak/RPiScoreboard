# imports 
import re
import time
import webiopi
from webiopi.devices.serial import Serial

#Enable debug output
#webiopi.setDebug()

#retrieve GPIO lib
GPIO = webiopi.GPIO

LED0 = 2

serial = Serial("ttyAMA0", 9600)
data = "niet"

#setup called auto at webiopi startup
def setup():
	# empty input buffer before starting processing
	if(serial.available() > 0):
		serial.readString()
	#PWN tests
	GPIO.setFunction(LED0, GPIO.PWM)
	GPIO.pwmWrite(LED0, 0.5)	# set to 50% ratio

def loop():
	#PWM tests
	GPIO.pwmWrite(LED0, 0.90)
	#webiopi.sleep(0.25)
	GPIO.pwmWrite(LED0, 0.30)
	#webiopi.sleep(0.2)
	GPIO.pwmWrite(LED0, 0.70)
	webiopi.sleep(0.2)
    
    
# destroy function is called at WebIOPi shutdown
def destroy():
	GPIO.setFunction(LED0, GPIO.IN)


# macro 
	
@webiopi.macro
def serialTX(etat):           #solution en string
	
	# flush input buffer before starting processing
	if(serial.available() > 0):
		serial.readString()
		
	etat = re.sub('[:]', '', etat)
	
	txdata = "\n"		# LF ici (10 ou 0xA)	
	txdata += etat
	txdata += "\r"		# CR (13 ou 0xD)
	serial.writeString(txdata)       # write as string

	data = "niet"					#pour feedback visuel
	webiopi.sleep(0.25)				#sinon delai dans les donnees, bizarre
	
	if (serial.available() > 0):
		data = serial.readString()        # read available data as string
	
	return data
	
#a faire si approved : une sortie directement en PWM (si Pi assez puissant)
