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

class SampleBytes(Adapter):
    def _decode(self, obj, context, path):
        return int((obj * 12/8) + 0.5)

    def _encode(self, obj, context, path):
        return int(obj * 2/3)

Sample = Struct(
    "length" / Peek(Int16ul),           # in 12bit samples
    "bytes" / SampleBytes(Int16ul),     # in bytes
    Const(b"\x00\x7d\x53\x4d\x50\x00"),
)

Data = Struct(
    "data" / Bytes(lambda this: this._.samples[this._index].bytes),
)

Block = Struct(
    Const(b"\x00\x00\x00\x00"),
    "length2" / Int32ul,
    #Check(this._.length1 == this.length2),

    "elements" / Array(12, Byte),
    "total" / Computed(lambda this: sum(this.elements)),
    "samples" / Array(this.total, Sample),

    "resize" / Computed((4 + 8 + 12 + (8 * this.total)) & 0xFFF8),  # gives 456

    "data" / Padded(lambda this: this.length2 - this.resize,# seems that there may be padding
        Array(this.total, Data),                            # maybe needs to be multiple of 4...
    ),
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

    #"crc32" / Int32ul,              # Python CRC32 ^ 0xffffffff
)

DFU = Struct(
    "header" / Header,
    "length" / Int32ul,
    Const(b"\x01\x00\x00\x00\x00\x00\x04\x08"),

    "length1" / Int32ul,

    "block" / Block,

    "checksum" / Int32ul,           # CRC-32-BZIP2
    "footer" / Footer,
)

def unpack_samples(data):
    phase = 0
    prev = 0
    comb = 0

    # unpack data to into array of 12bit samples
    unpacked = []
    for byte in data:
        phase += 1
        if phase == 1:
            comb = byte
        if phase == 2:
            # AB aa bb AB aa bb AB aa bb
            unpacked.append((comb >> 4 & 0x000F) + (byte << 4))
        elif phase == 3:
            unpacked.append((comb << 8 & 0x0F00) + (byte << 0))
            phase = 0
        prev = byte

    return unpacked

def pack_samples(unpacked):
    packed = bytearray()
    phase = 0
    comb = 0

    # pack 12bit data to bytestring
    for value in unpacked:
        phase += 1
        if phase == 1:
            comb = (value & 0x000F) << 4    # A_ aa
            data = (value & 0x0FF0) >> 4
        if phase == 2:
            comb |= (value & 0x0F00) >> 8   # AB aa bb
            packed.append(comb)
            packed.append(data)
            packed.append(value & 0x00FF)
            phase = 0

    if phase == 1:
        # haven't stored this data yet...
        packed.append(comb)
        packed.append(data)

    return packed

