# Script to test encoding/decoding UNO Drum '.undrpt' file format

from hexdump import hexdump

def encode_byte(byte):
    # Mutate each byte according to UNO's scheme
    if byte & 0x3f == 0:
        byte = 0x2e
    elif byte & 0x3f == 0x3f:
        byte = 0x2b
    elif byte > 0x74:
        byte = (byte - 0x45)
    elif byte > 0x5a:
        byte = (byte + 0x06)

    return byte

def encode_block(data):
    out = bytearray()

    # pad to allow encoding
    if len(data) % 3:
        data.append(0)

    # encode 3bytes to 4bytes (as per pattern file format)
    while data:
        if len(data) > 1:
            out.append(encode_byte(0x40 +  (data[0] & 0x3f)))
            out.append(encode_byte(0x40 + ((data[0] >> 6) & 0x03) + ((data[1] << 2) & 0x3c)))
        if len(data) > 2:
            out.append(encode_byte(0x40 + ((data[1] >> 4) & 0x0f) + ((data[2] << 4) & 0x30)))
            out.append(encode_byte(0x40 + ((data[2] >> 2) & 0x1f)))
        del data[:3]
    
    return out

def decode_byte(byte):
    # Mutate each byte according to UNO's scheme
    if byte == 0x2e:
        byte = 0x00
    elif byte == 0x2b:
        byte = 0x3f
    elif byte & 0x60 == 0x20:
        byte += 0x05 
    elif byte & 0x60 == 0x60:
        byte -= 0x46

    return byte

def decode_block(data):
    temp = bytearray()
    out = bytearray()

    # pre-process bytes
    for byte in data:
        temp.append(decode_byte(byte))

    # decode 4bytes into 3bytes
    while temp:
        if len(temp) > 1:
            out.append( (temp[0] & 0x3f)       + ((temp[1] & 0x03) << 6))
        if len(temp) > 2:
            out.append(((temp[1] & 0x3c) >> 2) + ((temp[2] & 0x0f) << 4))
        if len(temp) > 3:
            out.append(((temp[2] & 0x30) >> 4) + ((temp[3] & 0x1f) << 2))
        del temp[:4]

    return out

# Run some sample data...

'''
$ amidi -p hw:2,0,0 -S 'f0 00 21 1a 02 02 37 03 07 f7' -r temp.bin -t .1 ; hexdump -C temp.bin
48 bytes read
00000000  f0 00 21 1a 02 02 00 37  03 07 01 00 15 7f 7f 7f  |..!....7........|
                             data starts here >^^
00000010  00 00 00 01 01 01 02 02  02 04 04 04 08 08 08 10  |................|
00000020  10 10 20 20 20 40 40 40  00 00 00 00 00 00 00 f7  |..   @@@........|

$ python3 ~/uno-drum-utils-github/decode_pattern.py -l 7 kick1_vel_bitstep.unodrpt
Parsing 'kick1_vel_bitstep.unodrpt'
00000000: 05 33 35 2E 55 37 32 65  2B 41 2E 2E 2E 44 50 2E  .35.U72e+A...DP.
00000010: 41 48 66 2E 42 50 2E 41  44 66 2E 42 48 2E 41 44  AHf.BP.ADf.BH.AD
00000020: 50 2E 42 48 66 2E 44 50  2E 41 2E 2E 2E 2E 2E 2E  P.BHf.DP.A......
00000030: 2E 2E 2E 00
'''

test =  b"\x05\x33\x35\x2E\x55\x37\x32\x65\x2B\x41\x2E\x2E\x2E\x44\x50\x2E" + \
        b"\x41\x48\x66\x2E\x42\x50\x2E\x41\x44\x66\x2E\x42\x48\x2E\x41\x44" + \
        b"\x50\x2E\x42\x48\x66\x2E\x44\x50\x2E\x41\x2E\x2E\x2E\x2E\x2E\x2E" + \
        b"\x2E\x2E\x2E\x00"

#test =  b"\x05\x38\x2E\x41\x44\x2E\x2E\x2B\x41\x2E\x2E\x2E\x2E\x2E\x00"

# Data starts after the first '0x2e'
decoded = decode_block(list(test[test.index(0x2e) + 1:]))

print("Decoded:")
print(hexdump(decoded))

