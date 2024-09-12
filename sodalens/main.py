from time import sleep, time
from easygui import multenterbox
import os
import sys

title = "Dataset Maker"
msg = "Captura de imagens"
fieldNames = [
    "Nome do Projeto",
    "Nome da Classe",
    "Tempo de captura (em segundos)",
    "Intervalo de captura (em segundos)",
]
fieldValues = multenterbox(msg, title, fieldNames)
if fieldValues is None:
    sys.exit(0)
# make sure that none of the fields were left blank
while 1:
    errmsg = ""
    for i, name in enumerate(fieldNames):
        if fieldValues[i].strip() == "":
            errmsg += "{} e um campo necessario.\n\n".format(name)
    try:
        int(fieldValues[2])
        int(fieldValues[3])
    except:
        errmsg += "O tempo deve ser numeral"
    if errmsg == "":
        break  # no problems found
    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    if fieldValues is None:
        break

project = fieldValues[0].lower().replace(" ", "-")
classe = fieldValues[1].lower().replace(" ", "-")
open_time = int(fieldValues[2].strip())
timelapse = int(fieldValues[3].strip())


usr = os.path.expanduser("~")
dataset_path = usr + "/Desktop/datasets/"
project_path = dataset_path + project + "/"
class_path = project_path + classe + "/"

datasets = os.listdir(dataset_path)
if not project in datasets:
    os.mkdir(project_path)

all_classes = os.listdir(project_path)
if not classe in (all_classes):
    os.mkdir(class_path)


def current_milli_time():
    return round(time() * 1000)


end_time = current_milli_time() + (open_time * 1000)
time_to_capture = current_milli_time()

while current_milli_time() < end_time:
    if current_milli_time() >= time_to_capture:
        time_to_capture = current_milli_time() + (timelapse * 1000)
        file_name = class_path + str(time()) + ".jpg"
        try:
            cmd = (
                "ffmpeg -f v4l2 -video_size 1080x1080 -i /dev/video0 -vframes 1 %s"
                % (file_name)
            )
            os.system(cmd)
        except:
            try:
                cmd = (
                    "ffmpeg -f v4l2 -video_size 1080x1080 -i /dev/video1 -vframes 1 %s"
                    % (file_name)
                )
                os.system(cmd)
            except:
                pass