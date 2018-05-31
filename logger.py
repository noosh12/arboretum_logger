#!/usr/bin/env python

from datetime import datetime
import threading
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
    SERIAL_PORT = 'COM3'
    BAUD_RATE = 9600
    # Instantiate an instance for the serial port
    ser_port = serial.Serial(SERIAL_PORT, BAUD_RATE)
    # Instantiate an instance of the ZigBee class
    # and pass it an instance of the Serial class
    xbee1 = xbee.ZigBee(ser_port)
    
    print("initialising serial port listening...")

    node1 = "bx00x13xa2x00Abx9cZ"
    node2 = "bx00x13xa2x00Abx9cxb8"

    timer = threading.Timer(15.0, timer_test)
    

    while True:
        data_samples = xbee1.wait_read_frame()
        samples = data_samples['samples'][0]

        #node_id = str(data_samples['source_addr_long'])
        node_id = str(data_samples['source_addr_long'])
        node_id = re.sub('[^A-Za-z0-9]+', '', node_id)
        time = str(datetime.now())
        time = time[11:-10]

        vwc_600 = ((11.9*(((float(samples['adc-0'])*1200)/1023)/10000))-0.401)*100
        vwc_300 = ((11.9*(((float(samples['adc-1'])*1200)/1023)/10000))-0.401)*100
        temp_100 = ((((float(samples['adc-2'])*1.2)/1023)*3)*41.67)-40
        battery = float(samples['adc-3'])


        if(not timer.is_alive()):
            node1_battery = 0.0
            node2_battery = 0.0
            charge = [0.0, 0.0]
            
            timer = threading.Timer(15.0, timer_test, args=[charge])
            timer.start()
            print('timer started')
            print(str(datetime.now()))


        if(node_id == node1):
            charge[0] += battery
        if(node_id == node2):
            charge[1] += battery


def log_write(time, node1_battery, node2_battery):
    try: 
        with open('log.csv', 'a', newline='') as myFile:  
            writer = csv.writer(myFile, dialect='excel')
            writer.writerow([time, node1_battery, node2_battery])
            # print('time: '+time+'     n1: '+str(node1_battery)+'   n2: '+str(node2_battery))

    except IOError:
        print("error opening file")


def timer_test(readings):
    time = str(datetime.now())
    time = time[11:-10]

    try: 
        with open('log.csv', 'a', newline='') as myFile:  
            writer = csv.writer(myFile, dialect='excel')
            writer.writerow([time, readings[0]/4.0, readings[1]/4.0])
            # print('time: '+time+'     n1: '+str(node1_battery)+'   n2: '+str(node2_battery))

    except IOError:
        print("error opening file")
    
    print("timer complete")
    print(str(datetime.now()))
    # return True




if __name__ == "__main__":
    # execute only if run as a script
    main()
