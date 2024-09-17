""" This file will get the fault injection result with optimal fault injection parameters
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

def test_ans(glitcher):

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

    ans = ''

    flag =  list(Pinata_com_port.read(1))
    for i in range (0,73):
        pr =  list(Pinata_com_port.read(1))  
        if ((len(pr)!=1) or (pr == 0x00) ):
            glitcher.setNormalVcc(Spider.GLITCH_OUT1, 1.5)
            glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3)
            return 3
            
        #clock = list(Pinata_com_port.read(4))
    
    for i in range (0,8):
        tmp =  list(Pinata_com_port.read(8))
        if (len(tmp)!=8):
            glitcher.setNormalVcc(Spider.GLITCH_OUT1, 1.5)
            glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3)
            return 3
        #print(tmp) 
        tmp_ans = ''.join([format(ord(char), '02x') for char in tmp])
        ans += tmp_ans
    
    b='502E89FEBD8A2C4286832A526CE09242230F2EEA2AC3C5AB1B83507C5CEB21ED39768A9F8A1F19DB119F4242FA0A420FD32668C2C4DEF7C15B96B32F02A93625'
        
    if (ans==b.lower()):
        return 1
    else:
        return 2

def fault_injection(clock_cycle, triggercounter,data):
    Spider_com_port.close()
    Pinata_com_port.close()   

    Spider_com_port.open()
    Pinata_com_port.open()

    glitch_time = clock_cycle/CPU_Frequency
    i = 0
    flag = 0
   
    spiderCore1 = Spider(Spider.CORE1, Spider_com_port); # Instantiate a Spider object using CORE1
    spiderCore1.resetSettings(); # Clear all previous settings in CORE1

    glitcher = Glitcher(spiderCore1, 0)   # Instantiate a Glitcher machine in Spider CORE1
                                        # Trigger Input @ Pin 0
    
    #print (glitch_time)
    print ('\n')
    glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3) # Set normal Vcc of glitch out 1 to 3.3 Volts, this value will be effective until next setNomalVcc() call
    glitcher.setGlitchVcc(Spider.GLITCH_OUT1, 0.0)  # Set glitch Vcc of glitch out 1 to 0.0 Volts, this value will be effective until next setGlitchVcc() call
    glitcher.addGlitch(Spider.GLITCH_OUT1, glitch_time, 80e-9) # Assign the 1st glitch to glitch out 1:
        
    glitcher.arm(edge=Spider.RISING_EDGE, triggerCount=triggercounter) # Arm the glitcher to detect trigger 
                                                            # Count 1 rising edge and start glitching
    
    tmp = test_ans(glitcher)

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
    header = ['Prime','clock_cycle','correct','Faulty','Fail']
    write_data = []
    pr_cycle= pd.read_csv("CSIDH_clockcycles.csv")
    
    data = [0,0,0]
    
    #fault_injection (pr_cycle['clock'][0]*0.7, 2 ,data)

    percentage = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    for i in range (0,len(prime)):
        for per in percentage:
            clock_cycle = pr_cycle.Real[i]*per
            triggerCounter = i + 2
            print (clock_cycle/CPU_Frequency)
            #print (triggerCounter)
            data = [0,0,0] #correct, faulty, fail
            for i in range (5):
                fault_injection (clock_cycle, triggerCounter,data)
            write_data.append([prime[i],clock_cycle,data[0],data[1],data[2]])
            final = pd.DataFrame(write_data, columns=header)
            final.to_csv('CSIDH_clockcycles.csv', encoding='utf-8', index=False)
    