#--------------------------------------------------
def main():
    import sys
    import os
    import wave
    from optparse import OptionParser
    import crcmod

    from hexdump import hexdump
    import binascii
    import zlib

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
    parser.add_option("-p", "--pack",
        help="pack Samples to PACK directory",
        dest="pack")
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

    print("Opening:", args[0])
    infile = open(args[0], "rb")
    if not infile:
        sys.exit("Unable to open FILE for reading")
    else:
        data = infile.read()
    infile.close()

    if data:
        config = DFU.parse(data)

        if options.summary:
            print("Number of samples:", config['block']['total'])

            total = 0
            btotal = 0
            a_count = 1
            b_count = 1
            for sample in config['block']['samples']:
                print("Sample %d-%d: %s (%s bytes, %f sec)" % \
                    (a_count, b_count, sample['length'], sample['bytes'], int(sample['length'])/32000))
                total += int(sample['length'])
                btotal += int(sample['bytes'])
                if b_count == config['block']['elements'][a_count-1]:
                    a_count += 1
                    b_count = 1
                else:
                    b_count += 1
            print("Total length: %d bytes" % btotal)
            print("Total length: %f sec" % (total/32000))

        if options.unpack:
            path = os.path.join(os.getcwd(), options.unpack) 
            if os.path.exists(path): 
                sys.exit("Directory %s already exists" % path) 

            os.mkdir(path)

            a_count = 1
            b_count = 1
            for data in config['block']['data']:
                unpacked = unpack_samples(data.data)

                if options.raw:
                    name = os.path.join(path, "sample-{0:0=2d}-{1:0=1d}.raw".format(a_count, b_count))
                    outfile = open(name, "wb")
                    for value in unpacked:
                        outfile.write(value.to_bytes(2, byteorder='little'))
                    outfile.close()
                else:
                    name = os.path.join(path, "sample-{0:0=2d}-{1:0=1d}.wav".format(a_count, b_count))
                    outfile = wave.open(name, "wb")
                    outfile.setsampwidth(2)
                    outfile.setnchannels(1)
                    outfile.setframerate(32000)

                    for value in unpacked:
                        outfile.writeframesraw(value.to_bytes(2, byteorder='big'))
                    outfile.close()

                if b_count == config['block']['elements'][a_count-1]:
                    a_count += 1
                    b_count = 1
                else:
                    b_count += 1

        if options.pack or options.replace:
            if options.replace:
                path = os.path.join(os.getcwd(), options.replace)
            else:
                path = os.path.join(os.getcwd(), options.pack)
            if not os.path.exists(path):
                sys.exit("Directory %s does not exist" % path)

            count = 1
            a_count = 1
            b_count = 1
            for sample in config['block']['samples']:
                unpacked = []
                infile = None
                if options.raw:
                    name = os.path.join(path, "sample-{0:0=2d}-{1:0=1d}.raw".format(a_count, b_count))
                    if os.path.isfile(name):
                        infile = open(name, "rb")
                        if infile:
                            if options.pack:
                                file_stats = os.stat(name)
                                length = file_stats.st_size/2
                            else:
                                length = sample['length']

                            if length > 0xffff:
                                length = 0xffff

                            for temp in range(length):
                                value = infile.read(2)
                                unpacked.append(int.from_bytes(value, byteorder='little'))
                            infile.close()
                else:
                    name = os.path.join(path, "sample-{0:0=2d}-{1:0=1d}.wav".format(a_count, b_count))
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

                            if options.pack:
                                length = infile.getnframes() 
                            else:
                                length = sample['length']

                            if length > 0xffff:
                                length = 0xffff

                            for temp in range(length):
                                value = infile.readframes(1)
                                unpacked.append(int.from_bytes(value, byteorder='big'))
                            infile.close()

                if len(unpacked):
                    config['block']['data'][count-1].data = bytes(pack_samples(unpacked))

                count += 1
                if options.pack:
                    if not infile:
                        # file not found, advanced to next element
                        count -= 1

                        config['block']['elements'][a_count-1] = b_count - 1
                        config['block']['total'] = count - 1
                        a_count += 1
                        b_count = 1

                        if a_count == 13:
                            # all elements done, truncate data blocks
                            config['block']['samples'] = config['block']['samples'][:count-1]
                            config['block']['data'] = config['block']['data'][:count-1]
                            break
                    else:
                        config['block']['samples'][count-2].length = length
                        config['block']['samples'][count-2].bytes = \
                                len(config['block']['data'][count-2].data)
                        b_count += 1
                elif b_count == config['block']['elements'][a_count-1]:
                    a_count += 1
                    b_count = 1
                else:
                    b_count += 1

        if options.dump:
            print(config)

        if options.outfile:
            # re-calc inner checksum
            data = Block.build(config['block'])
            crc32 = crcmod.Crc(0x104c11db7, rev=False, initCrc=0, xorOut=0xFFFFFFFF)
            crc32.update(data)
            config['checksum'] = crc32.crcValue ^ 0xFFFFFFFF

            # re-calc outer checksum
            data = DFU.build(config)
            crc32 = crcmod.Crc(0x104c11db7, rev=True, initCrc=0, xorOut=0xFFFFFFFF)
            crc32.update(data)

            outfile = open(options.outfile, "wb")
            if outfile:
                outfile.write(data)
                outfile.write((crc32.crcValue ^ 0xFFFFFFFF).to_bytes(4, byteorder='little'))
                outfile.close

if __name__ == "__main__":
    main()

