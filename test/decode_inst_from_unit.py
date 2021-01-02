'''
Quick test to see if I can parse the pattern data from the unit

$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 37 03 07 f7' -r temp.bin -t .1 ; hexdump -C temp.bin

00000000  f0 00 21 1a 02 02 00 37  03 07 01 00 09 01 02 00  |..!....7........|
00000010  00 7f 7f 00 10 7f 7f 03  00 00 00 77 66 59 4c 3b  |...........wfYL;|
00000020  2b 1e 0e 0d 1d 2f 37 44  55 60 72 09 01 02 00 00  |+..../7DU`r.....|
00000030  7f 7f 00 00 00 00 f7                              |.......|
'''

example =   b"\xf0\x00\x21\x1a\x02\x02\x00\x37\x03\x07\x01\x00\x09\x01\x02\x00"+\
            b"\x00\x7f\x7f\x00\x10\x7f\x7f\x03\x00\x00\x00\x77\x66\x59\x4c\x3b"+\
            b"\x2b\x1e\x0e\x0d\x1d\x2f\x37\x44\x55\x60\x72\x09\x01\x02\x00\x00"+\
            b"\x7f\x7f\x00\x00\x00\x00\xf7"

itype = ['Setting',
            'Tom1', 'Tom2', 'Rim', 'Cowbell', 'Ride', 'Cymbal',
            'Kick1', 'Kick2', 'Snare', 'Closed HH', 'Open HH', 'Clap']

ptype = [ [],    # Inst 0
        ['Vel', 'Level', 'Tune', 'Decay'],
        ['Vel', 'Level', 'Tune', 'Decay'],
        ['Vel', 'Level', 'Tune', 'Decay'],
        ['Vel', 'Level', 'Tune', 'Decay'],
        ['Vel', 'Level', 'Tune', 'Decay'],
        ['Vel', 'Level', 'Tune', 'Decay'],
        ['Velocity','Level','Tune','Decay','Snap','FM Tune','FM Amount','Sweep'],
        ['Vel', 'Level', 'Tune', 'Decay'],
        ['Vel', 'Level', 'Tune', 'Decay', 'Snap', 'Noise LPF'],
        ['Vel', 'Level', 'Tune', 'Decay'],
        ['Vel', 'Level', 'Tune', 'Decay'],
        ['Vel', 'Level', 'Tune', 'Decay'],
        ]

offset = 12

pcount = 0
inst = int(example[offset - 3])
print("Decoding:", itype[inst])

# Loop over parameters until SysEx terminator
while example[offset] != 0xf7:
    print("-")
    print(ptype[inst][pcount])
    pcount +=1

    # check for empty segments
    if example[offset] == 0:
        offset += 1
        continue

    # Calculate the length of the bitfield (in Bytes)
    length = int(example[offset]/7) + 1

    count=0
    loc = []

    # Process Bitfield
    for loop in range(length):
        for bit in range(7):
            if (example[offset+loop+1] >> bit & 1) == 1:
                count += 1
                loc.append(loop*7 + bit)

    # Process Parameter
    for loop in range(count):
        print(loop, "@ step", loc[loop], "=", example[offset + (2*length) + 1 + loop])

    offset += 2*length + count + 1


