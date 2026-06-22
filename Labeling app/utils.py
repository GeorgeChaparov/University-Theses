import os
import pandas as pd
import json

from PyQt6.QtWidgets import QFileDialog

import globals
from modules import Event

def load_settings():
    try:
        with open(globals.vidDetails.root + "settings.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            offset_x = data["offset_x"]
            offset_y = data["offset_y"]
            overlay_delay = data["overlay_delay"]

            return offset_x, offset_y, overlay_delay
    except FileNotFoundError:
        print("Settings file does not exist")

        return 0,0,0


def load_data():
        """
            Lets the user select a folder. 
            Goes trough each sub folder in the selected folder and finds the gaze data as well as 
            it searches for labels that may have been created before that, and loads them. 
            It does the same for the workspace video feed.
        """
        events: list[Event]= []

        dir = QFileDialog.getExistingDirectory(None, "Choose folder")

        for entry in os.scandir(dir):
            if not entry.is_dir():
                continue
            

            if entry.name.find("_Data") != -1:
               
                path = dir + "/" + entry.name + "/"
                globals.vidDetails.root = path

                gaze_df = pd.read_csv(path + "gaze.csv")
                print(f"Loading {path}gaze.csv")

                globals.vidDetails.recording_id = gaze_df["recording id"][0]
                gaze_df = gaze_df.dropna(subset=["gaze x [px]", "gaze y [px]"])

                gaze_df["timestamp [ms]"] = gaze_df["timestamp [ns]"] / 1_000_000
                gaze_df["timestamp [ms]"] -= gaze_df["timestamp [ms]"].iloc[0]

                globals.vidDetails.gaze_df = gaze_df.sort_values("timestamp [ms]").reset_index(drop=True)
                globals.vidDetails.gaze_timestamp = gaze_df["timestamp [ms]"].values

                if os.path.exists(path + "labels.csv"):
                    globals.vidDetails.output_path = path + "labels.csv"

                    labels_file = pd.read_csv(globals.vidDetails.output_path)
                    labels_arr = labels_file.to_numpy()

                    start_time = 0
                    end_time = 0

                    for row in labels_arr:
                        
                        start_time = row[1]
                        end_time = row[2]
                        label = row[3]
                        event = Event(start_time, end_time, label)

                        events.append(event)

            elif entry.name.find("_Raw") != -1:
                globals.vidDetails.path = dir + "/" + entry.name + "/Neon Scene Camera v1 ps1.mp4"

        return events

def save_df_to_csv(df: pd.DataFrame, override: bool = False):
    path = globals.vidDetails.output_path

    if os.path.exists(path):
        df.to_csv(path, mode = "w" if override else "a", index=False)
    else:
        df.to_csv(path, index=False)

def save_settings(settings):
    with open(globals.vidDetails.root + "settings.json", "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)

def validate_list_index(index, list):
    if index < 0 :
        print("The given index was smaller then 0")
        index = 0

    list_len = len(list)

    if list_len == 0:
        raise IndexError("The list is empty")

    if index >= list_len:
        print("The given index was bigger then the length of the list")
        index = list_len - 1

    return index