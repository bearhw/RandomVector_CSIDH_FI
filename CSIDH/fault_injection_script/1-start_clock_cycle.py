""" This file will extract start times for each isogeny operation
    Copyright (C) 2024 Ting Hung Chiu (kennychiu0818@vt.edu)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""
import serial
import time
import sys
import struct
import pandas as pd
# import secrets

def read32bitData(ser): 
    data = 0
    for i in range(4):
        tmp = ser.read()
        data = data + (int.from_bytes(tmp , byteorder=sys.byteorder) << (i * 8))
        time.sleep(0.2)
    return data

def read64bitData(ser): 
    data = 0
    for i in range(8):
        tmp = ser.read()
        data = data + (int.from_bytes(tmp , byteorder=sys.byteorder) << (i * 8))
        time.sleep(0.2)
    return data

def uart_write_byte(ser, val):
    # length = 8
    # tmp = ('%%0%dx' % (length << 1) % val).decode('hex')[-length:]
    tmp = struct.pack(">B", val)
    print(tmp)
    # ser.write
    # ser.write(val.to_bytes(1, byteorder='big'))

if __name__ == '__main__':

    com_port = serial.Serial(
        port='COM6',
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    )
    
    com_port.close()
    cmd = [0x20]
    com_port.open()

    # time.sleep(2)
    for i in range(1):
        cmd = [0xCD,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01]
        com_port.write(bytes((bytearray(cmd))))
        time.sleep(0.2)
        write_data = []
        start_time = time.time()

        for pr in range (0,404):
            pr =  list(com_port.read(2)) 
            tmp_pr = ''.join([format(ord(char), '02x') for char in pr])
            prime = int(tmp_pr,16)
            print(prime)

            ref = list(com_port.read(1))
            end_time = time.time()
            ex_time = round(end_time-start_time,2)
            print (ex_time)
            write_data.append([prime, ex_time])



        for i in range (0,8):
            tmp = list(com_port.read(8))
            print (tmp)
        end_time = time.time()

        print (end_time-start_time)

        header = ['Prime', 'start_time']
        final = pd.DataFrame(write_data, columns=header)
        filename = 'CSIDH_plot_code\\start_time\prime_start_time_2.csv'
        final.to_csv(filename, encoding='utf-8', index=False)

    com_port.close()