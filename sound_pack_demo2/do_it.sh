# Create a demo sound pack using the samples from "Tiago Cunha's Intimate Percussion kit"
# https://www.pianobook.co.uk/packs/tcipk-tiago-cunhas-intimate-percussion-kit/

# create directory of empty samples
rm -r unpacked Uno_Drum_lib_TCIPk.dfu
python3 ../decode_sound_packs.py --unpack unpacked

# debug info
#soxi -V1 `find unpacked -name '*.wav' | sort -n ` > before.txt
#soxi -V1 `find DrumSamples.org-DS1000 -name '*.wav' | sort -n ` > DrumSamples-DS1000.txt

# Replace wav with own samples
# using 'sox' to convert to 32KHz, 16bit, mono
# longer samples can be trimmed with 'fade 0 0.2 0.01', ie trim to 0.2s with 10ms fade out.

# Or render a short file of 'silence'
# sox -n $ss unpacked/sample-01-4.wav trim 0.0 0.001

export ss="-r 32000 -c 1 -b 16 -e signed"

# PCM "only" pads
# Tom 1
sox samples/"Violin tom 001.wav" $ss unpacked/sample-01-1.wav fade 0 0.18 0.01
sox samples/"Violin tom 002.wav" $ss unpacked/sample-01-2.wav fade 0 0.18 0.01
sox samples/"Violin tom 003.wav" $ss unpacked/sample-01-3.wav fade 0 0.18 0.01
sox samples/"Violin tom 004.wav" $ss unpacked/sample-01-4.wav fade 0 0.12 0.01
sox samples/"Hard wood 003.wav"  $ss unpacked/sample-01-5.wav fade 0 0.12 0.01

# Tom2
sox samples/"Light wood 001.wav"  $ss unpacked/sample-02-1.wav fade 0 0.1 0.01
sox samples/"Light wood 002.wav"  $ss unpacked/sample-02-2.wav fade 0 0.1 0.01
sox samples/"Light wood 003.wav"  $ss unpacked/sample-02-3.wav fade 0 0.1 0.01
sox samples/"Light wood 004.wav"  $ss unpacked/sample-02-4.wav fade 0 0.1 0.01
sox samples/"Light wood 005.wav"  $ss unpacked/sample-02-5.wav fade 0 0.1 0.01

# Rim
sox samples/"Violin side soft 001.wav" $ss unpacked/sample-03-1.wav fade 0 0.2 0.01
sox samples/"Violin side soft 002.wav" $ss unpacked/sample-03-2.wav fade 0 0.3 0.01
sox samples/"Violin side soft 003.wav" $ss unpacked/sample-03-3.wav fade 0 0.2 0.01
sox samples/"Hard wood 001.wav"        $ss unpacked/sample-03-4.wav fade 0 0.2 0.01
sox samples/"Hard wood 002.wav"        $ss unpacked/sample-03-5.wav fade 0 0.2 0.01

# Cowbell
sox samples/"String sFx short 001.wav" $ss unpacked/sample-04-1.wav fade 0 0.1 0.01
sox samples/"String sFx short 002.wav" $ss unpacked/sample-04-2.wav fade 0 0.1 0.01
sox samples/"String sFx short 003.wav" $ss unpacked/sample-04-3.wav fade 0 0.3 0.01
sox samples/"String sFx slow 001.wav"  $ss unpacked/sample-04-4.wav fade 0 0.3 0.01
sox samples/"String sFx slow 002.wav"  $ss unpacked/sample-04-5.wav fade 0 0.2 0.01

# Ride
sox samples/"Rim wood 001.wav"         $ss unpacked/sample-05-1.wav fade 0 0.3 0.01
sox samples/"Rim wood 002.wav"         $ss unpacked/sample-05-2.wav fade 0 0.3 0.01
sox samples/"Rim wood 003.wav"         $ss unpacked/sample-05-3.wav fade 0 0.3 0.01
sox samples/"Violin metallic 001.wav"  $ss unpacked/sample-05-4.wav fade 0 0.3 0.01
sox samples/"Violin metallic 002.wav"  $ss unpacked/sample-05-5.wav fade 0 0.3 0.01

