# Script to correct the checksum of the DFU files

import binascii
from optparse import OptionParser

usage = "usage: %prog [options] FILENAME"
parser = OptionParser(usage)

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.error("DFU FILE not specified")

infile = open(args[0], "rb")
if not infile:
    sys.exit("Unable to open FILE for reading")
else:
    data = infile.read()
infile.close()

# Calculate desired checksum
print("Last Bytes:",  binascii.hexlify(data[-4:]))
crc32 = binascii.crc32(data[:-4]) ^ 0xffffffff
print("Calculated:", hex(crc32))

outfile = open(args[0], "wb")
if not outfile:
    sys.exit("Unable to open FILE for writing")

outfile.write(data[:-4])
outfile.write(crc32.to_bytes(4, "little"))
outfile.close()
print("Checksum written")
