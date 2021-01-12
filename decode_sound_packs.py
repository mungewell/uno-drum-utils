#!/usr/bin/python
#
# Script decode 'sound packs' for UNO Drum
# (c) Simon Wood, 7 Jan 2021
#
# Sample '.raw' file can be converted:
# sox -B -c 1 -b 16 -e signed -r 32000 sample_01.raw sample_01.wav

from construct import *

#--------------------------------------------------
# Define DFU file format using Construct (v2.9)
# requires:
# https://github.com/construct/construct

'''
1 => 2byte : AA Ax
2 => 3byte : AA AB BB
3 => 5byte : AA AB BB CC Cx
4 => 6byte : AA AB BB CC CD DD
5 => 8byte : AA AB BB CC CD DD EE Ex
6 => 9byte : AA AB BB CC CD DD EE EF FF
'''

class SampleBytes(Adapter):
    def _decode(self, obj, context, path):
        if obj % 2:
            return int((3 * (obj+1)/2) - 1)
        else:
            return int(3 * obj/2)

    def _encode(self, obj, context, path):
        if obj % 3:
            return int((2 * (obj+1)/3) - 1)
        else:
            return int(2 * obj/3)

Sample = Struct(
    "length" / Peek(Int24ul),                     # in 12bit samples
    "bytes" / SampleBytes(Int24ul),
    Const(b"\x7d\x53\x4d\x50\x00"),
)

Block = Struct(
    "counts" / Array(12, Byte),
    "total" / Computed( \
            this.counts[0] + this.counts[1] + this.counts[2] + this.counts[3] + \
            this.counts[4] + this.counts[5] + this.counts[6] + this.counts[7] + \
            this.counts[8] + this.counts[9] + this.counts[10] + this.counts[11]),
    "samples" / Array(this.total, Sample),
)

Header = Padded(0x12d, Struct(
    Const(b"DfuSe"),
    "param1" / Int32ul,
    Const(b"\x00\x01"),
    Const(b"Target"),
    Const(b"\x01\x01\x00\x00\x00"),
    Const(b"PCM Library"),
    Const(b"\x20\x00"),
    #"name" / PaddedString(100, "ascii"),
))

'''
Factory:
00000000: 00 00 07 0C 7C 6A 03 00  48 00 63 19 1A 01 55 46  ....|j..H.c...UF
00000010: 44 10 37 E4 92 92                                 D.7...

$ python3 decode_sound_packs.py -d -u pack Uno_Drum_lib_Antology1.dfu | tail
00000000: 00 00 00 00 96 36 85 60  03 00 48 00 63 19 1A 01  .....6.`..H.c...
00000010: 55 46 44 10 98 20 E9 87                           UFD.. ..

$ python3 decode_sound_packs.py -d -u pack Uno_Drum_lib_Antology2.dfu | tail
00000000: 00 00 00 00 0E 2C 2E EE  03 00 48 00 63 19 1A 01  .....,....H.c...
00000010: 55 46 44 10 23 19 BC 42                           UFD.#..B
'''

Footer = Struct(
    Const(b"\x03\x00\x48\x00\x63\x19\x1A\x01\x55\x46\x44\x10"),
    "param2" / Int32ul,
)

DFU = Struct(
    "header" / Header,
    "block" / Embedded(Block),
    Padding(2),

    "datalength" / Computed( \
            this.samples[0].bytes + this.samples[1].bytes + \
            this.samples[2].bytes + this.samples[3].bytes + \
            this.samples[4].bytes + this.samples[5].bytes + \
            this.samples[6].bytes + this.samples[7].bytes + \
            this.samples[8].bytes + this.samples[9].bytes + \
            this.samples[10].bytes + this.samples[11].bytes + \
            this.samples[12].bytes + this.samples[13].bytes + \
            this.samples[14].bytes + this.samples[15].bytes + \
            this.samples[16].bytes + this.samples[17].bytes + \
            this.samples[18].bytes + this.samples[19].bytes + \
            this.samples[20].bytes + this.samples[21].bytes + \
            this.samples[22].bytes + this.samples[23].bytes + \
            this.samples[24].bytes + this.samples[25].bytes + \
            this.samples[26].bytes + this.samples[27].bytes + \
            this.samples[28].bytes + this.samples[29].bytes + \
            this.samples[30].bytes + this.samples[31].bytes + \
            this.samples[32].bytes + this.samples[33].bytes + \
            this.samples[34].bytes + this.samples[35].bytes + \
            this.samples[36].bytes + this.samples[37].bytes + \
            this.samples[38].bytes + this.samples[39].bytes + \
            this.samples[40].bytes + this.samples[41].bytes + \
            this.samples[42].bytes + this.samples[43].bytes + \
            this.samples[44].bytes + this.samples[45].bytes + \
            this.samples[46].bytes + this.samples[47].bytes + \
            this.samples[48].bytes + this.samples[49].bytes + \
            this.samples[50].bytes + this.samples[51].bytes + \
            this.samples[52].bytes + this.samples[53].bytes),
    "data" / Bytes(this.datalength),
)