# Cymbal
sox samples/"Vln loose str hit 001.wav"  $ss unpacked/sample-06-1.wav fade 0 0.16 0.01
sox samples/"Vln loose str hit 002.wav"  $ss unpacked/sample-06-2.wav fade 0 0.16 0.01
sox samples/"Vln loose str hit 003.wav"  $ss unpacked/sample-06-3.wav fade 0 0.16 0.01
sox samples/"Vln loose str hit 004.wav"  $ss unpacked/sample-06-4.wav fade 0 0.16 0.01
sox samples/"Vln loose str hit 005.wav"  $ss unpacked/sample-06-5.wav fade 0 0.1 0.01

# Analog + PCM pads
# Kick1
sox samples/"Violin mF 001.wav"        $ss unpacked/sample-07-1.wav fade 0 0.2 0.01
sox samples/"Violin mF 002.wav"        $ss unpacked/sample-07-2.wav fade 0 0.2 0.01
sox samples/"Violin mF 003.wav"        $ss unpacked/sample-07-3.wav fade 0 0.2 0.01
sox samples/"Vln low w string 001.wav" $ss unpacked/sample-07-4.wav fade 0 0.2 0.01

# Kick2
sox samples/"Violin mP 001.wav"        $ss unpacked/sample-08-1.wav fade 0 0.2 0.01
sox samples/"Violin mP 002.wav"        $ss unpacked/sample-08-2.wav fade 0 0.2 0.01
sox samples/"Violin mP 003.wav"        $ss unpacked/sample-08-3.wav fade 0 0.2 0.01
sox samples/"Vln low w string 002.wav" $ss unpacked/sample-08-4.wav fade 0 0.2 0.01

# Snare
sox samples/"Violin F 001.wav" $ss unpacked/sample-09-1.wav fade 0 0.2 0.01
sox samples/"Violin F 002.wav" $ss unpacked/sample-09-2.wav fade 0 0.2 0.01
sox samples/"Violin P 001.wav" $ss unpacked/sample-09-3.wav fade 0 0.2 0.01
sox samples/"Violin P 002.wav" $ss unpacked/sample-09-4.wav fade 0 0.2 0.01

# Closed High-Hat
sox samples/"Clicky wood 001.wav" $ss unpacked/sample-10-1.wav fade 0 0.18 0.01
sox samples/"Clicky wood 002.wav" $ss unpacked/sample-10-2.wav fade 0 0.18 0.01
sox samples/"Clicky wood 003.wav" $ss unpacked/sample-10-3.wav fade 0 0.08 0.01
sox samples/"Clicky wood 004.wav" $ss unpacked/sample-10-4.wav fade 0 0.18 0.01

# Open High-Hat
sox samples/"Vln high w string 001.wav"  $ss unpacked/sample-11-1.wav fade 0 0.2 0.01
sox samples/"Vln high w string 002.wav"  $ss unpacked/sample-11-2.wav fade 0 0.2 0.01
sox samples/"Vln high w string 003.wav"  $ss unpacked/sample-11-3.wav fade 0 0.3 0.01
sox samples/"Vln low w string 003.wav"   $ss unpacked/sample-11-4.wav fade 0 0.2 0.01

# Clap
sox samples/"Wood normale 001.wav"  $ss unpacked/sample-12-1.wav fade 0 0.2 0.01
sox samples/"Wood normale 002.wav"  $ss unpacked/sample-12-2.wav fade 0 0.2 0.01
sox samples/"Wood normale 003.wav"  $ss unpacked/sample-12-3.wav fade 0 0.2 0.01
sox samples/"String sFx fast.wav"   $ss unpacked/sample-12-4.wav fade 0 2.0 0.01


# repack into UNO Drum soundpack
#soxi -V1 `find unpacked -name '*.wav' | sort -n ` > after.txt
python3 ../decode_sound_packs.py --pack unpacked -o Uno_Drum_lib_TCIPk.dfu

python3 ../decode_sound_packs.py -s Uno_Drum_lib_TCIPk.dfu
