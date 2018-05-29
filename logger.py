#!/usr/bin/env python

from datetime import datetime
import serial
import xbee
#import settings
import os
import csv
import re


def main():
    
    # main function
    log()

def log():
    #SERIAL_PORT = '/dev/ttyUSB0'
    SERIAL_PORT = 'COM4'
    BAUD_RATE = 9600
    # Instantiate an instance for the serial port
    ser_port = serial.Serial(SERIAL_PORT, BAUD_RATE)
    # Instantiate an instance of the ZigBee class
    # and pass it an instance of the Serial class
    xbee1 = xbee.ZigBee(ser_port)
    
    print("initialising serial port listening...")

    sample_count = 0
    node1_battery = 0.0
    node2_battery = 0.0
    node1 = "bx00x13xa2x00Abx9cZ"
    node2 = "bx00x13xa2x00Abx9cxbf"

    while True:
        data_samples = xbee1.wait_read_frame()
        samples = data_samples['samples'][0]

        #node_id = str(data_samples['source_addr_long'])
        node_id = str(data_samples['source_addr_long'])
        node_id = re.sub('[^A-Za-z0-9]+', '', node_id)
        time = datetime.now()

        vwc_600 = ((11.9*(((float(samples['adc-0'])*1200)/1023)/10000))-0.401)*100
        vwc_300 = ((11.9*(((float(samples['adc-1'])*1200)/1023)/10000))-0.401)*100
        temp_100 = ((((float(samples['adc-2'])*1.2)/1023)*3)*41.67)-40
        battery = float(samples['adc-3'])
        
        if(sample_count < 2):
            if(node_id == node1):
                node1_battery = battery
                print('n1 first: '+str(battery))
            elif(node_id == node2):
                node2_battery = battery
                print('n2 first: '+str(battery))
            sample_count+=1

        elif(sample_count == 2):
            if(node_id == node1):
                print('n1 second: '+str(battery))
                node1_battery += battery
                node1_battery = node1_battery/2.0
            elif(node_id == node2):
                print('n2 second: '+str(battery))
                node2_battery += battery
                node2_battery = node2_battery/2.0
            sample_count+=1
        else:
            if(node_id == node1):
                print('n1 second: '+str(battery))
                node1_battery += battery
                node1_battery = node1_battery/2.0
                log_write('node1', node1_battery)
                log_write('node2', node2_battery)
            elif(node_id == node2):
                print('n2 second: '+str(battery))
                node2_battery += battery
                node2_battery = node2_battery/2.0
                log_write('node1', node1_battery)
                log_write('node2', node2_battery)
            sample_count = 0







def log_write(node_id, battery):
    try: 
        with open('log.csv', 'a', newline='') as myFile:  
            writer = csv.writer(myFile, dialect='excel')
            writer.writerow([node_id, battery])
            print(node_id+','+str(battery))

    except IOError:
        print("error opening file")


if __name__ == "__main__":
    # execute only if run as a script
    main()
