""" This file will extract fault injection result with different injection time
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
from Spider import *
from Glitcher import *

import time
import sys
import subprocess
import pandas as pd

CPU_Frequency = float(168000000)

prime = [359, 353, 349, 347, 337, 331, 317, 313, 311, 307, 
         293, 283, 281, 277, 271, 269, 263, 257, 251, 241, 
         239, 233, 229, 227, 223, 211, 199, 197, 193, 191, 
         181, 179, 173, 167, 163, 157, 151, 149, 139, 137, 
         131, 127, 113, 109, 107, 103, 101,  97,  89,  83, 
          79,  73,  71,  67,  61,  59,  53,  47,  43,  41, 
          37,  31,  29,  23,  19,  17,  13,  11,   7,   5,
           3, 587, 373, 367]

def test_ans(glitcher, index, Ax, Az):

    time.sleep(0.2)

    cmd = [0xCD,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
                    0x01,0x01,0x01,0x01]
    Pinata_com_port.write(bytes((bytearray(cmd))))
   
    ansx = ''
    ansz = ''

    flag =  list(Pinata_com_port.read(1))
    for i in range (0,index):
        ansx = ''
        ansz = ''
        pr =  list(Pinata_com_port.read(2))  
        if ((len(pr)!=2) or (pr == 0x00) ):
            glitcher.setNormalVcc(Spider.GLITCH_OUT1, 1.5)
            glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3)
            return 3
        
        for j in range (0,8):
            inter_Ax = list(Pinata_com_port.read(8))
            if (len(inter_Ax)!=8):
                glitcher.setNormalVcc(Spider.GLITCH_OUT1, 1.5)
                glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3)
                return 3
            tmp_x = ''.join([format(ord(char), '02x') for char in inter_Ax])
            ansx += tmp_x  
        
        for j in range (0,8):
            inter_Az = list(Pinata_com_port.read(8))
            if (len(inter_Az)!=8):
                glitcher.setNormalVcc(Spider.GLITCH_OUT1, 1.5)
                glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3)
                return 3
            tmp_z = ''.join([format(ord(char), '02x') for char in inter_Az])
            ansz += tmp_z 
    print (ansx)
    print (ansz)
    
        
    glitcher.setNormalVcc(Spider.GLITCH_OUT1, 1.5)
    glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3)
    
        
    if ((ansx == Ax.lower()) and (ansz == Az.lower())):
        return 1
    else:
        return 2
    
    
    

def fault_injection(clock_cycle, triggercounter, data, Ax, Az):
    Spider_com_port.close()
    Pinata_com_port.close()   

    Spider_com_port.open()
    Pinata_com_port.open()

    glitch_time = float(clock_cycle)/CPU_Frequency
   
    spiderCore1 = Spider(Spider.CORE1, Spider_com_port); # Instantiate a Spider object using CORE1
    spiderCore1.resetSettings(); # Clear all previous settings in CORE1

    glitcher = Glitcher(spiderCore1, 0)   # Instantiate a Glitcher machine in Spider CORE1
                                        # Trigger Input @ Pin 0
    
    #print (glitch_time)
    print ('\n')
    glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3) # Set normal Vcc of glitch out 1 to 3.3 Volts, this value will be effective until next setNomalVcc() call
    glitcher.setGlitchVcc(Spider.GLITCH_OUT1, 1.8)  # Set glitch Vcc of glitch out 1 to 0.0 Volts, this value will be effective until next setGlitchVcc() call
    glitcher.addGlitch(Spider.GLITCH_OUT1, glitch_time, 160e-9) # Assign the 1st glitch to glitch out 1:
        
    glitcher.arm(edge=Spider.RISING_EDGE, triggerCount=triggercounter) # Arm the glitcher to detect trigger 
                                                            # Count 1 rising edge and start glitching
    
    tmp = test_ans(glitcher, triggercounter-1, Ax, Az)

    # Closing Serial Ports
    Spider_com_port.close()
    Pinata_com_port.close()
        
    if (tmp == 1):
        print("Correct")
        data[0] = data[0] + 1
    elif(tmp == 2):
        print("Faulty")
        data[1] = data[1] + 1  
    else:
        print("Fail")
        data[2] = data[2] + 1
    



if __name__ == '__main__':

    ## Setting Up Serial Ports
    Spider_com_port = serial.Serial()
    Spider_com_port.port = "COM7"

    Pinata_com_port = serial.Serial(
        port='COM6',
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=15,
    )
    header = ['Prime','precentage','clock_cycle','correct','Faulty','Fail']
   
    clock = pd.read_csv('CSIDH_clockcycles0116.csv')
    output = pd.read_csv('CSIDH_inter.csv')
    percentage = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    for i in range (33,len(clock.Prime)):
        write_data = []
        if (clock.rd[i]=='real'):
            for per in percentage:
                clock_cycle = int(clock.clock[i]*per)
                triggerCounter = i + 2
                data = [0,0,0] #correct, faulty, fail
                for it in range (3):
                    fault_injection (clock_cycle, triggerCounter, data, str(output.Ax[i]), str(output.Az[i]))
                write_data.append([clock.Prime[i], per, clock_cycle, data[0],data[1],data[2]])
        final = pd.DataFrame(write_data, columns=header)
        filename = 'data\CSIDH_'+ str(clock.Prime[i]) + '.csv'
            #filename = 'CSIDH_total.csv'
        final.to_csv(filename, mode= 'a', encoding='utf-8', index=False)
