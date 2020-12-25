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

CMD 0x12: Read F/W version
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 2 12 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

28 bytes read
00000000  f0 00 21 1a 02 02 00 12  01 30 31 2e 30 32 20 23  |..!......01.02 #|
00000010  23 2e 23 23 20 23 23 2e  23 23 00 f7              |#.## ##.##..|
0000001c
```
