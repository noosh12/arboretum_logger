from datetime import datetime
import serial
import xbee
import settings
import os
import csv


def main():
    
    # main function
    log()

def log():
    SERIAL_PORT = '/dev/ttyUSB0' # Change this depending on where the serial port is, this may be fine though
    BAUD_RATE = 9600
    # Instantiate an instance for the serial port
    ser_port = serial.Serial(SERIAL_PORT, BAUD_RATE)
    # Instantiate an instance of the ZigBee class
    # and pass it an instance of the Serial class
    xbee1 = xbee.ZigBee(ser_port)

        while True:
        data_samples = xbee1.wait_read_frame()
        samples = data_samples['samples'][0]

        node_id = data_samples['source_addr_long']
        time = datetime.now()

        vwc_600 = ((11.9*(((float(samples['adc-0'])*1200)/1024)/10000))-0.401)*100
        vwc_300 = ((11.9*(((float(samples['adc-1'])*1200)/1024)/10000))-0.401)*100
        temp_100 = ((((float(samples['adc-2'])*1.2)/1024)*3)*41.67)-40
        battery = float(samples['adc-3'])

        new_record = time+','+node_id+','+battery
        log_write(new_record)

def log_write(new_record):
    with open('log.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_record)


if __name__ == "__main__":
    # execute only if run as a script
    main()