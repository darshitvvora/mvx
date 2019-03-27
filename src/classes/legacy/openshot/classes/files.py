"""
 @file
 @brief This file is for legacy support of OpenShot 1.x project files

 """

import uuid


class OpenShotFile:
    """The generic file object for OpenShot"""

    # ----------------------------------------------------------------------
    def __init__(self, project=None):
        """Constructor"""
        self.project = project

        # init the variables for the File Object
        self.name = ""  # short / friendly name of the file
        self.length = 0.0  # length in seconds
        self.videorate = (30, 0)  # audio rate or video framerate
        self.file_type = ""  # video, audio, image, image sequence
        self.max_frames = 0.0
        self.fps = 0.0
        self.height = 0
        self.width = 0
        self.label = ""  # user description of the file
        self.thumb_location = ""  # file uri of preview thumbnail
        self.ttl = 1  # time-to-live - only used for image sequence.  Represents the # of frames per image.

        self.unique_id = str(uuid.uuid1())
        self.parent = None
        self.project = project  # reference to project

        self.video_codec = ""
        self.audio_codec = ""
        self.audio_frequency = ""
        self.audio_channels = ""


class OpenShotFolder:
    """The generic folder object for OpenShot"""

    # ----------------------------------------------------------------------
    def __init__(self, project=None):
        """Constructor"""

        # Init the variables for the Folder Object
        self.name = ""  # short / friendly name of the folder
        self.location = ""  # file system location
        self.parent = None
        self.project = project

        self.label = ""  # user description of the folder
        self.unique_id = str(uuid.uuid1())

        # init the list of files & folders
        # this list can contain OpenShotFolder or OpenShotFile objects
        # the order of this list determines the order of the tree items
        self.items = []

        # this queue holds files that are currently being added. this prevents
        # duplicate files to be added at the same time
        self.queue = []
