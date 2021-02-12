# Create a demo sound pack using the samples from "DrumSamples.org-DS1000.zip"
# https://archive.org/details/DrumSamples.orgDS1000archive

# unpack and dump info
rm -r unpacked Uno_Drum_lib_DrumSamples-DS1000.dfu

python3 ../decode_sound_packs.py --unpack unpacked Uno_Drum_lib.dfu 
soxi -V1 `find unpacked -name '*.wav' | sort -n ` > before.txt
soxi -V1 `find DrumSamples.org-DS1000 -name '*.wav' | sort -n ` > DrumSamples-DS1000.txt

# Replace wav with own samples... 'sox' converts to 32KHz, 16bit, mono
# longer samples can be trimmed with 'fade 0 0.2 0.01', ie trim to 0.2s with 10ms fade out.
export ss="-r 32000 -c 1 -b 16 -e signed"

# PCM "only" pads
# Tom 1
sox DrumSamples.org-DS1000/TomTomDrums/tomtomdrum2.wav $ss unpacked/sample-01-1.wav fade 0 0.35 0.01
sox DrumSamples.org-DS1000/TomTomDrums/tomtomdrum3.wav $ss unpacked/sample-01-2.wav fade 0 0.45 0.01
sox DrumSamples.org-DS1000/TomTomDrums/tomtomdrum5.wav $ss unpacked/sample-01-3.wav fade 0 0.45 0.01
sox DrumSamples.org-DS1000/TomTomDrums/tomtomdrum6.wav $ss unpacked/sample-01-4.wav fade 0 0.35 0.01
sox DrumSamples.org-DS1000/TomTomDrums/tomtomdrum10.wav $ss unpacked/sample-01-5.wav fade 0 0.45 0.01

# Tom2
sox DrumSamples.org-DS1000/KettleDrums/kettledrum1.wav $ss unpacked/sample-02-1.wav fade 0 0.6 0.01
sox DrumSamples.org-DS1000/KettleDrums/kettledrum6.wav $ss unpacked/sample-02-2.wav fade 0 0.4 0.01
sox DrumSamples.org-DS1000/KettleDrums/kettledrum7.wav $ss unpacked/sample-02-3.wav fade 0 0.4 0.01
sox DrumSamples.org-DS1000/KettleDrums/kettledrum8.wav $ss unpacked/sample-02-4.wav fade 0 0.3 0.01
sox DrumSamples.org-DS1000/KettleDrums/kettledrum9.wav $ss unpacked/sample-02-5.wav fade 0 0.2 0.01

# Rim
touch unpacked/sample-03-1.wav
touch unpacked/sample-03-2.wav
touch unpacked/sample-03-3.wav
touch unpacked/sample-03-4.wav
touch unpacked/sample-03-5.wav
rm unpacked/sample-03-5.wav

# Cowbell
sox DrumSamples.org-DS1000/Cowbells/cowbell2.wav $ss unpacked/sample-04-1.wav
sox DrumSamples.org-DS1000/Cowbells/cowbell3.wav $ss unpacked/sample-04-2.wav
sox DrumSamples.org-DS1000/Cowbells/cowbell4.wav $ss unpacked/sample-04-3.wav fade 0 0.25 0.01
sox DrumSamples.org-DS1000/Cowbells/cowbell5.wav $ss unpacked/sample-04-4.wav
sox DrumSamples.org-DS1000/Cowbells/cowbell9.wav $ss unpacked/sample-04-5.wav

# Ride
sox DrumSamples.org-DS1000/Rattles/rattle2.wav $ss unpacked/sample-05-1.wav fade 0 0.45 0.01
sox DrumSamples.org-DS1000/Rattles/rattle3.wav $ss unpacked/sample-05-2.wav fade 0 0.3 0.01
sox DrumSamples.org-DS1000/Rattles/rattle8.wav $ss unpacked/sample-05-3.wav
sox DrumSamples.org-DS1000/Triangles/triangle2.wav $ss unpacked/sample-05-4.wav fade 0 0.35 0.01
sox DrumSamples.org-DS1000/Triangles/triangle8.wav $ss unpacked/sample-05-5.wav fade 0 0.32 0.01

# Cymbal
touch unpacked/sample-06-1.wav
touch unpacked/sample-06-2.wav
touch unpacked/sample-06-3.wav
touch unpacked/sample-06-4.wav
touch unpacked/sample-06-5.wav
rm unpacked/sample-06-5.wav

# Analog + PCM pads
# Kick1
touch unpacked/sample-07-1.wav
touch unpacked/sample-07-2.wav
rm unpacked/sample-07-3.wav
rm unpacked/sample-07-4.wav

# Kick2
touch unpacked/sample-08-1.wav
touch unpacked/sample-08-2.wav
rm unpacked/sample-08-3.wav
rm unpacked/sample-08-4.wav

# Snare
touch unpacked/sample-09-1.wav
touch unpacked/sample-09-2.wav
touch unpacked/sample-09-3.wav
touch unpacked/sample-09-4.wav

# Closed High-Hat
touch unpacked/sample-10-1.wav
touch unpacked/sample-10-2.wav
touch unpacked/sample-10-3.wav
touch unpacked/sample-10-4.wav

# Open High-Hat
touch unpacked/sample-11-1.wav
touch unpacked/sample-11-2.wav
touch unpacked/sample-11-3.wav
touch unpacked/sample-11-4.wav

# Clap
touch unpacked/sample-12-1.wav
touch unpacked/sample-12-2.wav
touch unpacked/sample-12-3.wav
touch unpacked/sample-12-4.wav


# repack using orignal DFU as template
soxi -V1 `find unpacked -name '*.wav' | sort -n ` > after.txt
python3 ../decode_sound_packs.py --pack unpacked -o Uno_Drum_lib_DrumSamples-DS1000.dfu Uno_Drum_lib.dfu 

python3 ../decode_sound_packs.py -s Uno_Drum_lib_DrumSamples-DS1000.dfu
