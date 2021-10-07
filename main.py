#Bibliotecas
import json
import serial
import time # Para usar o time.sleep
from crc_16bits import*
from binascii import hexlify

#Constantes
CABECALHO = 0xAB
COMANDO = 0x81
ID_FAIXA = 0x10
RODAPE = 0xCD

#Serial
ser_Sensor = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
ser_Sensor.reset_input_buffer()

ser_Rasp = serial.Serial('/dev/ttyS0', 9600, timeout=0)
ser_Rasp.reset_input_buffer()


#CRC config
formato_CRC = crc_16("HEX")

#Funções
def sendVel(vel, crc16_alta, crc16_baixa):
    ser_Rasp.write(serial.to_bytes([CABECALHO,COMANDO,ID_FAIXA,vel,crc16_alta, crc16_baixa,RODAPE]))

while True:
    #ser.write(serial.to_bytes([CABECALHO,0x82,ID_FAIXA,0x01,0x8A,0xF4,RODAPE]))
    time.sleep(0.01)
    if ser_Sensor.inWaiting() > 0:
        sensor_data = ser_Sensor.readline().decode("utf-8")
        try:
            dict_json = json.loads(sensor_data)
            print('Dados recebidos pelo sensor:', dict_json)
            velocidade_sensor = int(dict_json['DetectedObjectVelocity'])
            print('Velocidade do sensor:', velocidade_sensor)
# Escreve protocolo em formato HEX e o dado (velocidade) com duas casas decimais ex:0F ou 0A...
            protocolo = f'{COMANDO:x}{ID_FAIXA:x}{velocidade_sensor:0{2}x}'
            print('Protocolo a ser enviado', protocolo)
            CRC_16_bits = (formato_CRC.crc16_CCITT(str(protocolo))) 
            msb_CRC = (CRC_16_bits[0:1])
            lsb_CRC = (CRC_16_bits[1:4])
            msb_CRC_hex = int.from_bytes(msb_CRC, 'big', signed=False)
            lsb_CRC_hex= int.from_bytes(lsb_CRC, 'big', signed=False) 
            sendVel(velocidade_sensor, msb_CRC_hex, lsb_CRC_hex)
        except json.JSONDecodeError as e:
            print("JSON:", e)
            time.sleep(1)


