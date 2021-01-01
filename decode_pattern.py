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


#--------------------------------------------------
def main():
    from optparse import OptionParser

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dump",
        help="dump configuration to text",
        action="store_true", dest="dump")
    parser.add_option("-l", "--line",
        help="dump line X as hex", dest="line")
    parser.add_option("-s", "--summary",
        help="summarize config in human readable form",
        action="store_true", dest="summary")
    parser.add_option("-x", "--xor",
        help="XOR the BLOB with 0x2E",
        action="store_true", dest="xor")

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

    if options.dump and data:
        config = UNODRPT.parse(data)
        print(config)

    if options.line and data:
        config = UNODRPT.parse(data)

        if options.xor:
           new = bytearray()
           for byte in config['line'+str(options.line)]['blob']:
               new.append(0x2e ^ int(byte))
           config['line'+str(options.line)]['blob'] = new

        #print("line %s :" % options.line)
        print(hexdump(config['line'+str(options.line)]['blob']))

    if options.summary and data:
        config = UNODRPT.parse(data)
        for line in range(13):
            print(line, hexdump(config['line'+str(line)]['blob']))


if __name__ == "__main__":
    main()

