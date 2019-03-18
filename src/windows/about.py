"""
 @file
 @brief This file loads the About dialog (i.e about Openshot Project)
 @author Jonathan Thomas <jonathan@openshot.org>
 @author Olivier Girard <olivier@openshot.org>

 @section LICENSE

 Copyright (c) 2008-2018 OpenShot Studios, LLC
 (http://www.openshotstudios.com). This file is part of
 OpenShot Video Editor (http://www.openshot.org), an open-source project
 dedicated to delivering high quality video editing and animation solutions
 to the world.

 OpenShot Video Editor is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 OpenShot Video Editor is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with OpenShot Library.  If not, see <http://www.gnu.org/licenses/>.
 """

import os
import codecs
from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from classes import info, ui_util
from classes.logger import log
from classes.app import get_app
from classes.metrics import *
#from windows.views.credits_treeview import CreditsTreeView

try:
    import json
except ImportError:
    import simplejson as json

import datetime

class About(QDialog):
    """ About Dialog """

    ui_path = os.path.join(info.PATH, 'windows', 'ui', 'about.ui')

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

        #create_text = _('Your X-Factor for composing amazing videos')
        description_text = _('Magic VideoX Pro is simple, intuitive and amazing video editing software. Your X-Factor for composing amazing videos')
        #learnmore_text = _('Learn more')
        #copyright_text = _('Copyright &copy; %(begin_year)s-%(current_year)s') % {'begin_year': '2008', 'current_year': str(datetime.datetime.today().year) }
        #about_html = '<html><head/><body><hr/><p align="center"><span style=" font-size:10pt; font-weight:600;">%s</span></p><p align="center"><span style=" font-size:10pt;">%s </span><a href="http://%s.openshot.org?r=about-us"><span style=" font-size:10pt; text-decoration: none; color:#55aaff;">%s</span></a><span style=" font-size:10pt;">.</span></p></body></html>' % (create_text, description_text, info.website_language(), learnmore_text)
        #company_html = '<html><head/><body style="font-size:11pt; font-weight:400; font-style:normal;">\n<hr />\n<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:10pt; font-weight:600;">%s </span><a href="http://%s.openshotstudios.com?r=about-us"><span style=" font-size:10pt; font-weight:600; text-decoration: none; color:#55aaff;">OpenShot Studios, LLC<br /></span></a></p></body></html>' % (copyright_text, info.website_language())

        # Set description and company labels
        self.lblAboutDescription.setText(description_text)
        #self.lblAboutCompany.setText(company_html)

        # set events handlers
        #self.btncredit.clicked.connect(self.load_credit)
        #self.btnlicense.clicked.connect(self.load_license)

        # Init some variables
        #self.txtversion.setText(_("Version: %s") % info.VERSION)
        self.txtversion.setAlignment(Qt.AlignCenter)

        # Track metrics
        #track_metric_screen("about-screen")


