# uno-drum-utils
Scripts for controlling the IK UNO Drum.

Like it's sister the UNO Drum has an official app, but unlike the synth this splits
the presets into two parts - Kits ('.unodrp' files) and Patterns ('.unodrpt' files).

The device supports 100 Kits and 100 Patterns. There is also a Song mode, where a 
number of patterns can be chained together to form a longer composition.

Recently we had a breakthough, and now understand how the 'sound packs' the IK provided
in the 'Anthology' series are encoded. The include '.dfu' files which patch part of
the UNO Drum's firmware. The '.dfu' contains 32KHz mono samples for each sound and tables
of how they are allocated within the device.

I imagine that this will become the prime "reason-d'etra" for this project, it is
totally in the realms of possibilty that it could provide a GUI interface to make it
easy for users to add their own samples. I'll jusy say "coming soon"....

For programming UNO Synth, see the sister project:
https://github.com/mungewell/uno-synth-utils

# Sound-Pack Capabilities

The UNO Drum is advertised with a fixed set of sounds, but shortly after release
IK released their "Drum Anthology" - 8 sound packs with samples from historic
drum machines. Registered users could download these and flash them to the UNO Drum.

Each sound/sample is 12bit, mono, 32KHz, and can be up-to 65535 samples (~2sec) long.

# Custom Sound-Packs

The format of these sound packs has been reversed engineered, and we now have the
ability to extract, or replace the sounds from these packs. We can even create a
sound pack completely from scratch.

```
$ python3 decode_sound_packs.py -o empty.dfu
Warning: no input file specified, auto-generating
```

As the name hints this is a completely empty sound pack, all samples are short
sections of silence. But like others this pack could be extracted (to a directory),
sample files adjusted and then repacked.

```
$ python3 decode_sound_packs.py -u pack_samples
Warning: no input file specified, auto-generating

$ python3 decode_sound_packs.py -o my_new_pack.dfu -p pack_samples
Warning: no input file specified, auto-generating
```

The sound packs can by uploaded to the UNO Drum using the official tools. We are
investigating whether these 'dfu' files can be uploaded with other 'free' apps.

Offically each pad has either 5 PCM samples, or Analog + 4 PCM samples. Leading
to a total of 54 samples for each pack. The largest factory pack contains a
total of 12.58sec, although the exact limit is not known at this time.

A summary of the samples in a pack can be printed

```
$ python3 decode_sound_packs.py -s empty.dfu
Opening: empty.dfu
Number of samples: 54
Sample 1-1: 1 (2 bytes, 0.000031 sec)
Sample 1-2: 1 (2 bytes, 0.000031 sec)
Sample 1-3: 1 (2 bytes, 0.000031 sec)
Sample 1-4: 1 (2 bytes, 0.000031 sec)
Sample 1-5: 1 (2 bytes, 0.000031 sec)
Sample 2-1: 1 (2 bytes, 0.000031 sec)
Sample 2-2: 1 (2 bytes, 0.000031 sec)
...
Sample 11-4: 1 (2 bytes, 0.000031 sec)
Sample 12-1: 1 (2 bytes, 0.000031 sec)
Sample 12-2: 1 (2 bytes, 0.000031 sec)
Sample 12-3: 1 (2 bytes, 0.000031 sec)
Sample 12-4: 1 (2 bytes, 0.000031 sec)
Total length: 108 bytes
Total length: 0.001687 sec
```

Oddly analog samples are labelled 'An' and 2 thru 5 on the device, but 'An' 
and 1 thru 4 on the Editor application.

The Sound-Packs can define more (or fewer) samples for each pad, the display
on the device can't count above 9 - it just shows blanks - but the samples can 
continue to be switched.

If less than regular ammount are set the device can become 'confused' if a drum pack
selects an unused sample, and then turning the data dial will be in-affective. The
desired sample can be selected via Midi.

# Handcrafted SysEx control of the device

Reverse engineering has only just started but it seems that it's at least somewhat
similar the UNO Synth.

CMD 0x14: Read back current Kit/Pattern setting
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 14 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

