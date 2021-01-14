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
        return int((obj * 12/8) + 0.5)

    def _encode(self, obj, context, path):
        return int(obj * 2/3)

Sample = Struct(
    "length" / Peek(Int24ul),                     # in 12bit samples
    "bytes" / SampleBytes(Int24ul),
    Const(b"\x7d\x53\x4d\x50\x00"),
)

Data = Struct(
    "data" / Bytes(lambda this: this._.samples[this._index].bytes),
)

Block = Struct(
    Const(b"\x04\x08"),
    "length1" / Int32ul,
    Const(b"\x00\x00\x00\x00"),
    "length2" / Int32ul,
    Check(this.length1 == this.length2),

    "elements" / Array(12, Byte),
    "total" / Computed(lambda this: sum(this.elements)),
    "samples" / Array(this.total, Sample),

    "param4" / Int16ul,
    "data" / Array(this.total, Data),
)

Header = Padded(0x115, Struct(
    Const(b"DfuSe"),
    "param1" / Int32ul,
    Const(b"\x00\x01"),
    Const(b"Target"),
    Const(b"\x01\x01\x00\x00\x00"),
    Const(b"PCM Library"),
    Const(b"\x20\x00"),
    #"name" / PaddedString(100, "ascii"),
))

Footer = Struct(
    "BCD" / Const(b"\x03\x00"),
    "PID" / Const(b"\x48\x00"),
    "VID" / Bytes(2),               # Const(b"\x63\x19"),
    "BCD_DFU" / Const(b"\x1A\x01"),
    Const(b"UFD"),
    "LENGTH" / Const(b"\x10"),

    "crc32" / Int32ul,              # Python CRC32 ^ 0xffffffff
)

DFU = Struct(
    "header" / Header,

    "param1" / Int32ul,
    Const(b"\x01\x00\x00\x00\x00\x00"),

    "block" / Embedded(Block),

    #"footer" / Footer,
)

def unpack_samples(data):
    phase = 0
    value = 0

    # unpack data to into array of 12bit samples
    unpacked = []
    for byte in data:
        value = (value >> 8) + (byte << 8)
        phase += 1

        if phase == 2:
            unpacked.append((value & 0x0FFF))
        elif phase == 3:
            unpacked.append((value >> 4 & 0x0FFF))
            phase = 0

    return unpacked

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

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dump",
        help="dump configuration to text",
        action="store_true", dest="dump")
    parser.add_option("-s", "--summary",
        help="summarize DFU as human readable text",
        action="store_true", dest="summary")
    parser.add_option("-o", "--output", dest="outfile",
        help="write data to OUTFILE")

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

    parser.add_option("-t", "--test",
        help="scripted test, dev use only",
        action="store_true", dest="test")

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

        if options.summary:
            print("total samples:", config["total"])

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

            print("delta", int(config["length2"]) - btotal - 456)

        if options.unpack:
            path = os.path.join(os.getcwd(), options.unpack) 
            if os.path.exists(path): 
                sys.exit("Directory %s already exists" % path) 

            os.mkdir(path)

            count = 1
            for data in config["data"]:
                unpacked = unpack_samples(data.data)

                if options.raw:
                    name = os.path.join(path, "sample-{0:0=2d}.raw".format(count))
                    outfile = open(name, "wb")
                    for value in unpacked:
                        outfile.write(value.to_bytes(2, byteorder='little'))
                    outfile.close()
                else:
                    name = os.path.join(path, "sample-{0:0=2d}.wav".format(count))
                    outfile = wave.open(name, "wb")
                    outfile.setsampwidth(2)
                    outfile.setnchannels(1)
                    outfile.setframerate(32000)

                    for value in unpacked:
                        outfile.writeframesraw(value.to_bytes(2, byteorder='big'))
                    outfile.close()

                count += 1

        if options.replace:
            path = os.path.join(os.getcwd(), options.replace)
            if not os.path.exists(path):
                sys.exit("Directory %s does not exist" % path)

            count = 1
            for sample in config["samples"]:
                unpacked = []
                if options.raw:
                    name = os.path.join(path, "sample-{0:0=2d}.raw".format(count))
                    if os.path.isfile(name):
                        infile = open(name, "rb")
                        if infile:
                            for temp in range(sample["length"]):
                                value = infile.read(2)
                                unpacked.append(int.from_bytes(value, byteorder='little'))
                            infile.close()

                else:
                    name = os.path.join(path, "sample-{0:0=2d}.wav".format(count))
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
                                unpacked.append(int.from_bytes(value, byteorder='big'))
                            infile.close()

                if len(unpacked):
                    config['data'][count-1].data = bytes(pack_samples(unpacked))
                count += 1

        if options.dump:
            print(config)

        if options.outfile:
            outfile = open(options.outfile, "wb")

            if outfile:
                outfile.write(DFU.build(config))
                outfile.close

if __name__ == "__main__":
    main()

