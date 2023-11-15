/*
From doc(https://developer.arm.com/documentation/ka003292/latest/):
:10246200464C5549442050524F46494C4500464C33
|||||||||||                              CC->Checksum
|||||||||DD->Data
|||||||TT->Record Type
|||AAAA->Address
|LL->Record Length
:->Colon

One line cc calc:
:02000004FFFFFC
where:
- 02 is the number of data bytes in the record.
- 0000 is the address field. For the extended linear address record, this field is always 0000.
- 04 is the record type 04 (an extended linear address record).
- FFFF is the upper 16 bits of the address.
- FC is the checksum of the record and is calculated as:
  01h + NOT(02h + 00h + 00h + 04h + FFh + FFh).
*/

#include <stdio.h>
#include <stdint.h>

#define len 20

// one line of an intel hex file without leading colon and cecksum (last byte)
static uint8_t val[len]= {0x10,0x06,0x20,0x00,0x2C,0xD9,0x61,0x19,0x08,0xF1,0xFF,0x33,0x04,0xD2,0x8E,0x45,0x02,0xD9,0xA8,0xF1};
static uint8_t res=0;
static uint8_t cc=0;

int main (void)
{
	for (int i =0; i < len; i++){
		res += val[i];
	}
	res = ~(res) ;
	cc= 0x01 + res;
	printf("cc= 0x%02x", cc);
  	return 0;
}
