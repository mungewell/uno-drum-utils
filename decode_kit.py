#!/usr/bin/python
#
# Script decode/encode '.unodrp' Kit files from UNO Drum
# (c) Simon Wood, 26 Dec 2020
#

from construct import *
import enum

#--------------------------------------------------
# Define UNODRP file format using Construct (v2.9)
# requires:
# https://github.com/construct/construct

class PCM(enum.IntEnum):
        PCM_1 = 1,
        PCM_2 = 2,
        PCM_3 = 3,
        PCM_4 = 4,
        PCM_5 = 5,

class ANALOG(enum.IntEnum):
        ANALOG = 0,
        PCM_2 = 1,
        PCM_3 = 2,
        PCM_4 = 3,
        PCM_5 = 4,

DRUM = Struct(
    "sample" / Enum(Computed(lambda this: \
            this._._.samples[this._.parsingindex]) , PCM),
    "level" / Byte,
    "tune" / Byte,
    "decay" / Byte,
    Const(b"\x00"),
)

KICK1 = Struct(
    "sample" / Enum(Computed(lambda this: \
            this._._.samples[this._.parsingindex]) , ANALOG),
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
    "sample" / Enum(Computed(lambda this: \
            this._._.samples[this._.parsingindex]) , ANALOG),
    "level" / Byte,
    "tune" / Byte,
    "snap" / Byte,
    "decay" / Byte,
    Const(b"\x00"),
)

SNARE = Struct(
    "sample" / Enum(Computed(lambda this: \
            this._._.samples[this._.parsingindex]) , ANALOG),
    "level" / Byte,
    "tune" / Byte,
    "snap" / Byte,
    "decay" / Byte,
    "noise_lpf" / Byte,
    Const(b"\x00"),
)

HHAT = Struct(
    "sample" / Enum(Computed(lambda this: \
            this._._.samples[this._.parsingindex]) , ANALOG),
    "level" / Byte,
    "tune" / IfThenElse(this.sample == "ANALOG",
            Enum(Byte,      # analog sample
                _1 = 0,
                _2 = 32,
                _3 = 64,
                _4 = 96,
            ),
            Byte,           # PCM sample
         ),
    "decay" / Byte,
    Const(b"\x00"),
)

CLAP = Struct(
    "sample" / Enum(Computed(lambda this: \
            this._._.samples[this._.parsingindex]) , ANALOG),
    "level" / Byte,
    "tune" / Byte,
    "decay" / Byte,
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
)

FX = Struct(
    "comp" / Byte,
    "drive" / Byte,
)

UNODRP = Struct(
    "samples" / Array(12, Byte),
    Const(b"\x00\x00"),
    "drums" / DRUMS,
    "fx" / FX,
    Const(b"\x00\x00\x64\x5f"),
)

MIDI = Struct(
    Const(b"\xf0\x00\x21\x1a\x02\x02\x00\x37\x00\x00"),
    "samples" / Array(12, Byte),
    Const(b"\x00\x00"),
    "drums" / DRUMS,
    "fx" / FX,
    Const(b"\x00\x00\x64\x5f"),
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

