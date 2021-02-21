# Create a demo sound pack using the samples from "DrumSamples.org-DS1000.zip"
# https://archive.org/details/DrumSamples.orgDS1000archive

# unpack and dump info
rm -r unpacked Uno_Drum_lib_DrumSamples-DS1000.dfu
python3 ../decode_sound_packs.py --unpack unpacked Uno_Drum_lib_Anthology8.dfu

# debug info
#soxi -V1 `find unpacked -name '*.wav' | sort -n ` > before.txt
#soxi -V1 `find DrumSamples.org-DS1000 -name '*.wav' | sort -n ` > DrumSamples-DS1000.txt

# Replace wav with own samples
# using 'sox' to convert to 32KHz, 16bit, mono
# longer samples can be trimmed with 'fade 0 0.2 0.01', ie trim to 0.2s with 10ms fade out.

export ss="-r 32000 -c 1 -b 16 -e signed"

# PCM "only" pads
# Tom 1
sox DrumSamples.org-DS1000/Bongos/bongo5.wav $ss unpacked/sample-01-1.wav fade 0 0.17 0.01
sox DrumSamples.org-DS1000/Bongos/bongo6.wav $ss unpacked/sample-01-2.wav fade 0 0.11 0.01
sox DrumSamples.org-DS1000/Bongos/bongo7.wav $ss unpacked/sample-01-3.wav fade 0 0.12 0.01
sox DrumSamples.org-DS1000/Bongos/bongo8.wav $ss unpacked/sample-01-4.wav fade 0 0.10 0.01
sox DrumSamples.org-DS1000/Bongos/bongo9.wav $ss unpacked/sample-01-5.wav fade 0 0.06 0.01

# Tom2
sox DrumSamples.org-DS1000/Congas/conga5.wav $ss unpacked/sample-02-1.wav
sox DrumSamples.org-DS1000/Congas/conga6.wav $ss unpacked/sample-02-2.wav
sox DrumSamples.org-DS1000/Congas/conga7.wav $ss unpacked/sample-02-3.wav
sox DrumSamples.org-DS1000/Congas/conga5.wav $ss unpacked/sample-02-4.wav
sox DrumSamples.org-DS1000/Congas/conga9.wav $ss unpacked/sample-02-5.wav fade 0 0.18 0.01

# Rim
sox DrumSamples.org-DS1000/Rattles/rattle3.wav $ss unpacked/sample-02-1.wav
sox DrumSamples.org-DS1000/Rattles/rattle4.wav $ss unpacked/sample-02-2.wav
sox DrumSamples.org-DS1000/Rattles/rattle5.wav $ss unpacked/sample-02-3.wav
sox DrumSamples.org-DS1000/Tambourines/tambourine2.wav $ss unpacked/sample-02-4.wav
sox DrumSamples.org-DS1000/Tambourines/tambourine3.wav $ss unpacked/sample-02-5.wav

# Cowbell
sox DrumSamples.org-DS1000/Cowbells/cowbell1.wav  $ss unpacked/sample-04-1.wav fade 0 0.09 0.01
sox DrumSamples.org-DS1000/Cowbells/cowbell2.wav  $ss unpacked/sample-04-2.wav
sox DrumSamples.org-DS1000/Cowbells/cowbell3.wav  $ss unpacked/sample-04-3.wav
sox DrumSamples.org-DS1000/Cowbells/cowbell9.wav  $ss unpacked/sample-04-4.wav
sox DrumSamples.org-DS1000/Cowbells/cowbell10.wav $ss unpacked/sample-04-5.wav

# Ride
sox DrumSamples.org-DS1000/Triangles/triangle2.wav  $ss unpacked/sample-05-1.wav fade 0 0.35 0.01
sox DrumSamples.org-DS1000/Triangles/triangle3.wav  $ss unpacked/sample-05-2.wav fade 0 0.42 0.01
sox DrumSamples.org-DS1000/Triangles/triangle4.wav  $ss unpacked/sample-05-3.wav fade 0 0.26 0.01
sox DrumSamples.org-DS1000/Triangles/triangle5.wav  $ss unpacked/sample-05-4.wav fade 0 0.14 0.01
sox DrumSamples.org-DS1000/Triangles/triangle10.wav $ss unpacked/sample-05-5.wav fade 0 0.27 0.01

