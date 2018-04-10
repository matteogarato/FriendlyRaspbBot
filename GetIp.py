import os, psutil, datetime
import time
import Adafruit_CharLCD as LCD
import commands
# Raspberry Pi pin setup
lcd_rs = 18
lcd_en = 23
lcd_d4 = 24
lcd_d5 = 16
lcd_d6 = 20
lcd_d7 = 21
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
#rpm=os.environ.get('SCREEN_UPD') the user running python does not read the ev variable
rpm=10
timetosleep=60/rpm
for x in range (0, rpm):
	lcd.clear()
	lcd.message('IP=')
	lcd.message(commands.getoutput('hostname -I'))
	lcd.message('\n')
	temp=commands.getoutput('/opt/vc/bin/vcgencmd measure_temp')
	temp=temp.replace("temp","T")
	temp=temp.replace("C","")
	temp=temp.split('.', 1)[0]
	lcd.message(temp)
	cpusage=psutil.cpu_percent()
	cpu=" C={}".format(cpusage)
	cpu=cpu.split('.', 1)[0]
	lcd.message(cpu)
	ram=" FR={}".format(commands.getoutput("free | grep Mem | awk '{print $4/$2 * 100.0}'"))
	ram=ram.split('.', 1)[0]
	lcd.message(ram)
	time.sleep(timetosleep)  
