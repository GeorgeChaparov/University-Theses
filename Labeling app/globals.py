import pandas as pd

class VideoDetails:
    """
    Stores shared recording data.
    Attributes:
        root: the root directory.
        recording_id: The id of the recording.
        gaze_df: The dataframe that holds the gaze data.
        path: The path to the video source.
        output_path: the path to which the events should be saved.
        gaze_timestamp: All of the gaze data timestamps.
    """

    root = ""
    recording_id = 0
    gaze_df: pd.DataFrame = None
    path = ""
    output_path = "labels.csv"
    gaze_timestamp = 0


vidDetails = VideoDetails()