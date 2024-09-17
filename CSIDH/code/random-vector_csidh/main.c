/*
    This file will generate shared secret of dynamic random vector CSIDH 
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
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/







#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

#include "fp.h"
#include "csidh.h"
#include "mont.h"
#include "uint.h"

int8_t** randomVector(int8_t max[], int8_t weight[], int size) {

	printf ("size = %d\n", size);

	int8_t** vector = (int8_t**)malloc(size * sizeof(int8_t*));
	for (int i = 0; i < size; i++) {
		vector[i] = (int8_t*)malloc(max[i] * sizeof(int8_t));
		}


		// Initialize array elements to 0
		for (int i = 0; i < size; i++)
			for (int j = 0; j < size; j++) {
				vector[i][j] = 0;
			}

			// Seed for randomization
			srand(time(NULL));

			// Set 'weight' number of elements to 1 at random positions
			for (int i = 0; i < size; i++){
				for (int j = 0; j < weight[i]; j++) {
					int randomIndex;
					do {
						randomIndex = rand() % max[i]; // Get a random index
						} while (vector[i][randomIndex] == 1); // Ensure the index hasn't been set to 1 before
						vector[i][randomIndex] = 1; // Set the element to 1
				}
			}
	return vector;
}


int main(void)
{
    public_key shared_alice, shared_bob;
    (void)shared_alice;
    (void)shared_bob;
    
    uint8_t num_batches = 1;
    uint8_t my = 0;
    
    /*
    int8_t max[num_primes] = {2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 
                              3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 
                              4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 
                              5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 
                              7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                              7, 7, 8, 9, 9, 9, 10, 10, 10, 10, 
                              9, 8, 8, 8, 7, 7, 7, 7, 7, 6, 
                              5, 1, 2, 2};
   */
    
    int8_t max[num_primes] = {5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 
                              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                              1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  
                              1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  
                              1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  
                              1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  
                              1, 1, 1, 1};
    unsigned int num_isogenies = 82;

    public_key pub_bob = {{{0xa7071cf2062c5b28, 0x4ef6c4e374631ad5, 0x075a4dd6d3013833, 0xa3c0a67a26b9e943, 0x51601a8a437952f2, 0x4f45902681f6b516, 0xc8364e54abb888f4, 0x0266ebb102f36783}}};

    /*
    private_key priv_alice = {{1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1}};
    */
    
    private_key priv_alice = {{4,4,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0}};
    


   int size = 74; 
   int8_t** result = randomVector(max, priv_alice.e, size);

    for (int i = 0; i < size; i++){
        for (int j = 0; j < max[i]; j++) {
            printf("%d ",result[i][j]);
        }
        printf("\n");
    }

    public_key shared_secret = {{{0xa7071cf2062c5b28, 0x4ef6c4e374631ad5, 0x075a4dd6d3013833, 0xa3c0a67a26b9e943, 0x51601a8a437952f2, 0x4f45902681f6b516, 0xc8364e54abb888f4, 0x0266ebb102f36783}}};
    
    

    csidh(&shared_alice, &pub_bob, &priv_alice, num_batches, max, num_isogenies, my, result);
    
    
    

    for(int i = 0; i < 8; i++) {
        printf("%02llX\n",shared_alice.A.c[i]);
    }

    
}
