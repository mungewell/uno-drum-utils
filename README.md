# uno-drum-utils
Scripts for controlling the IK UNO Drum.

Like it's sister the UNO Drum has an official app, but unlike the synth this splits
the presets into two parts - Kits ('.unodrp' files) and Patterns ('.unodrpt' files).

The device supports 100 Kits and 100 Patterns. There is also a Song mode, where a 
number of patterns can be chained together to form a longer composition.

For programming UNO Synth, see the sister project:
https://github.com/mungewell/uno-synth-utils

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

CMD 0x33: Switch to Pattern xx (ie 99-> 0x63).
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 35 00 63 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

20 bytes read
00000000  f0 00 21 1a 02 02 00 35  f7 f0 00 21 1a 02 02 34  |..!....5...!...4|
00000010  00 63 63 f7                                       |.cc.|
00000014
```

The patch name is not displayed on the device, but is stored and read back by
the official patch editor application.

CMD 0x29+0x01: Read back patch name (for example patch 100 -> 0x64)
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 29 01 64 00 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

44 bytes read
00000000  f0 00 21 1a 02 02 00 29  01 64 01 55 73 65 72 20  |..!....).d.User |
00000010  4b 69 74 00 00 00 00 00  00 00 00 00 00 00 00 00  |Kit.............|
00000020  00 00 00 00 00 00 00 00  00 00 00 f7              |............|
0000002c
```

CMD 0x28+0x01: Write patch name
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 11 01 0a f7'
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 28 01 63 01 55 4e 4f 2d 55 74 69 6c 73 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

12 bytes read
00000000  f0 00 21 1a 02 02 00 28  01 63 01 f7              |..!....(.c..|
0000000c
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
00000000  f0 00 21 1a 02 02 00 22  00 0d 00 f7              | Metronome, Off/On
00000000  f0 00 21 1a 02 02 00 22  00 0e 00 f7              | Pad Velocity, Off/On
00000000  f0 00 21 1a 02 02 00 22  00 0f 0a f7              |
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
