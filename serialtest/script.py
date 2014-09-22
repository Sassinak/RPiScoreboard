import webiopi
from webiopi.devices.serial import Serial

serial = Serial("ttyAMA0", 9600)

def loop():
    serial.writeByte(0xFF)                # write a single byte
    serial.writeBytes([0x01, 0x02, 0xFF]) # write a byte array
    serial.writeString("some text")       # write a string

    if (serial.available() > 0):
        value = serial.readByte()         # read and return a single byte
        print("0x%X" % value)

        values = serial.readBytes(3)      # read 3 bytes and return an array
        print(", ".join("0x%X" % i for i in values))

        data = serial.readString()        # read available data as string
        print(data)

    webiopi.sleep(1)
