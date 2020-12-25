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

## Device Configuration (Setup)

CMD 0x21: Write setup parameter, need to enter 'setup mode' first with CMD 0x11
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 11 01 7f f7' -r temp.bin -t 1 ; hexdump -C temp.bin

20 bytes read
00000000  f0 00 21 1a 02 02 34 00  01 01 f7 f0 00 21 1a 02  |..!...4......!..|
00000010  02 00 11 f7                                       |....|
00000014
```

And then, for example turning "Prog Change" messages on...
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 21 00 06 01 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

9 bytes read
00000000  f0 00 21 1a 02 02 00 21  f7                       |..!....!.|
00000009
```

CMD 0x22: Read setup parameter.
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 22 00 01 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

9 bytes read
00000000  f0 00 21 1a 02 02 00 22  f7                       |..!....".|
00000009

$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 02 22 00 06 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

12 bytes read
00000000  f0 00 21 1a 02 02 00 22  00 06 01 f7              |..!...."....|
0000000c
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