14 bytes read
00000000  f0 00 21 1a 02 02 00 14  02 00 03 02 63 f7        |..!.........c.|
0000000e
                                         ^^    ^^-- Kit
                                         ++-------- Pattern
```

CMD 0x33: Switch to Drum Kit xx (ie 100-> 0x64).
Note: display does not automatically update
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 33 64 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

29 bytes read
00000000  f0 00 21 1a 02 02 32 63  63 f7 f0 00 21 1a 02 02  |..!...2cc...!...|
00000010  00 33 f7 f0 00 21 1a 02  02 32 64 64 f7           |.3...!...2dd.|
0000001d
```

CMD 0x35: Switch to Pattern xx (ie 99-> 0x63).
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 35 00 63 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

20 bytes read
00000000  f0 00 21 1a 02 02 00 35  f7 f0 00 21 1a 02 02 34  |..!....5...!...4|
00000010  00 63 63 f7                                       |.cc.|
00000014
```

The patch name is not displayed on the device, but is stored and read back by
the official patch editor application.

CMD 0x29+0x01: Read back Kit name

CMD 0x29+0x02: Read back Pattern name
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 29 01 64 00 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

44 bytes read
00000000  f0 00 21 1a 02 02 00 29  01 64 01 55 73 65 72 20  |..!....).d.User |
00000010  4b 69 74 00 00 00 00 00  00 00 00 00 00 00 00 00  |Kit.............|
00000020  00 00 00 00 00 00 00 00  00 00 00 f7              |............|
0000002c
```

CMD 0x28+0x01: Write Kit name

CMD 0x28+0x02: Write Pattern name
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 11 01 0a f7'
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 28 01 63 01 55 4e 4f 2d 55 74 69 6c 73 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

