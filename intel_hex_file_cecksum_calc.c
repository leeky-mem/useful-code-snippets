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
#include <stdlib.h>
#include <string.h>

#define INTEL_HEX_MAX_LINE_LEN 42
#define INTEL_HEX_MIN_LINE_LEN 2

int main (int argc, char *argv[])
{
	uint8_t cc = 0;
	int line_len = strlen(argv[1]);
	int byte_len = line_len / 2;
	char *input;
	char temp[3];
	temp[2] = 0;
	int j = 0;
	uint8_t val[byte_len];

	// Input check
	if (argc == 2) {
		input = argv[1];
		if (line_len > INTEL_HEX_MAX_LINE_LEN){
			printf("Input line cannot be longer than 21 Byte!\n");
			return -1;
		}
		if (line_len < INTEL_HEX_MIN_LINE_LEN){
			printf("Input line cannot be shorter than 2 byte!");
			return -1;
		}
	}
	else if (argc > 2) {
		printf("Too many arguments supplied.\n");
		return -1;
	}
	else {
		printf("One argument expected.\n");
		return -1;
	}

	//Convert input string to array of baytes
	for (int i = 0; i < line_len ; i+=2){
		temp[0] = input[i];
		temp[1] = input[i + 1];
		val[j] = (uint8_t)strtol(temp, NULL, 16);
		//printf("temp = 0x%s\n", temp);
		//printf("val %d = 0x%02x\n",j ,val[j]);
		j += 1;
	}

	// Calculate Checksum
	// byte_len - 1 because the last byte is the old checksum
	for (int i = 0; i < byte_len - 1; i++){
		cc += val[i];
	}
	cc= 0x01 + ~(cc);

	// Show results;
	printf("Calculated cc = 0x%02x\n", cc);
	printf("Provided cc = 0x%02x\n", val[byte_len - 1]);
	return 0;
}
