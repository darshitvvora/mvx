"""
 @file
 @brief This file loads the Animation dialog (i.e about Openshot Project)

 """

import os
from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from classes import info, ui_util
from classes.logger import log
from classes.app import get_app
from classes.metrics import *
from windows.views.credits_treeview import CreditsTreeView

try:
    import json
except ImportError:
    import simplejson as json


class Animation(QDialog):
    """ Animation Dialog """

    ui_path = os.path.join(info.PATH, 'windows', 'ui', 'animation.ui')

    def __init__(self):
        # Create dialog class
        QDialog.__init__(self)

        # Load UI from designer
        ui_util.load_ui(self, self.ui_path)

        # Init Ui
        ui_util.init_ui(self)

        # get translations
        self.app = get_app()
        _ = self.app._tr

        # Track metrics
        #track_metric_screen("animation-screen")
