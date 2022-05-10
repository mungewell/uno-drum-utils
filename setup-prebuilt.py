from cx_Freeze import setup, Executable

base = None    

executables = [Executable("decode_sound_packs.py", base=base)]

packages = ["construct", "os", "optparse", "sys", "binascii", "crcmod"]
options = {
    'build_exe': {    
        'packages':packages,
        'excludes':["pygame", "numpy"],
    },    
}

setup(
    name = "decode_sound_packs.py",
    options = options,
    version = "0.2.0.0",
    description = 'Script for unpacking/packing DFU SoundPacks for UNO Drum',
    executables = executables
)
