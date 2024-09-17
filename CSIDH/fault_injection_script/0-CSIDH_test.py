""" This file will get the real-then-dummy vector CSIDH shared secret
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

    
    # ## Encryption 
    # time.sleep(2)
    for i in range(1):
        cmd = [0xCD,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00]
        com_port.write(bytes((bytearray(cmd))))
        time.sleep(0.2)
        # start_time = time.time()
        # total_time = 0
        # total_time_for = 0
        ans = ''

        for j in range (0,2):
                ansx = ''
                ansz = ''
                pr =  list(com_port.read(2)) 
                print(pr)
                # start_time1 = time.time()
                # start_time_for = time.time()
                # ref =  list(com_port.read(1)) 
                # ref1 =  list(com_port.read(1)) 
                # end_time_for = time.time()
                for l in range (0,8):
                        intx =  list(com_port.read(8))
                        #print (intx)
                        tmp_ansx = ''.join([format(ord(char), '02x') for char in intx])
                        ansx += tmp_ansx
                print (ansx)
                for m in range (0,8):
                        intz =  list(com_port.read(8))
                        #print (intz)
                        tmp_ansz = ''.join([format(ord(char), '02x') for char in intz])
                        ansz += tmp_ansx
                print (ansz)
                # end_time = time.time()
                # total_time_for += (end_time_for-start_time_for)
                # total_time += (end_time-start_time1)
        
        for j in range (0,72):
                pr =  list(com_port.read(2)) 
                print(pr)

        for j in range (0,8):
                pr =  list(com_port.read(2)) 
                print(pr)
                
                for l in range (0,8):
                        intx =  list(com_port.read(8))
                        print (intx)
                print ('\n')
                for m in range (0,8):
                        intz =  list(com_port.read(8))
                        print (intz)
                
        for k in range (0,8):
                tmp =  list(com_port.read(8))

                tmp_ans = ''.join([format(ord(char), '02x') for char in tmp])
                ans += tmp_ans
        print (ans)
        # end_time = time.time()
        # print ('CSIDH_time = ',end_time-start_time)
        # print ('isogney_time=', total_time)
        # print ('for_time=', total_time_for)
    com_port.close()