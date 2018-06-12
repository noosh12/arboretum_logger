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

        vwc_600 = vwc_conversion(float(samples['adc-0']))
        vwc_300 = vwc_conversion(float(samples['adc-1']))
        temp_100 = temp_conversion(float(samples['adc-2']))
        battery = battery_conversion(float(samples['adc-3']))

        if(not timer.is_alive()):

            readings = [0.0, 0.0, 0.0, 0.0, 0]
            
            timer = threading.Timer(15.0, timer_test, args=[readings])
            timer.start()
            print('timer started')
            print(str(datetime.now()))
            


        if(node_id == node1):
            readings[0] += vwc_600
            readings[1] += vwc_300
            readings[2] += temp_100
            readings[3] += battery
            readings[4] += 1
            print(readings)

        if(node_id == node2):
            # charge[1] += battery
            print("node2 not updating log")


# def log_write(time, node1_battery, node2_battery):
#     try: 
#         with open('log.csv', 'a', newline='') as myFile:  
#             writer = csv.writer(myFile, dialect='excel')
#             writer.writerow([time, node1_battery, node2_battery])
#             # print('time: '+time+'     n1: '+str(node1_battery)+'   n2: '+str(node2_battery))

#     except IOError:
#         print("error opening file")


def timer_test(readings):
    time = str(datetime.now())
    time = time[11:-10]
    print(readings)
    count = readings[4]
    vwc1 = round(readings[0]/count, 4)
    vwc2 = round(readings[1]/count, 4)
    temp = round(readings[2]/count, 1)
    battery = round(readings[3]/count, 3)


    try: 
        with open('log.csv', 'a', newline='') as myFile:  
            writer = csv.writer(myFile, dialect='excel')
            writer.writerow([time, vwc1, vwc2, temp, battery])
            # print('time: '+time+'     n1: '+str(node1_battery)+'   n2: '+str(node2_battery))

    except IOError:
        print("error opening file")
    
    print("timer complete")
    print(str(datetime.now()))
    # return True

def adc_conversion(reading):
    return reading*1250/1023

def vwc_conversion(reading):
    raw = reading*0.61*4095/982
    return (raw*8.5*0.0001)-0.48

def temp_conversion(reading):
    mv = adc_conversion(reading)
    return mv*3*41.67/1000-40

def battery_conversion(reading):
    return (constrain_battery(reading)-730)/100

def constrain_battery(reading):
    return min(830, max(730, reading))




if __name__ == "__main__":
    # execute only if run as a script
    main()