# Cymbal
sox DrumSamples.org-DS1000/Cymbals1/cymbal1.wav $ss unpacked/sample-06-1.wav fade 0 1.10 0.01
sox DrumSamples.org-DS1000/Cymbals1/cymbal9.wav $ss unpacked/sample-06-2.wav fade 0 0.70 0.01
sox DrumSamples.org-DS1000/Cymbals1/cymbal2.wav $ss unpacked/sample-06-3.wav fade 0 0.82 0.01
sox DrumSamples.org-DS1000/Cymbals1/cymbal3.wav $ss unpacked/sample-06-4.wav fade 0 0.95 0.01
sox DrumSamples.org-DS1000/Cymbals2/cymbalcrash7.wav $ss unpacked/sample-06-5.wav fade 0 0.46 0.01

# Analog + PCM pads
# Kick1
sox DrumSamples.org-DS1000/BassDrums1/bassdrum3.wav  $ss unpacked/sample-07-1.wav
sox DrumSamples.org-DS1000/DistortedKicks1/distortedkick8.wav $ss unpacked/sample-07-2.wav
sox DrumSamples.org-DS1000/BassDrums1/bassdrum9.wav  $ss unpacked/sample-07-3.wav
sox DrumSamples.org-DS1000/BassDrums1/bassdrum15.wav $ss unpacked/sample-07-4.wav

# Kick2
sox DrumSamples.org-DS1000/BassDrums1/bassdrum49.wav $ss unpacked/sample-08-1.wav
sox DrumSamples.org-DS1000/BassDrums2/bassdrum87.wav $ss unpacked/sample-08-2.wav
sox DrumSamples.org-DS1000/BassDrums2/bassdrum90.wav $ss unpacked/sample-08-3.wav
sox DrumSamples.org-DS1000/BassDrums2/bassdrum86.wav $ss unpacked/sample-08-4.wav

# Snare
sox DrumSamples.org-DS1000/DistortedSnares1/distortedsnare6.wav  $ss unpacked/sample-09-1.wav fade 0 0.13 0.01
sox DrumSamples.org-DS1000/DistortedSnares1/distortedsnare21.wav $ss unpacked/sample-09-2.wav
sox DrumSamples.org-DS1000/DistortedSnares1/distortedsnare13.wav $ss unpacked/sample-09-3.wav
sox DrumSamples.org-DS1000/DistortedSnares2/distortedsnare63.wav $ss unpacked/sample-09-4.wav

# Closed High-Hat
sox DrumSamples.org-DS1000/HiHats1/hihat1.wav  $ss unpacked/sample-10-1.wav fade 0 0.16 0.01
sox DrumSamples.org-DS1000/HiHats1/hihat5.wav  $ss unpacked/sample-10-2.wav fade 0 0.10 0.01
sox DrumSamples.org-DS1000/HiHats1/hihat15.wav $ss unpacked/sample-10-3.wav fade 0 0.08 0.01
sox DrumSamples.org-DS1000/HiHats1/hihat46.wav $ss unpacked/sample-10-4.wav fade 0 0.17 0.01

# Open High-Hat
sox DrumSamples.org-DS1000/HiHats1/hihat47.wav $ss unpacked/sample-11-1.wav fade 0 0.13 0.01
sox DrumSamples.org-DS1000/HiHats2/hihat63.wav $ss unpacked/sample-11-2.wav fade 0 0.22 0.01
sox DrumSamples.org-DS1000/HiHats2/hihat94.wav $ss unpacked/sample-11-3.wav fade 0 0.23 0.01
sox DrumSamples.org-DS1000/HiHats2/hihat84.wav $ss unpacked/sample-11-4.wav fade 0 0.18 0.01

# Clap
sox DrumSamples.org-DS1000/KettleDrums/kettledrum1.wav $ss unpacked/sample-12-1.wav fade 0 0.6 0.01
sox DrumSamples.org-DS1000/KettleDrums/kettledrum6.wav $ss unpacked/sample-12-2.wav fade 0 0.4 0.01
sox DrumSamples.org-DS1000/KettleDrums/kettledrum7.wav $ss unpacked/sample-12-3.wav fade 0 0.4 0.01
sox DrumSamples.org-DS1000/KettleDrums/kettledrum8.wav $ss unpacked/sample-12-4.wav fade 0 0.3 0.01


# repack using orignal DFU as template
#soxi -V1 `find unpacked -name '*.wav' | sort -n ` > after.txt
python3 ../decode_sound_packs.py --pack unpacked -o Uno_Drum_lib_DrumSamples-DS1000.dfu Uno_Drum_lib_Anthology8.dfu

python3 ../decode_sound_packs.py -s Uno_Drum_lib_DrumSamples-DS1000.dfu
