""" This file will extract fault injection result with the fault occur during degree-359
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
        cmd = [0xCD,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00]
        Pinata_com_port.write(bytes((bytearray(cmd))))
    
        

        
        for j in range (0,1):
                ansx = ''
                ansz = ''
                pr =  list(Pinata_com_port.read(2)) 
                #print(pr)

                if ((len(pr)!=2)):
                        return 'fail'
                
                for l in range (0,8):
                        intx =  list(Pinata_com_port.read(8))
                        #print (intx)
                        if (len(intx)!=8):
                                return 'fail'
                        tmp_x = ''.join([format(ord(char), '02x') for char in intx])
                        ansx += tmp_x

                #print ('\n')
                for m in range (0,8):
                        intz =  list(Pinata_com_port.read(8))
                        #print (intz)
                        if (len(intz)!=8):
                                return 'fail' 
                        tmp_z = ''.join([format(ord(char), '02x') for char in intz])
                        ansz += tmp_z
                          
        '''
        for j in range (0,2):
                ansx = ''
                ansz = ''
                pr =  list(Pinata_com_port.read(2)) 
                print(pr)
                if ((len(pr)!=2)):
                        return 'fail' 
                for l in range (0,8):
                        intx =  list(Pinata_com_port.read(8))
                        #print (intx)
                        if (len(intx)!=8):
                                return 'fail'
                        tmp_x = ''.join([format(ord(char), '02x') for char in intx])
                        ansx += tmp_x
                #print ('\n')
                for m in range (0,8):
                        intz =  list(Pinata_com_port.read(8))
                        #print (intz)
                        if (len(intz)!=8):
                                return 'fail'
                        tmp_z = ''.join([format(ord(char), '02x') for char in intz])
                        ansz += tmp_z 
        '''
        print (ansx)
        print (ansz)

        a = 'a7071cf2062c5b284ef6c4e374631ad5075a4dd6d3013833a3c0a67a26b9e94351601a8a437952f24f45902681f6b516c8364e54abb888f40266ebb102f36783'
        b = 'c8fc8df598726f0a7b1bc81750a6af955d319e67c1e961b4b0aa7275301955f14a080672d9ba6c6497a5ef8a246ee77b06ea9e5d4383676a3496e2e117e0ec80'
        

        ##359##
        #a = '7CDF7A54C5C870212DFB41F0BDBF6CF3055EC93CB7A3DB504CC8B6D6439D381D5CD5C262ECD1EE0D5F796260D537E409DD5149A202E92B4B3A238FF664C1A582' 
        #b = '900B866498A58E606488913455711E2A4A96273740BA9AEF2D2C17E85B29D2A548A402C8ED02CCA4551D7656E9013212BC03B43D1742C3AF24FF0E7C3F94AB0A' 
        
        ##353## 
        #a = '5906C7AE37824EF9052BC03D2C9C7F454126003E7EDD258687EEE8B34E5A14702152A8FF097DEC6FA8AFB41BA8B6DF4DE5B86B845AA7ED190E31A51DA36D4DCE'
        #b = '76CFA6F18B1B4638A730C0DB89F35B217957766CA24378403D9D0FA4000B9D0A5EF4ED7133E33DAC23F39A6CD7D789496F4EF2CCF5EDE07314406435051392E4'
        
        ##53##
        #a = '62a9cf24e84316bf0389007ab606dc5fc167e896a86ba0cb808dc6686bfe5358d1ec8ea25ec324e8b846ad2afd0543a52dcc3dfc66ff047b12ad7001c934317c'
        #b = 'b3a2c4bf49971a05a08f1ceef2924e2a03f54c7b718574813b3a635a2768eb9605f5b2baa252e120018ca1be3372b358cb96b009c284e7c9404bb42017cbc567'
        
        ##47##
        #a = '69572FBAB9493E618817D22D2922FF4AE6866065A73C6A218F393FEEF871E2C8BD2F837304B0FDE1A001D92414B90083859BE3B51723C279417D7B2D0FC60F48'
        #b = 'D6BF3C9C8FDFFE98768C70AE11DF70FBEFE8C6346F0A8FF2DC0CCE2F26C9D82A9629405BFF154E850672E25F0ABF34FAE19CEFDB8C6211B508C857993375A230'
        
        ##43##
        #a = '8C9F6DE15A236686AED704EEE01563764C51C34A7584DC62E54D196180782818AC8BC2D6848C750CB0C4D766BB11A9C30D096CA69E72E224212F82BB12B33355'
        #b = '5D35EB0737B65F0BA7F00DB8DE76722B7E3E3315DE23F6C08E0DD9585E4ED6905D7677C2E2E1138A03ABD02C6CABD41205354727B312E9883983CC3DCFA9E3DE'
        #print ((ansx==a.lower(),ansz==b.lower()))
        return (ansx==a.lower(),ansz==b.lower())
                                                              
    #print(glitcher.isGlitcherDone()) # Check if the glitcher is done. User may implement a timeout here.
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
        timeout = 10
    )
    header = ['duration', 'inject_time', 'vol', 'Correct', 'Faulty','reset']
    duration = [175e-9]
    #rate= list(range (0,100))
    #percentage = [float(x)/float(100) for x in rate]
    percentage = [0.14, 0.41, 0.91] 
    #percentage = [0.31, 0.52, 0.6]
    #percentage = [0.91]
    #voltage = [1.8, 1.85, 1.9, 2.0, 2.1, 2.2]
    voltage = [1.85]
    execution_time = float(274524427)/float(168000000)
    #execution_time = float(269930307)/float(168000000)
    write = []
    
    for per in percentage:
        for vol in voltage:
            for dur in duration:
                data = [0,0,0]
                i = 0
                for i in range (50):
                        print (per,i)
                        output = fault_injection(execution_time*per, dur, vol)
                        if output == 'fail':
                                data[2] += 1
                        elif output[0] == True and output[1]==True:
                                data[0] += 1
                        else:
                                data[1] += 1
                print (data)
                write.append([dur, execution_time*per, vol, data[0], data[1],data[2]])
    final = pd.DataFrame(write, columns=header)
    filename = 'CSIDH_plot_code\\fine_grain\\faulty rate\\359_04120941_d.csv'
    final.to_csv(filename, encoding='utf-8', index=False)
                