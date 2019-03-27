"""
 @file
 @brief This file is for legacy support of OpenShot 1.x project files

 """

import uuid


class track:
    """The track class contains a simple grouping of clips on the same layer (aka track)."""

    # ----------------------------------------------------------------------
    def __init__(self, track_name, parent_sequence):
        """Constructor"""

        # init variables for sequence
        self.name = track_name
        self.x = 10  # left x coordinate to start the track
        self.y_top = 0  # top y coordinate of this track
        self.y_bottom = 0  # bottom y coordinate of this track
        self.parent = parent_sequence  # reference to parent sequence object
        self.play_video = True
        self.play_audio = True
        self.unique_id = str(uuid.uuid1())

        # init the tracks on the sequence
        self.clips = []

        # init transitions
        self.transitions = []
