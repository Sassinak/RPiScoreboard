import re

import webiopi
from webiopi.devices.serial import Serial

GPIO = webiopi.GPIO

serial = Serial("ttyAMA0", 9600)
data = "niet"

#setup called auto at webiopi startup
def setup():
	# empty input buffer before starting processing
	if(serial.available() > 0):
		serial.readString()

def loop():
	#embetee: que mettre ici ? un led "en fonction" qui flashe ?

    webiopi.sleep(5)

# destroy function is called at WebIOPi shutdown
#def destroy():   ???


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
