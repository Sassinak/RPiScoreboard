import re
import subprocess
from subprocess import call, Popen

import webiopi
from webiopi.devices.serial import Serial

GPIO = webiopi.GPIO

serial = Serial("ttyAMA0", 9600)
data = "nada"

#setup called auto at webiopi startup
def setup():
	# empty input buffer before starting processing
	print ("script.py")
	if(serial.available() > 0):
		serial.readString()

def loop():
	#embetee: que mettre ici ? un led "en fonction" qui flashe ?

    webiopi.sleep(1)

# destroy function is called at WebIOPi shutdown
#def destroy():
	

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
	
@webiopi.macro
def shutdown():
	#fermer tout
	print ("macro shutdown")
	command = "/usr/bin/sudo /etc/init.d/webiopi stop"
	proc = subprocess.Popen(command.split(),stdout=subprocess.PIPE)
	print ("macro executed?")
	
@webiopi.macro
def restartServer():
	#repart Webiopi 
	print("macro restart webiopi")
	command = "/usr/bin/sudo /etc/init.d/webiopi restart"
	proc = subprocess.Popen(command.split(),stdout=subprocess.PIPE)
	print ("macro executed?")
	

	
	



	
