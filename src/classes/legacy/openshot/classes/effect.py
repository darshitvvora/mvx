"""
 @file
 @brief This file is for legacy support of OpenShot 1.x project files

 """

import uuid


class effect:
    """This class represents a media clip on the timeline."""

    # ----------------------------------------------------------------------
    def __init__(self, service, paramaters=[]):
        """Constructor"""

        # init variables for clip object
        self.service = service  # the name of the mlt service (i.e. frei0r.water, chroma, sox, etc...)
        self.paramaters = paramaters  # example:  "key" : "123123123",   "variance" : "0.15" (dictionary of settings)
        self.audio_effect = ""
        self.unique_id = str(uuid.uuid1())
