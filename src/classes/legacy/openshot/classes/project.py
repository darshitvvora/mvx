"""
 @file
 @brief This file is for legacy support of OpenShot 1.x project files

 """

import os
from classes.legacy.openshot.classes import files


class project():
    """This is the main project class that contains all
    the details of a project, such as name, folder, timeline
    information, sequences, media files, etc..."""

    # ----------------------------------------------------------------------
    def __init__(self, init_threads=True):
        """Constructor"""

        # debug message/function control
        self.DEBUG = True

        # define common directories containing resources
        # get the base directory of the openshot installation for all future relative references
        # Note: don't rely on __file__ to be an absolute path. E.g., in the debugger (pdb) it will be
        # a relative path, so use os.path.abspath()
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.UI_DIR = os.path.join(self.BASE_DIR, "magicvideox", "windows", "ui")
        self.IMAGE_DIR = os.path.join(self.BASE_DIR, "magicvideox", "images")
        self.LOCALE_DIR = os.path.join(self.BASE_DIR, "magicvideox", "locale")
        self.PROFILES_DIR = os.path.join(self.BASE_DIR, "magicvideox", "profiles")
        self.TRANSITIONS_DIR = os.path.join(self.BASE_DIR, "magicvideox", "transitions")
        self.BLENDER_DIR = os.path.join(self.BASE_DIR, "magicvideox", "blender")
        self.EXPORT_PRESETS_DIR = os.path.join(self.BASE_DIR, "magicvideox", "export_presets")
        self.EFFECTS_DIR = os.path.join(self.BASE_DIR, "magicvideox", "effects")
        # location for per-session, per-user, files to be written/read to
        self.DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
        self.USER_DIR = os.path.join(os.path.expanduser("~"), ".magicvideox")
        self.THEMES_DIR = os.path.join(self.BASE_DIR, "magicvideox", "themes")
        self.USER_PROFILES_DIR = os.path.join(self.USER_DIR, "user_profiles")
        self.USER_TRANSITIONS_DIR = os.path.join(self.USER_DIR, "user_transitions")

        # init the variables for the project
        self.name = "Default Project"
        self.folder = self.USER_DIR
        self.project_type = None
        self.canvas = None
        self.is_modified = False
        self.refresh_xml = True
        self.mlt_profile = None

        # reference to the main GTK form
        self.form = None

        # init the file / folder list (used to populate the tree)
        self.project_folder = files.OpenShotFolder(self)

        # ini the sequences collection
        self.sequences = []

        # init the tab collection
        self.tabs = []
