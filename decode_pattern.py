#!/usr/bin/python
#
# Script decode/encode '.unodrpt' Pattern files from UNO Drum
# (c) Simon Wood, 26 Dec 2020
#

from construct import *
from hexdump import *

#--------------------------------------------------
# Define UNODRPT file format using Construct (v2.9)
# requires:
# https://github.com/construct/construct

BLOB = Struct(
    "length" / Byte,
    "blob" / Bytes(this.length),
)

UNODRPT = Struct(
    Const(b"UNODrumPattern"),
    Const(b"\x00\x01\x0d"),
    Const(b"\x30\x00\x01"), "line0" / BLOB,
    Const(b"\x31\x00\x01"), "line1" / BLOB,
    Const(b"\x32\x00\x01"), "line2" / BLOB,
    Const(b"\x33\x00\x01"), "line3" / BLOB,
    Const(b"\x34\x00\x01"), "line4" / BLOB,
    Const(b"\x35\x00\x01"), "line5" / BLOB,
    Const(b"\x36\x00\x01"), "line6" / BLOB,
    Const(b"\x37\x00\x01"), "line7" / BLOB,
    Const(b"\x38\x00\x01"), "line8" / BLOB,
    Const(b"\x39\x00\x01"), "line9" / BLOB,
    Const(b"\x31\x30\x00\x01"), "line10" / BLOB,
    Const(b"\x31\x31\x00\x01"), "line11" / BLOB,
    Const(b"\x31\x32\x00\x01"), "line12" / BLOB,
    Const(b"\x00"),
)

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

#--------------------------------------------------
def main():
    from optparse import OptionParser

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dump",
        help="dump configuration to text",
        action="store_true", dest="dump")
    parser.add_option("-l", "--line",
        help="select specific LINE", dest="line")
    parser.add_option("-m", "--midi", dest="midi",
        help="import data from midi dump")

    parser.add_option("-s", "--summary",
        help="summarize LINE in human readable form",
        action="store_true", dest="summary")
    parser.add_option("-t", "--text",
        help="summarize whole config as text art",
        action="store_true", dest="text")

    parser.add_option("-o", "--output", dest="outfile",
        help="write data to OUTFILE")
    parser.add_option("-O", "--outmidi", dest="outmidi",
        help="write LINE of data to OUTFILE in MIDI format")
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.error("FILE not specified")

    print("Parsing '%s'" % args[0])
    infile = open(args[0], "rb")
    if not infile:
        sys.exit("Unable to open FILE for reading")
    else:
        data = infile.read()
    infile.close()

    if data:
        config = UNODRPT.parse(data)

        if options.dump:
            print(config)

        if options.text and data:
            inst = ["", "tom1", "tom2", "rim", "cowbell", "ride", "cymbal", \
                    "kick1", "kick2", "snare", "closed_hh", "open_hh", "clap"]
            graphic = "..,,ooxxOOXX$$##"
            for line in range(1, 13):
                start = 1 + config['line'+str(line)]['blob'].index(0x2e)
                decoded = decode_block(config['line'+str(line)]['blob'][start:])
                if len(decoded) == 0:
                    continue
                length = decoded[0]
                out = [" "] * length

                offset = 0
                pcount = 0
                while offset < len(decoded):
                    if decoded[offset] == 0:
                        offset += 1
                        pcount += 1
                        continue

                    length = int(decoded[0]/7)+1
                    count = 0
                    loc = []
                    for loop in range(length):
                        for bit in range(7):
                            if (decoded[offset+loop+1] >> bit & 1) == 1:
                                count += 1
                                loc.append(loop*7 + bit)

                    if pcount == 0:
                        for loop in range(count):
                            out[loc[loop]] = graphic[decoded[offset + (2*length) + 1 + loop] >> 3]

                    offset += 2*length + count + 1
                    pcount += 1

                print("%2.2d %10.10s :%s" % (line, inst[line], "".join(out)))

        if options.outfile or (options.outmidi and options.line):
            if 0: #options.outmidi:
                outfile = open(options.outmidi, "wb")
            else:
                outfile = open(options.outfile, "wb")

            data = UNODRPT.build(config)
            if outfile:
                outfile.write(data)
                outfile.close

if __name__ == "__main__":
    main()

