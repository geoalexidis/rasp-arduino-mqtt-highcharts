# ChallProj 2
# Only works with I2C Module attached
# Make sure to install first pip install paho-mqtt
# For more info visit https://pypi.python.org/pypi/paho-mqtt/1.1
#--------------------------------------
import smbus
import time
import serial # um serial input zu lesen
import RPi.GPIO as GPIO  # gpio einzulesen
import paho.mqtt.publish as publish # mqtt publisher library

GPIO.setmode(GPIO.BCM) # modus bcm oder board, pin belegungs art
GPIO.setup(26, GPIO.OUT) # pin 26 genommen als autput für das LED


ser= serial.Serial('/dev/ttyACM0', 9600) # tty * bzw das acm0 herlauslesen aus dem Befehl 
											# "ls /dev/tty*"  Arduino zuerst nicht angeschlossen danach angeschlossen anwendenden
											#danach ist ein Modul mehr angegeben und dieses darauf definieren.
										
arduinonr = 10 # die Variable Arduino nr die übergabe einfach mal initiziert ggf überflüssig?

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    
def getwert(): # funktion definiert um den seriellen Wert auszulesen
 while True:
    try:
      arduinonr = 0    # setzen von der Variabel, gg fnicht nötig
      arduinonr = ser.readline()  # Anweisung arduinonr das dies eingelesen wird als eine Zahl
      print(arduinonr)  # Ausgabe in der Comandzeile  eigentlich überflüssig aber gut zm testen
      
      return arduinonr 
    except:  # fals nichts vorhanden einfach weiter springen ggf Fehler ausgeben oder default?
      pass

def main():
  # Main program block

  # Initialise display
  lcd_init()

  while True:
  
    wert=getwert()  # setzen eines Wertes
   
    # Send some test
    lcd_string(wert,LCD_LINE_1)
    #lcd_string("laufts, also ",LCD_LINE_2)
    if (int(wert) < 500):
      GPIO.output(26, True) #LED ansteuern
      lcd_string("Gruen! LED AN ",LCD_LINE_2) # to display
      publish.single("paho/test/cp2swag/value", wert, hostname="broker.mqttdashboard.com") # to broker

    else:
      GPIO.output(26, False) #LED ausstellen 
      lcd_string("Achtung Halt! ",LCD_LINE_2) # to display
      publish.single("paho/test/cp2swag/value", wert, hostname="broker.mqttdashboard.com") # to broker
      

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:    # mit ctrl + C kann das Programm abgebrochen werden
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)

