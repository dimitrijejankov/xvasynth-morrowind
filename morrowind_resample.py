import os
from glob import glob

# ".\lame.exe -b 64 --resample 44.1 -a .\fbmwa1sleepers_1sixthshouse_0001c198_1.wav .\out.mp3"
paths = glob('D:\\mw_data\\sound\\voice\\morrowind_ob.esm\\imperial\\f\\*')
for p in paths:

    input = str(p)
    output = (input[0:-4] + ".mp3").replace("mw_data", "mw_data_resampled")

    os.system("D:\\lame.exe -b 64 --resample 44.1 -a %s %s" % (input, output))

paths = glob('D:\\mw_data\\sound\\voice\\morrowind_ob.esm\\imperial\\f\\*')
for p in paths:

    input = str(p)
    output = (input[0:-4] + ".mp3").replace("mw_data", "mw_data_resampled")

    os.system("D:\\lame.exe -b 64 --resample 44.1 -a %s %s" % (input, output))
