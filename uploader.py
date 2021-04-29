import os
from PIL import Image
from datamanager import DataManager

gdrive = DataManager()


def notes_uploader(remove_files=True):
    notes_pics = []
    dir = "screenshots"
    new_dirs = [file_in_screenshot for file_in_screenshot in os.listdir(dir) if file_in_screenshot.endswith(".jpg")]
    ss_files = sorted(new_dirs, key=lambda x: int(x.strip("slide").strip(".jpg")))
    for file in ss_files:
        notes_pics.append(Image.open(dir + "\\" + file))

    save_dir = "notes\\{}\\{}".format(title, datetime.now().strftime("%d-%m-%y"))
    filename = "{}\\{}.pdf".format(save_dir, datetime.now().strftime("%I%M"))
    try:
        os.makedirs(save_dir)
    except FileExistsError:
        pass
    notes_pics[0].save(filename, save_all=True, append_images=notes_pics[1:])
    gdrive.upload_notes(filename)

    if remove_files:
        for file in os.listdir(dir):
            os.remove(dir + "\\" + file)


def file_upload(fp, type=None):
    if type is None:
        folder_name = input("Folder Name:\n")
        gdrive.upload(folder_name, fp)
    elif "note" in type.lower():
        gdrive.upload_notes(fp)
    elif "down" in type.lower():
        gdrive.upload_down(fp)
    elif "svg" in type.lower():
        gdrive.upload_svg(fp)




def main():
    a = int(input("make notes(1) or upload files(2):\n"))
    if a == 1:
        t = input("Remove files(y)?\n")=="y"
        notes_uploader(t)
    else:
        type = input("Type of Upload: ")
        fp = input("File Path:\n")
        file_upload(fp, type)


main()


