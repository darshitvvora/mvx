"""
 @file
 @brief This file is for legacy support of OpenShot 1.x project files

 """

import uuid


class keyframe:
    """This class represents a media clip on the timeline."""

    # ----------------------------------------------------------------------
    def __init__(self, frame, height, width, x, y, alpha):
        """Constructor"""

        # init variables for keyframe object
        self.frame = frame
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.alpha = alpha
        self.unique_id = str(uuid.uuid1())
