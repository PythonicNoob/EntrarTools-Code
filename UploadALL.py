from os import walk
from datamanager import  DataManager

a = DataManager()
for (dirpath, dirnames, filenames) in walk("presentation_downloaded"):
    for filename in filenames:
        print(dirpath+filename)
        a.upload_down(f'{dirpath}\\{filename}')


for (dirpath, dirnames, filenames) in walk("presentation"):
    for filename in filenames:
        print(dirpath+filename)
        a.upload_svg(f'{dirpath}\\{filename}')