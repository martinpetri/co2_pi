import time, board, serial, os, busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

lcd_columns = 16
lcd_rows = 2
i2c = board.I2C()  # uses board.SCL and board.SDA
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()
time.sleep(1)

lcd.message = "Initialized"
time.sleep(1)

ipaddress = os.popen("ifconfig wlan0 \
                     | grep 'inet ' \
                     | awk '{print $2}'").read()
ssid = os.popen("iwconfig wlan0 \
                | grep 'ESSID' \
                | awk '{print $4}' \
                | awk -F\\\" '{print $2}'").read()

lcd.clear()
lcd.message = ipaddress + "\n" + ssid

time.sleep(3)

ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1
)


lcd.clear()
while True:

    if lcd.left_button:
        lcd.clear()
        lcd.message = "Left"
        time.sleep(1)
        lcd.clear()

    data =ser.readline()
    try:
        data = data.decode("utf-8").strip()
    except:
        print('Can not decode data')
    if len(data) == 6:
        value = float(data)
        msg = data
        
        lcd.message = "CO2: " + data

