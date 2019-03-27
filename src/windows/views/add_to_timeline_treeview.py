""" 
 @file
 @brief This file contains the add to timeline file treeview

 """

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *

from classes.logger import log
from classes.app import get_app
from windows.models.add_to_timeline_model import TimelineModel

try:
    import json
except ImportError:
    import simplejson as json


class TimelineTreeView(QTreeView):
    """ A TreeView QWidget used on the add to timeline window """

    def currentChanged(self, selected, deselected):
        # Get selected item
        self.selected = selected
        self.deselected = deselected

        # Get translation object
        _ = self.app._tr

    def contextMenuEvent(self, event):
        # # Ignore event, propagate to parent
        event.ignore()

    def mousePressEvent(self, event):

        # Ignore event, propagate to parent
        event.ignore()
        super().mousePressEvent(event)

    def refresh_view(self):
        self.timeline_model.update_model()
        self.hideColumn(2)

    def __init__(self, *args):
        # Invoke parent init
        QTreeView.__init__(self, *args)

        # Get a reference to the window object
        self.app = get_app()
        self.win = args[0]

        # Get Model data
        self.timeline_model = TimelineModel()

        # Keep track of mouse press start position to determine when to start drag
        self.selected = None
        self.deselected = None

        # Setup header columns
        self.setModel(self.timeline_model.model)
        self.setIconSize(QSize(131, 108))
        self.setIndentation(0)
        self.setSelectionBehavior(QTreeView.SelectRows)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setWordWrap(True)
        self.setStyleSheet('QTreeView::item { padding-top: 2px; }')

        # Refresh view
        self.refresh_view()
