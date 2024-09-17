""" This file will extract fault injection result with different duration and voltage
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
import pandas as pd
import time
import sys
import subprocess

def fault_injection(Injection_time, duration, vol):

    Spider_com_port.close()
    Pinata_com_port.close()   

    Spider_com_port.open()
    Pinata_com_port.open()

    spiderCore1 = Spider(Spider.CORE1, Spider_com_port); # Instantiate a Spider object using CORE1
    spiderCore1.resetSettings(); # Clear all previous settings in CORE1

    glitcher = Glitcher(spiderCore1, 0)   # Instantiate a Glitcher machine in Spider CORE1
                                        # Trigger Input @ Pin 0
    
    glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3) # Set normal Vcc of glitch out 1 to 3.3 Volts, this value will be effective until next setNomalVcc() call
    glitcher.setGlitchVcc(Spider.GLITCH_OUT1, vol)  # Set glitch Vcc of glitch out 1 to 0.0 Volts, this value will be effective until next setGlitchVcc() call
    glitcher.addGlitch(Spider.GLITCH_OUT1, Injection_time, duration) # Assign the 1st glitch to glitch out 1:
    
    glitcher.arm(edge=Spider.RISING_EDGE, triggerCount=2) # Arm the glitcher to detect trigger 
                                                        # Count 1 rising edge and start glitching

    time.sleep(0.2)
    ## Encryption 
    for i in range(1):
        flag =  list(Pinata_com_port.read(1))
        cmd = [0xCD,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00]
        Pinata_com_port.write(bytes((bytearray(cmd))))
    
        ansx = ''
        ansz = ''

 
        for i in range (1):
            ansx = ''
            ansz = ''
            pr =  list(Pinata_com_port.read(2)) 
            #print (pr)
            if ((len(pr)!=2)):
                return 'fail'
        
            for j in range (0,8):
                inter_Ax = list(Pinata_com_port.read(8))
                if (len(inter_Ax)!=8):
                    return 'fail'
                tmp_x = ''.join([format(ord(char), '02x') for char in inter_Ax])
                ansx += tmp_x  
            for j in range (0,8):
                inter_Az = list(Pinata_com_port.read(8))
                if (len(inter_Az)!=8):
                    return 'fail'
                tmp_z = ''.join([format(ord(char), '02x') for char in inter_Az])
                ansz += tmp_z 
        print (ansx)
        print (ansz)

        #a = 'a7071cf2062c5b284ef6c4e374631ad5075a4dd6d3013833a3c0a67a26b9e94351601a8a437952f24f45902681f6b516c8364e54abb888f40266ebb102f36783'
        #b = 'c8fc8df598726f0a7b1bc81750a6af955d319e67c1e961b4b0aa7275301955f14a080672d9ba6c6497a5ef8a246ee77b06ea9e5d4383676a3496e2e117e0ec80'
        
        ##359##
        #a = '8CA9933C03BB4B8B9841F6C76D368896F483231984D32D0AE2D2CF69C0781E405B148BE3FBA6FE1168B07C88961041D9B9F9139322D1FBE44320A2408B1EC722' 
        #b = 'C11EC3FFDA5111919B4080A2F3E4B6A19C74F834AD568F4AE6AF140C2087670BFBB925261AC7DB5AA0835345E2C2EB0474F2270B289BF1E5569FFA1047399626' 
        
        a = 'F3DC47857B5378F1761D4BBC00F8572A3EF589D09F2D59EEDC3FA1CDB0A873D8C87288EF3050AD3A00D87C261F0AC3252DECE1D20E128B3D60FDA987CF173298'
        b = '90F18C02ABEFA2F7436C243A742947DAE91865F146EA8F5037DBE9CF77F48013E95A38038AFA1E8ACE1DDBD82E0BA8788528B8BC41511BF64262AAF9A45E0711'

        #print ((ansx==a.lower(),ansz==b.lower()))
        return (ansx==a.lower(),ansz==b.lower())
                                                              
    print(glitcher.isGlitcherDone()) # Check if the glitcher is done. User may implement a timeout here.
    ##tmp =  list(Pinata_com_port.read(16))
    ##print(tmp) 

    # Closing Serial Ports
    Spider_com_port.close()
    Pinata_com_port.close()


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
        timeout= 15
    )
    header = ['duration', 'inject_time', 'vol', 'Correct', 'Faulty', 'Fail']
    #duration = [140e-9, 145e-9, 150e-9, 155e-9, 160e-9, 165e-9, 170e-9, 175e-9, 180e-9, 185e-9, 190e-9, 195e-9, 200e-9, 205e-9, 210e-9, 215e-9, 220e-9, 225e-9, 230e-9]
    duration = [175e-9]
    rate= list(range (0,100))
    percentage = [float(x)/float(100) for x in rate]
    #percentage = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    #percentage = [0.04]
    #voltage = [1.8, 1.85, 1.9, 2.0, 2.1, 2.2]
    voltage = [1.85]
    execution_time = float(38344840)/float(168000000)
    write = []
    for per in percentage:
        for vol in voltage:
            for dur in duration:
                data = [0,0,0]
                for i in range (10):
                    print (per,i)
                    output = fault_injection(execution_time*per, dur, vol)
                    if output == 'fail':
                        data[2] += 1
                    elif output[0] == True and output[1]==True:
                        data[0] += 1
                    else:
                        data[1] += 1
                print (data)
                write.append([dur, execution_time*per, vol, data[0], data[1], data[2]])
    final = pd.DataFrame(write, columns=header)
    filename = 'CSIDH_plot_code\\fine_grain\\53.csv'
    final.to_csv(filename, encoding='utf-8', index=False)
                