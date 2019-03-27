"""
 @file
 @brief This file is for legacy support of OpenShot 1.x project files

 """

import uuid


class transition:
    """This class represents a media clip on the timeline."""

    # ----------------------------------------------------------------------
    def __init__(self, name, position_on_track, length, resource, parent, type="transition", mask_value=50.0):
        """Constructor"""

        # init variables for clip object
        self.name = name
        self.position_on_track = float(position_on_track)  # the time in seconds where the transition starts on the timeline
        self.length = float(length)  # the length in seconds of this transition
        self.resource = resource  # Any grey-scale image, or leave empty for a dissolve
        self.softness = 0.3  # 0.0 = no softness. 1.0 = too soft.
        self.reverse = False
        self.unique_id = str(uuid.uuid1())
        self.parent = parent  # the sequence

        # mask settings
        self.type = type  # transition or mask
        self.mask_value = mask_value  # 0.0 to 1.0

        # init vars for drag n drop
        self.drag_x = 0.0
        self.drag_y = 0.0
