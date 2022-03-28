import os
import shutil

wav_container= "D:\\TESIS\\tesis-data-base\\waveform_names.out"
destiny = 'D:\\TESIS\\datos\\wav'
path_to_find= "E:\\wav2010-2020"

def findfile(name, path):
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)

with open(wav_container, "r") as fname:
	files = fname.readlines()
linea = 0
not_found = 0
for file in files:    
    origin = findfile(file.strip('\n'), path_to_find)
    if origin is not None:
        shutil.copy(origin, destiny)
        linea = linea +1
        print(linea)
    else:
        not_found= not_found +1
print('No encontrados')
print(not_found)