def unpack_samples(data, length):
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

def pack_samples(unpacked):
    # pack 12bit data to bytestring
    packed = bytearray()
    phase = 0
    bnext = 0

    for value in unpacked:
        if phase == 0:
            packed.append(value & 0x00FF)
            bnext = (value >> 8 & 0x000F)
            phase += 1
        else:
            packed.append((value << 4 & 0x00F0) + bnext)
            packed.append(value >> 4 & 0x00FF)
            phase = 0

    if phase == 1:
        packed.append(bnext)

    return packed

#--------------------------------------------------
def main():
    import sys
    import os
    import wave
    from optparse import OptionParser
    from hexdump import hexdump

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dump",
        help="dump configuration to text",
        action="store_true", dest="dump")
    parser.add_option("-s", "--summary",
        help="summarize DFU as human readable text",
        action="store_true", dest="summary")

    parser.add_option("-u", "--unpack",
        help="unpack Samples to UNPACK directory",
        dest="unpack")
    parser.add_option("-r", "--replace",
        help="pack REPLACE directory of samples to DFU " + \
            "(overwrites contents, either padded or clipped to original size)",
        dest="replace")
    parser.add_option("-R", "--raw",
        help="use '.raw' sample files (rather than '.wav')",
        action="store_true", dest="raw")

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
            btotal = 0
            count = 1
            for sample in config["samples"]:
                #print(count, sample["length"], sample["bytes"])
                total += sample["length"]
                btotal += sample["bytes"]
                count += 1
            print("Sample length", total)
            print("Bytes length", btotal)

        if options.unpack:
            path = os.path.join(os.getcwd(), options.unpack) 
            if os.path.exists(path): 
                sys.exit("Directory %s already exists" % path) 

            os.mkdir(path)

            count = 1
            #data = data[0x2e8:]
            data = config['data']
            for sample in config["samples"]:
                unpacked, consumed = unpack_samples(data, sample['length'])

                if options.raw:
                    name = os.path.join(path, "sample_{0:0=2d}.raw".format(count))
                    outfile = open(name, "wb")
                    for value in unpacked:
                        outfile.write(value.to_bytes(2, byteorder='little'))
                    outfile.close()
                else:
                    name = os.path.join(path, "sample_{0:0=2d}.wav".format(count))
                    outfile = wave.open(name, "wb")
                    outfile.setsampwidth(2)
                    outfile.setnchannels(1)
                    outfile.setframerate(32000)

                    for value in unpacked:
                        outfile.writeframesraw(value.to_bytes(2, byteorder='little'))
                    outfile.close()

                data = data[consumed:]
                count += 1

        if options.replace:
            path = os.path.join(os.getcwd(), options.replace)
            if not os.path.exists(path):
                sys.exit("Directory %s does not exist" % path)

            count = 1
            data = config['data']
            for sample in config["samples"]:
                unpacked = []
                if options.raw:
                    name = os.path.join(path, "sample_{0:0=2d}.raw".format(count))
                    if os.path.isfile(name):
                        infile = open(name, "rb")
                        if infile:
                            for temp in range(sample["length"]):
                                value = infile.read(2)
                                unpacked.append(int.from_bytes(value, byteorder='little'))
                            infile.close()
                    else:
                        # clear sample
                        unpacked = [0] * sample['length']

                else:
                    name = os.path.join(path, "sample_{0:0=2d}.wav".format(count))
                    if os.path.isfile(name):
                        infile = wave.open(name, "rb")
                        if infile:
                            # checks
                            if infile.getnchannels() != 1:
                                sys.exit("Samples should be 1 channel: %s" % name)
                            if infile.getsampwidth() != 2:
                                sys.exit("Samples should be 16 bit: %s" % name)
                            if infile.getframerate() != 32000:
                                sys.exit("Samples should be 3200KHz: %s" % name)

                            for temp in range(sample["length"]):
                                value = infile.readframes(1)
                                unpacked.append(int.from_bytes(value, byteorder='little'))
                            infile.close()
                    else:
                        # clear sample
                        unpacked = [0] * sample['length']

                packed = pack_samples(unpacked)
                # TODO: need to merge new data into existing DFU

                count += 1


if __name__ == "__main__":
    main()

