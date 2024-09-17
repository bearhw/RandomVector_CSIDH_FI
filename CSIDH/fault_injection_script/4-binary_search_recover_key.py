""" This file will recover the real-then-dummy CSIDH private key with binary search
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
#from statistics import mode
import time
import sys
import subprocess
import pandas as pd
def binary_search(index, prime_index, execution_time):
    left = -1
    right = len(index)
    
    while left < right:
        mid = (left + right) // 2
        
        output = fault_inject(2 * index[mid] + prime_index, execution_time)

        # ignore left half
        if output == 'faulty':
            left = mid
        # ignore right half
        else:
            right = mid

        # Check if target is present at mid
        if (right - left == 1) :
            if output =='faulty':
                return index[mid]
            else:
                return index[mid]-1

        
            
    # If the element is not present in the array
    return 0
'''
#right to left
def binary_search(index, prime_index, execution_time):
    low, high = 0, len(index) - 1
 
    while low <= high:
        mid = (low + high) // 2
        
        output = fault_inject(2 * index[mid] + prime_index, execution_time)
        if output == "faulty":
            if (mid + 1 < len(index)):
                next_output = fault_inject(2 * index[mid + 1] + prime_index, execution_time)
            else:
                next_output = "N"
        
        if output == "faulty" and (next_output == "correct" or next_output == "N"):
            return index[mid]  # Index where "correct" changes to "faulty"

        # If the current element is "correct", search in the left half
        elif output == "correct":
            high = mid - 1

        # If the current element is "faulty", search in the right half
        else:
            low = mid + 1

    return 0
'''
#left to right
'''
def binary_search(index, prime_index, execution_time):
    low, high = 0, len(index) - 1
 
    while low <= high:
        mid = (low + high) // 2
        
        output = fault_inject (2*index[mid]+prime_index, execution_time)
        if (2*index[mid]+1+1+2 <= 11):
               next_output = fault_inject (2*index[mid]+prime_index+2, execution_time)
        else:
               next_output = "N"
        if output == "faulty" and (next_output == "correct" or next_output == "N"):
            return index[mid]  # Index where False changes to True

        # If the current element is False, search in the right half
        elif output == "faulty":
            low = mid + 1

        # If the current element is True, search in the left half
        else:
            high = mid - 1

    return -1
'''

def test_ans(glitcher):
        tmp_flag =  list(Pinata_com_port.read(1))
        time.sleep(0.2)
        

        
        cmd = [0xCD,0x04,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x00,0x00,0x00,0x00]
        Pinata_com_port.write(bytes((bytearray(cmd))))

        ans = ''
                
        for j in range (0,2):
                pr =  list(Pinata_com_port.read(2)) 
                #print(pr)

                if ((len(pr)!=2)):
                        return 3 
                
                for l in range (0,8):
                        intx =  list(Pinata_com_port.read(8))
                        #print (intx)
                        if (len(intx)!=8):
                                return 3
                #print ('\n')
                for m in range (0,8):
                        intz =  list(Pinata_com_port.read(8))
                        #print (intz)
                        if (len(intz)!=8):
                                return 3
        
        for i in range (0,72):
            pr =  list(Pinata_com_port.read(2)) 
            #print(pr)
            if ((len(pr)!=2)):
                return 3 
        for j in range (0,8):
                pr =  list(Pinata_com_port.read(2)) 
                #print(pr)
                if ((len(pr)!=2)):
                        return 3 
                for l in range (0,8):
                        intx =  list(Pinata_com_port.read(8))
                        #print (intx)
                        if (len(intx)!=8):
                                return 3
                #print ('\n')
                for m in range (0,8):
                        intz =  list(Pinata_com_port.read(8))
                        #print (intz)
                        if (len(intz)!=8):
                                return 3
        for k in range (0,8):
                tmp =  list(Pinata_com_port.read(8))

                tmp_ans = ''.join([format(ord(char), '02x') for char in tmp])
                ans += tmp_ans
        #print (ans)

        #b='AB89B41217DBEEDFA4668E69F74D391F9136DE8AEAA8A6977C7F6987E71E0B3799DDF37B5E15B4DA45E39EEFEC616CDFF8D61A32EBC9FEE3361F7301CC818493'
        b = 'DF039A29B710A2BD6E02F71161783A6F5C4E513CD52EB226AC203BF5E1B24A57425193629272502E0831B4F3E14C8E31C40EB0E2D437711560CA52FEE0916940'

        if (ans==b.lower()):
                return 1
        else:
                return 2

def fault_inject(index, execution_time):
        print('index:',index)
        
        Spider_com_port.close()
        Pinata_com_port.close()   

        Spider_com_port.open()
        Pinata_com_port.open()
        i = 0
        flag = 0
        ans = []
        while  (i<6):
                

                spiderCore1 = Spider(Spider.CORE1, Spider_com_port); # Instantiate a Spider object using CORE1
                spiderCore1.resetSettings(); # Clear all previous settings in CORE1

                glitcher = Glitcher(spiderCore1, 0)   # Instantiate a Glitcher machine in Spider CORE1
                                                        # Trigger Input @ Pin 0
                glitcher.setNormalVcc(Spider.GLITCH_OUT1, 3.3) # Set normal Vcc of glitch out 1 to 3.3 Volts, this value will be effective until next setNomalVcc() call
                glitcher.setGlitchVcc(Spider.GLITCH_OUT1, 1.85)  # Set glitch Vcc of glitch out 1 to 0.0 Volts, this value will be effective until next setGlitchVcc() call
                
                glitcher.addGlitch(Spider.GLITCH_OUT1, execution_time, 175e-9) # Assign the 1st glitch to glitch out 1:
                glitcher.arm(edge=Spider.RISING_EDGE, triggerCount=index) # Arm the glitcher to detect trigger 
                
                tmp = test_ans(glitcher)
                
                
                
                if (tmp==3):
                        print("fail")
                else:
                        i = i + 1
                        if (tmp==2):
                                print ("faulty")
                                return "faulty" 
                        else:
                                print ("correct")
        # Closing Serial Ports
        Spider_com_port.close()
        Pinata_com_port.close()  

                
        return "correct"
            
          
        

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

        cp= [4, 4]

        max= [5, 5]
        
        header = ['key','output','time']
        write = []
       
        for i in range (10):
                private_key = []
                prime_count = 0

                start_time = time.time()
                for prime_index in range (0,2):
                        print (i,prime_index)
                        index = list(range(1, max[prime_index]+1))
                        #print (index)
                        if (prime_index == 0):
                               execution_time = (float(274524427)/float(168000000))*0.41
                        if (prime_index == 1):
                               execution_time = (float(269930307)/float(168000000))*0.6
                        private_key.append(binary_search(index, prime_index, execution_time))
                        
                print(private_key)
                end_time = time.time()

                e_time = end_time - start_time

                #print("Execution time:", execution_time, "seconds")
                output = (private_key==cp)
                write.append([private_key, output, e_time])
        final = pd.DataFrame(write, columns=header)
        filename = 'CSIDH_plot_code\\binary_search\\result7_k=6.csv'
        final.to_csv(filename, encoding='utf-8', index=False)
       