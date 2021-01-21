#!/usr/bin/python
#
# Script decode/encode '.unodrp' Kit files from UNO Drum
# (c) Simon Wood, 26 Dec 2020
#

from construct import *

#--------------------------------------------------
# Define UNODRP file format using Construct (v2.9)
# requires:
# https://github.com/construct/construct

PCM = Struct(
    "type" / Enum(Byte,
        PCM_1 = 0,
        PCM_2 = 1,
        PCM_3 = 2,
        PCM_4 = 3,
        PCM_5 = 4,
        ),
)

ANALOG = Struct(
    "type" / Enum(Byte,
        ANALOG = 0,
        PCM_1 = 1,
        PCM_2 = 2,
        PCM_3 = 3,
        PCM_4 = 4,
        ),
)

DRUM = Struct(
    #"type" / Embedded(PCM),
    "level" / Byte,
    "tune" / Byte,
    "decay" / Byte,
    Const(b"\x00"),
)

KICK1 = Struct(
    #"type" / Embedded(ANALOG),
    "level" / Byte,
    "tune" / Byte,
    "snap" / Byte,
    "decay" / Byte,
    "fm_tune" / Byte,
    "fm_amt" / Byte,
    "sweep" / Byte,
    Const(b"\x00"),
)

KICK2 = Struct(
    #"type" / Embedded(ANALOG),
    "level" / Byte,
    "tune" / Byte,
    "snap" / Byte,
    "decay" / Byte,
    Const(b"\x00"),
)

SNARE = Struct(
    #"type" / Embedded(ANALOG),
    "level" / Byte,
    "tune" / Byte,
    "snap" / Byte,
    "decay" / Byte,
    "noise_lpf" / Byte,
    Const(b"\x00"),
)

HHAT = Struct(
    #"type" / Embedded(ANALOG),
    "level" / Byte,
    "tune" / Enum(Byte,     # 1..4 only
        _1 = 0,
        _2 = 1,
        _3 = 2,
        _4 = 3,
        ),
    "decay" / Byte,
    Const(b"\x00"),
)

CLAP = Struct(
    #"type" / Embedded(ANALOG),
    "level" / Byte,
    "tune" / Byte,
    "decay" / Byte,
)

FX = Struct(
    "comp" / Byte,
    "drive" / Byte,
)

DRUMS = Struct(
    "tom1" / DRUM,
    "tom2" / DRUM,
    "rim" / DRUM,
    "cowbell" / DRUM,
    "ride" / DRUM,
    "cymbal" / DRUM,
    "kick1" / KICK1,
    "kick2" / KICK2,
    "snare" / SNARE,
    "closed_hh" / HHAT,
    "open_hh" / HHAT,
    "clap" / CLAP,
    "fx" / FX,
)

UNODRP = Struct(
    "elements" / Array(13, Byte),   # including "fx"
    Const(b"\x00"),
    "drums" / DRUMS,
    Const(b"\x00\x00\x64\x5f"),
)

MIDI = Struct(
    Const(b"\xf0\x00\x21\x1a\x02\x02\x00\x37\x00\x00"),
    "unodrp" / Embedded(UNODRP),
    Const(b"\xf7"),
)

#--------------------------------------------------
def main():
    from optparse import OptionParser

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dump",
        help="dump configuration to text",
        action="store_true", dest="dump")
    parser.add_option("-m", "--midi",
        help="decode kit from midi dump (ie not '.unodrp' file)",
        action="store_true", dest="midi")

    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.error("FILE not specified")

    infile = open(args[0], "rb")
    if not infile:
        sys.exit("Unable to open FILE for reading")
    else:
        data = infile.read()
    infile.close()

    if options.dump and data:
        if options.midi:
            config = MIDI.parse(data)
        else:
            config = UNODRP.parse(data)
        print(config)


if __name__ == "__main__":
    main()