12 bytes read
00000000  f0 00 21 1a 02 02 00 28  01 63 01 f7              |..!....(.c..|
0000000c
```
## Kits

The UNO-Drum can store 100 Kits, these can be editted by the offical
app, which can also save/load kits to the '.unodrp' files.

Kits are basically a sequential list of drums and their parameters.
```
    Tom1 	(Type, Level, Tune, Decay)
    Tom2 	(Type, Level, Tune, Decay)
    Rim 	(Type, Level, Tune, Decay)
    Cowbell 	(Type, Level, Tune, Decay)
    Ride 	(Type, Level, Tune, Decay)
    Cymbal 	(Type, Level, Tune, Decay)
    Kick1 	(Type, Level, Tune, Snap, Decay, FM tune, FM amnt, Sweep)
    Kick2	(Type, Level, Tune, Snap, Decay)
    Snare	(Type, Level, Tune, Snap, Decay, Noise LPF)
    Closed HH 	(Type, Level, Tune, Decay)
    Open HH 	(Type, Level, Tune, Decay)
    Clap 	(Type, Level, Tune, Decay)
```

'.undrp' (and Midi files) can be dumped to text with the 'decode_kit.py'
script. This also allows for transcoding between formats.
```
$ python3 decode_kit.py -h
Usage: decode_kit.py [options] FILENAME

Options:
  -h, --help            show this help message and exit
  -d, --dump            dump configuration to text
  -m, --midi            decode kit from midi dump (ie not '.unodrp' file)
  -o OUTFILE, --output=OUTFILE
                        write data to OUTFILE
  -O OUTMIDI, --outmidi=OUTMIDI
                        write data to OUTFILE in MIDI format
```

CMD 0x37+0x00+0x00: Read current Kit
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 37 00 00 f7' -r temp.bin -t .1 ; hexdump -C temp.bin            

85 bytes read
00000000  f0 00 21 1a 02 02 00 37  00 00 01 01 03 03 01 04  |..!....7........|
00000010  00 01 04 00 00 02 00 00  5b 4c 7f 00 4b 00 7f 00  |........[L..K...|
00000020  7f 40 7f 00 52 00 03 00  63 40 7f 00 5f 40 7f 00  |.@..R...c@.._@..|
00000030  78 43 50 35 12 6f 48 00  5d 2e 3c 7f 00 7f 29 3c  |xCP5.oH.].<...)<|
00000040  0b 7f 00 7f 00 2b 00 7f  00 7c 00 7f 57 30 28 0f  |.....+...|..W0(.|
00000050  00 00 64 5f f7                                    |..d_.|
00000055
```

## Patterns

The UNO-Drum can store 100 Patterns. These can be editted by the official 
app, which can also save/load patterns to '.unodrpt' files. Unfortunately these
files appear to be encoded differently to the data stored on the device.

Patterns are structured as a number of instruments.

```
PCM Sounds:
Inst 1 = tom1 (vel, level, tune, decay)
Inst 2 = tom2 (vel, level, tune, decay)
Inst 3 = rim (vel, level, tune, decay)
Inst 4 = cowbell (vel, level, tune, decay)
Inst 5 = ride (vel, level, tune, decay)
Inst 6 = cymbal (vel, level, tune, decay)

Analog/PCM Sounds:
Inst 7 = kick1 (vel, level, tune, decay, snap, FM tune FM amt, sweep)
Inst 8 = kick2 (vel, level, tune, decay, snap)
Inst 9 = snare (vel, level, tune, decay, snap, Noise LPF)
Inst 10 = closed hh (vel, level, tune, decay)
Inst 11 = open hh (vel, level, tune, decay)
Inst 12 = clap (vel, level, tune, decay)
```

Additionally the 'length'(in steps) and 'swing' are stored as Instrument 0.

The currently selected pattern can be read/set via SysEx commands, instrument by
instrument. The pattern data is structured a bit field holding the affected steps,
followed by parameter values for each.

There are a number of parameters which can be recorded, these differ on the type
instrument (as above) and each parameter type has it's own bitfield for 
marking affected steps.

CMD 0x37+0x03+Inst: Read Instrument in current Pattern, for example '0x07' for Kick1
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 37 03 07 f7' -r temp.bin -t .1 ; hexdump -C temp.bin

29 bytes read
00000000  f0 00 21 1a 02 02 00 37  03 07 01 00 05 11 00 7f  |..!....7........|
00000010  7f 05 11 00 40 40 00 00  00 00 00 00 f7           |....@@.......|
0000001d
```

The encoding is quiet complex, in order to define the length of the bitfield the
packet include the last active step of that bitfield. The number of active ('1')
bits in the bitfield determine how many param values are given.
```
00000000  f0 00 21 1a 02 02 00 37  03 07 01 00 05 11 00 7f  |..!....7........|
                                                        ^^ 1st Param value(s)
                                                     -- padding
                                                  ++ Bitfield
                                               ** Last Step
                                      ^^ Instrument
00000010  7f 05 11 00 40 40 00 00  00 00 00 00 f7           |....@@.......|
                            ~~ ~~  ~~ ~~ ~~ ~~ Unused Param Types
                      ^^ ^^ 2nd Param values
                   -- Padding (same # bytes as bitfield)
                ++ Bitfield (may be multiple bytes)
             ** Last Step
          ^^ Param value(s)
```

CMD 0x36+0x03+0x1x: Write pattern to instrument. For example Kick1 (0x07) uses 0x17, 
followed by 'last step' and 'bitfield' for 1st parameter.
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 36 03 17 ...pattern data... f7'
```

Reading a more complicated pattern (factory #8)
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 37 03 07 f7' -r temp.bin -t .1 ; hexdump -C temp.bin

40 bytes read
00000000  f0 00 21 1a 02 02 00 37  03 07 37 08 0f 53 14 01  |..!....7..7..S..|
00000010  00 00 00 7f 7f 7f 7f 7f  7f 7f 00 0c 40 10 00 00  |............@...|
00000020  7f 62 00 00 00 00 00 f7                           |.b......|
00000028
```

CMD 0x37+0x03+0x00: Reading pattern length and swing.
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 37 03 00 f7' -r temp.bin -t .1 ; hexdump -C temp.bin

15 bytes read
00000000  f0 00 21 1a 02 02 00 37  03 00 00 00 15 32 f7     |..!....7.....2.|
                                                  ^^ swing (50..70)
                                               ^^ length (1..64)
0000000f
```

## Device Configuration (Setup)

CMD 0x21: Write setup parameter, need to enter 'setup mode' first with CMD 0x11
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 11 01 7f f7' -r temp.bin -t 1 ; hexdump -C temp.bin

20 bytes read
00000000  f0 00 21 1a 02 02 34 00  01 01 f7 f0 00 21 1a 02  |..!...4......!..|
00000010  02 00 11 f7                                       |....|
00000014
```

And then, for example turning "RX Prog Change" on
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 21 00 06 01 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

9 bytes read
00000000  f0 00 21 1a 02 02 00 21  f7                       |..!....!.|
00000009
```

CMD 0x22: Read setup parameter
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 22 00 06 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

12 bytes read
00000000  f0 00 21 1a 02 02 00 22  00 06 01 f7              |..!...."....|
0000000c
```

Default values:
```
00000000  f0 00 21 1a 02 02 00 22  00 02 01 f7              | MIDI Soft Thru
00000000  f0 00 21 1a 02 02 00 22  00 03 08 f7              | Tempo (low  byte?)
00000000  f0 00 21 1a 02 02 00 22  00 04 00 f7              |
00000000  f0 00 21 1a 02 02 00 22  00 05 01 f7              | ? - Read by App
00000000  f0 00 21 1a 02 02 00 22  00 06 01 f7              | RX Program Change
00000000  f0 00 21 1a 02 02 00 22  00 07 01 f7              | Midi Soft Thru
00000000  f0 00 21 1a 02 02 00 22  00 08 00 f7              | TX Program Change
00000000  f0 00 21 1a 02 02 00 22  00 09 01 f7              |
00000000  f0 00 21 1a 02 02 00 22  00 0a 01 f7              |
00000000  f0 00 21 1a 02 02 00 22  00 0b 01 f7              | MIDI Interface Mode
00000000  f0 00 21 1a 02 02 00 22  00 0c 00 f7              | MIDI Clock Sync
00000000  f0 00 21 1a 02 02 00 22  00 0d 00 f7              | Metronome, Off/On/Play (CC-76)
00000000  f0 00 21 1a 02 02 00 22  00 0e 00 f7              | Pad Velocity, Off/On
00000000  f0 00 21 1a 02 02 00 22  00 0f 0a f7              | Pad Note Length (CC-77)
00000000  f0 00 21 1a 02 02 00 22  00 10 01 f7              | Stutter Type
00000000  f0 00 21 1a 02 02 00 22  00 11 07 f7              | Stutter Amount
00000000  f0 00 21 1a 02 02 00 22  00 12 32 f7              |
00000000  f0 00 21 1a 02 02 00 22  00 13 02 f7              | Division
00000000  f0 00 21 1a 02 02 00 22  00 14 00 f7              |
00000000  f0 00 21 1a 02 02 00 22  00 15 00 f7              | Song Mode Active?

00000000  f0 00 21 1a 02 02 00 22  00 17 02 f7              | Roll Type
00000000  f0 00 21 1a 02 02 00 22  20 18 01 08 f7           | Tempo (2byte = 14bit value)
00000000  f0 00 21 1a 02 02 00 22  00 19 02 f7              |
                                         ^^
```


## System Commands

CMD 0x11: Set device mode, ie 'setup mode'.
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 11 01 7f f7' -r temp.bin -t 1 ; hexdump -C temp.bin

20 bytes read
00000000  f0 00 21 1a 02 02 34 00  01 01 f7 f0 00 21 1a 02  |..!...4......!..|
00000010  02 00 11 f7                                       |....|
00000014
```

CMD 0x12: Read F/W version
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 2 12 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

28 bytes read
00000000  f0 00 21 1a 02 02 00 12  01 30 31 2e 30 32 20 23  |..!......01.02 #|
00000010  23 2e 23 23 20 23 23 2e  23 23 00 f7              |#.## ##.##..|
0000001c
```
