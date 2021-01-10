#!/usr/bin/python
#
# Script decode 'sound packs' for UNO Drum
# (c) Simon Wood, 7 Jan 2021
#
# Sample file can be converted:
# sox -B -c 1 -b 16 -e signed -r 32000 sample_01.raw sample_01.wav

import os, sys
from construct import *

#--------------------------------------------------
# Define DFU file format using Construct (v2.9)
# requires:
# https://github.com/construct/construct

Sample = Struct(
    "length" / Int24ul,                     # in 12bit samples
    Const(b"\x7d\x53\x4d\x50\x00"),
)

Block = Struct(
    "counts" / Array(12, Byte),
    "total" / Computed(sum([51,2,1])),      # Works
    #"total" / Computed(sum(this.counts)),  # Hangs indefinately
    "samples" / Array(this.total, Sample),
)

Header = Padded(0x12d, Struct(
    Const(b"\x44\x66\x75\x53\x65"),
    "param1" / Int32ul,
    Padding(2),
    Const(b"\x54\x61\x72\x67\x65\x74"),
    Padding(5),
    Const(b"\x50\x43\x4d\x20\x4c\x69\x62\x72\x61\x72"),
    Padding(2),
    "name" / PaddedString(100, "ascii"),
))

DFU = Struct(
    "header" / Header,
    "block" / Embedded(Block),
)

def unpack_samples(data, length):
    '''
    LE 12bit
    0000BBBB AAAAAAAA
    0000CCCC CCCCBBBB
    0000EEEE DDDDDDDD
    0000FFFF FFFFEEEE
    '''
    phase = 0
    value = 0
    consumed = 0

    # unpack data to into array of 12bit samples
    unpacked = []
    for byte in data:
        value = (value >> 8) + (byte << 8)
        phase += 1
        consumed += 1

        if phase == 2:
            unpacked.append((value & 0x0FFF))
        elif phase == 3:
            unpacked.append((value >> 4 & 0x0FFF))
            phase = 0

        if len(unpacked) >= length:
            return unpacked, consumed

    return unpacked, consumed

#--------------------------------------------------
def main():
    from optparse import OptionParser

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dump",
        help="dump configuration to text",
        action="store_true", dest="dump")
    parser.add_option("-s", "--summary",
        help="summarize DFU as human readable text",
        action="store_true", dest="summary")

    parser.add_option("-u", "--unpack",
        help="unpack Samples/SysEx to UNPACK directory",
        dest="unpack")

    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.error("FILE not specified")

    infile = open(args[0], "rb")
    if not infile:
        sys.exit("Unable to open FILE for reading")
    else:
        data = infile.read()
    infile.close()

    if data:
        config = DFU.parse(data)
        if options.dump:
            print(config)

        if options.summary:
            print("total samples:", sum(config["counts"]))

            total = 0
            count = 1
            for sample in config["samples"]:
                print(count, hex(sample["length"]))
                total += sample["length"]
                count += 1
            print("Total length", hex(total), total)

        if options.unpack:
            # very crude slicing of samples (12bit, 32KHz)
            path = os.path.join(os.getcwd(), options.unpack) 
            if os.path.exists(path): 
                sys.exit("Directory %s already exists" % path) 

            os.mkdir(path)

            count = 1
            data = data[0x2e8:]
            for sample in config["samples"]:
                name = os.path.join(path, "sample_{0:0=2d}.raw".format(count)) 

                outfile = open(name, "wb")
                unpacked, consumed = unpack_samples(data, sample['length'])

                for value in unpacked:
                    outfile.write(value.to_bytes(2, byteorder='little'))
                outfile.close()

                data = data[consumed:]
                count += 1


if __name__ == "__main__":
    main()

