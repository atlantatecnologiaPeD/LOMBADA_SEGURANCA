#Bibliotecas
import json
import serial
import time # Para usar o time.sleep
from crc_16bits import*
from binascii import hexlify
  
ser_Rasp = serial.Serial('/dev/ttyS0', 9600, timeout=0)
ser_Rasp.reset_input_buffer()

#CRC config
formato_CRC = crc_16("HEX")

while(1):
    try:
        ser_Sensor = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
    except serial.SerialException as e:
        print('sensor desconectado') 
        ser_Sensor.close()
        
    print('hi')
    time.sleep(1) 
    
    try:
        if ser_Sensor.is_open:
            print('porta aberta')
            if ser_Sensor.inWaiting() > 0:
                sensor_data = ser_Sensor.readline().decode("utf-8")
                print(sensor_data) 
    except:
        print('Pass')
        
        
        