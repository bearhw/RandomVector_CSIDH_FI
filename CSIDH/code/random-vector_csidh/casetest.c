#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

#include "fp.h"
#include "csidh.h"
#include "mont.h"
#include "uint.h"



int main(void)
{   
    proj out;

    proj A = {{{0xa7071cf2062c5b28, 0x4ef6c4e374631ad5, 0x075a4dd6d3013833, 0xa3c0a67a26b9e943, 0x51601a8a437952f2, 0x4f45902681f6b516, 0xc8364e54abb888f4, 0x0266ebb102f36783}}, fp_1};

    proj K = {{{0xC353C56AADFE6AB1,0xA97947DC2DBF1781,0xCCB2E644649F8C33,0xA5212B5A4D154C20,0x9D6F69112D8A93D7,0xBE4E34C55169801F,0xF56DACBF06E74702,0x5F436C8FBCCC03BB}},
               {{0x4DF05327BD30FA79,0x34CF8D85FA265C9C,0x281806891C82AD8D,0xD3515DBA6562BA73,0xE365F2BC64EAB5E3,0x3DD8F7D92DD9E540,0x3CA8285B5F20AEEE,0x38B6F552D7960323}}};
    uint_c k ={0x3,0x0,0x0,0x0,0x0,0x0,0x0,0x0};
    
    xMUL (&out,&A,&K,&k);
    
    printf("Kx:\n");
    for(int i = 0; i < 8; i++) {
        printf("%02llX\n",K.x.c[i]);
    }
    printf("\n");

    printf("Kz:\n");
    for(int i = 0; i < 8; i++) {
        printf("%02llX\n",K.z.c[i]);
    }
    printf("\n");

}
