"""
 @file
 @brief This file loads the Choose Profile dialog

 """

import os
import sys
import functools

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5 import uic
import openshot  # Python module for libopenshot (required video editing module installed separately)

from classes import info, ui_util, settings, qt_types, updates
from classes.app import get_app
from classes.logger import log
from classes.metrics import *


class Profile(QDialog):
    """ Choose Profile Dialog """

    # Path to ui file
    ui_path = os.path.join(info.PATH, 'windows', 'ui', 'profile.ui')

    def __init__(self):

        # Create dialog class
        QDialog.__init__(self)

        # Load UI from designer
        ui_util.load_ui(self, self.ui_path)

        # Init UI
        ui_util.init_ui(self)

        # get translations
        app = get_app()
        _ = app._tr

        # Get settings
        self.s = settings.get_settings()

        # Pause playback (to prevent crash since we are fixing to change the timeline's max size)
        get_app().window.actionPlay_trigger(None, force="pause")

        # Track metrics
        #track_metric_screen("profile-screen")

        # Loop through profiles
        self.profile_names = []
        self.profile_paths = {}
        for profile_folder in [info.USER_PROFILES_PATH, info.PROFILES_PATH]:
            for file in os.listdir(profile_folder):
                # Load Profile
                profile_path = os.path.join(profile_folder, file)
                profile = openshot.Profile(profile_path)

                # Add description of Profile to list
                profile_name = "%s (%sx%s)" % (profile.info.description, profile.info.width, profile.info.height)
                self.profile_names.append(profile_name)
                self.profile_paths[profile_name] = profile_path

        # Sort list
        self.profile_names.sort()

        # Loop through sorted profiles
        box_index = 0
        selected_index = 0
        for profile_name in self.profile_names:

            # Add to dropdown
            self.cboProfile.addItem(profile_name, self.profile_paths[profile_name])

            # Set default (if it matches the project)
            if app.project.get(['profile']) in profile_name:
                selected_index = box_index

            # increment item counter
            box_index += 1


        # Connect signal
        self.cboProfile.currentIndexChanged.connect(functools.partial(self.dropdown_index_changed, self.cboProfile))

        # Set current item (from project)
        self.cboProfile.setCurrentIndex(selected_index)

    def dropdown_index_changed(self, widget, index):
        # Get profile path
        value = self.cboProfile.itemData(index)
        log.info(value)

        # Load profile
        profile = openshot.Profile(value)

        # Set labels
        self.lblSize.setText("%sx%s" % (profile.info.width, profile.info.height))
        self.lblFPS.setText("%0.2f" % (profile.info.fps.num / profile.info.fps.den))
        self.lblOther.setText("DAR: %s/%s, SAR: %s/%s, Interlaced: %s" % (profile.info.display_ratio.num, profile.info.display_ratio.den, profile.info.pixel_ratio.num, profile.info.pixel_ratio.den, profile.info.interlaced_frame))

        # Get current FPS (prior to changing)
        current_fps = get_app().project.get(["fps"])
        current_fps_float = float(current_fps["num"]) / float(current_fps["den"])
        new_fps_float = float(profile.info.fps.num) / float(profile.info.fps.den)
        fps_factor = new_fps_float / current_fps_float

        # Update timeline settings
        get_app().updates.update(["profile"], profile.info.description)
        get_app().updates.update(["width"], profile.info.width)
        get_app().updates.update(["height"], profile.info.height)
        get_app().updates.update(["fps"], {"num" : profile.info.fps.num, "den" : profile.info.fps.den})

        # Rescale all keyframes and reload project
        if fps_factor != 1.0:
            get_app().project.rescale_keyframes(fps_factor)

        # Force ApplyMapperToClips to apply these changes
        get_app().window.timeline_sync.timeline.ApplyMapperToClips()

        # Update Window Title
        get_app().window.SetWindowTitle(profile.info.description)

        # Update max size (to size of video preview viewport)
        viewport_rect = get_app().window.videoPreview.centeredViewport(get_app().window.videoPreview.width(), get_app().window.videoPreview.height())
        get_app().window.timeline_sync.timeline.SetMaxSize(viewport_rect.width(), viewport_rect.height())

        # Refresh frame (since size of preview might have changed)
        QTimer.singleShot(500, get_app().window.refreshFrameSignal.emit)
