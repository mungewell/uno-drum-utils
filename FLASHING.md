# Official vs Un-official Flashing

Once you have built/modified a sound pack, you likely want to flash this to the device.

You can use the official `UNO Drum Sound Content Installer.exe` tool to do this, simply
copy/name your '.dfu' file to `Uno_Drum_lib.dfu` in the same directory as the tool.

Run the tool and follow the onscreen directions.

Using the official tool is preferable, it possible. However, if you are using Linux,
or have not registered you device (maybe because its 2nd hand...), life isn't that easy.

# Fixing the VID/PID

The USB VID/PID embedded in the '.dfu' files from IK does not match the device (when in
Bootloader mode). The official app does not seem to care, the tools in the next section do.

The `decode_sound_packs.py` script has a `-f` command option, which will automatically
fix/adjust the VID/PID before it saves it's output.
```
$ python3 decode_sound_packs.py -f -o my_pack.dfu
Warning: no input file specified, auto-generating
```

# Entering Bootloader Mode

In order the enter bootload mode you need to send a special SysEx packet
```
$ amidi -p hw:1,0,0 -s UNO_Drum_Update_Mode.syx
```

The display on UNO Drum will now show "UPD"

# Flashing with 'dfu-util'

It should be stated (again) that these actions are reversed engineered, they work for
me but there may be something that I do not know/understand correctly.

*But I take no responsibility for any damage to your device.*

Ubunutu (and other distros) include the 'dfu-util' package, first install it with
```
$ sudo apt-get install dfu-util
```

*Note: All `dfu-util` commands need to be run as root.*

Then use the '-l' option to scan your machine for UNO Drum.
```
$ sudo dfu-util -l
dfu-util 0.9

Copyright 2005-2009 Weston Schmidt, Harald Welte and OpenMoko Inc.
Copyright 2010-2016 Tormod Volden and Stefan Schmidt
This program is Free Software and has ABSOLUTELY NO WARRANTY
Please report bugs to http://sourceforge.net/p/dfu-util/tickets/

Found DFU: [1963:0049] ver=0100, devnum=9, cfg=1, intf=0, path="3-1.1", alt=2, name="@External Flash   /0x00000000/01*2048Kg", serial="000000000001"
Found DFU: [1963:0049] ver=0100, devnum=9, cfg=1, intf=0, path="3-1.1", alt=1, name="@PCM Library  /0x08040000/06*128Kg", serial="000000000001"
Found DFU: [1963:0049] ver=0100, devnum=9, cfg=1, intf=0, path="3-1.1", alt=0, name="@Internal Flash    /0x08008000/02*016Kg,01*064Kg,01*128Kg", serial="000000000001"
```

Look for the line with "PCM Library" and note the 'alt' value (`alt=1`).

To install/flash the soundpack use following command, with the VID/PID, `-a 1` and 
the name of the '.dfu' file.
```
$ sudo dfu-util -d 1963:0049 -a 1 -D empty.dfu
dfu-util 0.9

Copyright 2005-2009 Weston Schmidt, Harald Welte and OpenMoko Inc.
Copyright 2010-2016 Tormod Volden and Stefan Schmidt
This program is Free Software and has ABSOLUTELY NO WARRANTY
Please report bugs to http://sourceforge.net/p/dfu-util/tickets/

Opening DFU capable USB device...
ID 1963:0049
Run-time device DFU version 011a
Claiming USB DFU Interface...
Setting Alternate Setting #1 ...
Determining device status: state = dfuIDLE, status = 0
dfuIDLE, continuing
DFU mode device DFU version 011a
Device returned transfer size 1024
DfuSe interface name: "PCM Library  "
file contains 1 DFU images
parsing DFU image 1
image for alternate setting 1, (1 elements, total size = 782956)
parsing element 1, address = 0x08040000, size = 782948
Download        [=========================] 100%       782948 bytes
Download done.
done parsing DfuSe file
```

You will see the UNO Drum's display flicker between the characters "U", "P" and "D", as
the flashing progesses. Once the download is complete the display will show "UPD".

You should now reset the UNO Drum, and enjoy your new sounds.


