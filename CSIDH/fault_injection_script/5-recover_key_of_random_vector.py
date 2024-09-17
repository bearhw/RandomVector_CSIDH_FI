""" This file will recover the dynamic random vector CSIDH private key 
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


def test_ans(glitcher,index):
        tmp_flag =  list(Pinata_com_port.read(1))
        time.sleep(0.2)
        
        cmd = [0xC1,0x05,0x05,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00]
        Pinata_com_port.write(bytes((bytearray(cmd))))

        ans = ''
                
        for j in range (0,index):
                ansx = ''
                ansz = ''
                pr =  list(Pinata_com_port.read(2)) 
                print(pr)

                if ((len(pr)!=2)):
                        return 'fail'
                if (j==0):
                    mask1 =  list(Pinata_com_port.read(1))
                    if (len(mask1)!=1):
                            return 'fail'
                    tmp_mask1 = ''.join([format(ord(char), '02x') for char in mask1])
                    print (tmp_mask1)
                else:
                    mask2 =  list(Pinata_com_port.read(1))
                    if (len(mask2)!=1):
                            return 'fail'
                    tmp_mask2 = ''.join([format(ord(char), '02x') for char in mask2])
                    print (tmp_mask2)
                for l in range (0,8):
                        intx =  list(Pinata_com_port.read(8))
                        #print (intx)
                        if (len(intx)!=8):
                                return 'fail'
                        tmp_ansx = ''.join([format(ord(char), '02x') for char in intx])
                        ansx += tmp_ansx

                #print ('\n')
                for m in range (0,8):
                        intz =  list(Pinata_com_port.read(8))
                        #print (intz)
                        if (len(intz)!=8):
                                return 'fail'
                        tmp_ansz = ''.join([format(ord(char), '02x') for char in intz])
                        ansz += tmp_ansz
                #print (ansx)
                #print (ansz)

        #b = '7bf5086d1b76bf400b4aa864c806c078067f2ab3b7861aaaa8dc501f1f8add02cf8222f524d992a46482121445195567dc4e66524912f9a7538f73140c5e4ae9' #key = [3,3]
        #b = 'E1AF33077149D0EBA6A2444651A008978974BAF1F8806DDAD1A021E74712DC04EDDC5B841D47BD19B19F1DCA88F12C6AC9DD2840681FC01D00FC6F3BDD38B284' #key = [2,2]
        #b = 'AB89B41217DBEEDFA4668E69F74D391F9136DE8AEAA8A6977C7F6987E71E0B3799DDF37B5E15B4DA45E39EEFEC616CDFF8D61A32EBC9FEE3361F7301CC818493' #key = [1,1]
        
        if (tmp_mask1 =='00'and index==1):
            a = '7cdf7a54c5c870212dfb41f0bdbf6cf3055ec93cb7a3db504cc8b6d6439d381d5cd5c262ecd1ee0d5f796260d537e409dd5149a202e92b4b3a238ff664c1a582'
            b = '900b866498a58e606488913455711e2a4a96273740ba9aef2d2c17e85b29d2a548a402c8ed02cca4551d7656e9013212bc03b43d1742c3af24ff0e7c3f94ab0a'
        elif(tmp_mask1 =='01' and index==1):
            a = 'a7071cf2062c5b284ef6c4e374631ad5075a4dd6d3013833a3c0a67a26b9e94351601a8a437952f24f45902681f6b516c8364e54abb888f40266ebb102f36783'
            b = 'c8fc8df598726f0a7b1bc81750a6af955d319e67c1e961b4b0aa7275301955f14a080672d9ba6c6497a5ef8a246ee77b06ea9e5d4383676a3496e2e117e0ec80'
        elif(tmp_mask1 =='00' and tmp_mask2 =='00' and index==2):
            a = '5906c7ae37824ef9052bc03d2c9c7f454126003e7edd258687eee8b34e5a14702152a8ff097dec6fa8afb41ba8b6df4de5b86b845aa7ed190e31a51da36d4dce'
            b = '76cfa6f18b1b4638a730c0db89f35b217957766ca24378403d9d0fa4000b9d0a5ef4ed7133e33dac23f39a6cd7d789496f4ef2ccf5ede07314406435051392e4'
        elif(tmp_mask1 =='01'and tmp_mask2 =='00' and index==2):
            a = '201b88aae08e03c595cf528ba9a56e84215b3b534c89e7ac71a54e054f1932aed7cb68da8b37ec0ac783568792c42b28f05fb68d493f426331bc552ff5a428b2'
            b = 'e0f7e58ed2a74ea6a424a8f88a77b8e5e26195dccd0b80de86b3862095d47ddb85ba060dea5dd094014ed189b7d42c73ae4d134c8fbf3c711b9d0ef546d99621'
        elif(tmp_mask1 =='00'and tmp_mask2 =='01'and index==2):
            a = '7cdf7a54c5c870212dfb41f0bdbf6cf3055ec93cb7a3db504cc8b6d6439d381d5cd5c262ecd1ee0d5f796260d537e409dd5149a202e92b4b3a238ff664c1a582'
            b = '900b866498a58e606488913455711e2a4a96273740ba9aef2d2c17e85b29d2a548a402c8ed02cca4551d7656e9013212bc03b43d1742c3af24ff0e7c3f94ab0a'
        elif(tmp_mask1 =='01' and tmp_mask2 =='01'and index==2):
            a = 'a7071cf2062c5b284ef6c4e374631ad5075a4dd6d3013833a3c0a67a26b9e94351601a8a437952f24f45902681f6b516c8364e54abb888f40266ebb102f36783'
            b = 'c8fc8df598726f0a7b1bc81750a6af955d319e67c1e961b4b0aa7275301955f14a080672d9ba6c6497a5ef8a246ee77b06ea9e5d4383676a3496e2e117e0ec80'
        #print (index)
        #print (a)
        #print (b)
        #print (ansx)
        #print (ansz)
        return (ansx==a.lower(), ansz==b.lower())


def fault_inject(index, execution_time):
        #print('index:',index)
        
        Spider_com_port.close()
        Pinata_com_port.close()   

        Spider_com_port.open()
        Pinata_com_port.open()
        i = 0
        ans = [0,0,0]
        while  (i<200):
                

                spiderCore1 = Spider(Spider.CORE1, Spider_com_port); # Instantiate a Spider object using CORE1
                spiderCore1.resetSettings(); # Clear all previous settings in CORE1

                glitcher = Glitcher(spiderCore1, 0)   # Instantiate a Glitcher machine in Spider CORE1
                                                        # Trigger Input @ Pin 0
                glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3) # Set normal Vcc of glitch out 1 to 3.3 Volts, this value will be effective until next setNomalVcc() call
                glitcher.setGlitchVcc(Spider.GLITCH_OUT1, 1.85)  # Set glitch Vcc of glitch out 1 to 0.0 Volts, this value will be effective until next setGlitchVcc() call
                
                glitcher.addGlitch(Spider.GLITCH_OUT1, execution_time, 175e-9) # Assign the 1st glitch to glitch out 1:
                glitcher.arm(edge=Spider.RISING_EDGE, triggerCount=index+2) # Arm the glitcher to detect trigger 
                
                tmp = test_ans(glitcher,index+1)
                
                
                
                if (tmp=='fail'):
                    print("fail")
                    ans[2] = ans[2]+1
                else:
                    i = i + 1
                    print (tmp)
                    if (tmp==(True,True)):
                        print ("correct")
                        ans[1] = ans[1]+1
                    else:
                        print ("faulty")
                        ans[0] = ans[0]+1
                print (ans)
        # Closing Serial Ports
        Spider_com_port.close()
        Pinata_com_port.close()  

        return ans

          
        

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


        max= [5, 5]
        
        header = ['key','time']
        write = []
       
        for i in range (1):
                private_key = []
                prime_count = 0

                start_time = time.time()
                for prime_index in range (0,2):
                        print (i,prime_index)
                        if (prime_index == 0):
                               execution_time = (float(274524427)/float(168000000))*0.41
                        if (prime_index == 1):
                               execution_time = (float(269930307)/float(168000000))*0.6
                        private_key.append(fault_inject(prime_index, execution_time))
                        
                print(private_key)
                end_time = time.time()

                e_time = end_time - start_time

                #print("Execution time:", execution_time, "seconds")
                write.append([private_key, e_time])
        final = pd.DataFrame(write, columns=header)
        filename = 'CSIDH_plot_code\\recovery random vector\\key=5.csv'
        final.to_csv(filename, encoding='utf-8', index=False)
       