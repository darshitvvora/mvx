""" 
 @file
 @brief This file creates the QApplication, and displays the main window

 """

import os
import sys
import platform
from uuid import uuid4
from PyQt5.QtWidgets import QApplication, QStyleFactory, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QFontDatabase, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
import socket


from classes.logger import log
from classes import info, settings, project_data, updates, language, ui_util, logger_libopenshot
import openshot


try:
    # Enable High-DPI resolutions
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
except AttributeError:
    pass # Quietly fail for older Qt5 versions


def get_app():
    """ Returns the current QApplication instance of OpenShot """
    return QApplication.instance()

def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

class OpenShotApp(QApplication):
    """ This class is the primary QApplication for OpenShot.
            mode=None (normal), mode=unittest (testing) """

    def __init__(self, *args, mode=None):
        QApplication.__init__(self, *args)

        # Log some basic system info
        try:
            v = openshot.GetVersion()
            log.info("openshot-qt version: %s" % info.VERSION)
            log.info("libopenshot version: %s" % v.ToString())
            log.info("platform: %s" % platform.platform())
            log.info("processor: %s" % platform.processor())
            log.info("machine: %s" % platform.machine())
            log.info("python version: %s" % platform.python_version())
            log.info("qt5 version: %s" % QT_VERSION_STR)
            log.info("pyqt5 version: %s" % PYQT_VERSION_STR)
        except:
            pass

        # Setup application
        self.setApplicationName('Magic-VideoX-Pro')
        self.setApplicationVersion(info.SETUP['version'])

        # Init settings
        self.settings = settings.SettingStore()
        self.settings.load()

        # Init and attach exception handler
        from classes import exceptions
        sys.excepthook = exceptions.ExceptionHandler

        # Init translation system
        language.init_language()

        # Detect minimum libopenshot version
        _ = self._tr
        libopenshot_version = openshot.GetVersion().ToString()
        if mode != "unittest" and libopenshot_version < info.MINIMUM_LIBOPENSHOT_VERSION:
            QMessageBox.warning(None, _("Wrong Version of libopenshot Detected"),
                                      _("<b>Version %(minimum_version)s is required</b>, but %(current_version)s was detected. Please update libopenshot or download our latest installer.") %
                                {"minimum_version": info.MINIMUM_LIBOPENSHOT_VERSION, "current_version": libopenshot_version})
            # Stop launching and exit
            sys.exit()


        if is_connected() == False:
            log.info("Internet Connection Not Available")
            _ = self._tr
            QMessageBox.warning(None, _("Internet Connection Error"),
                                _("Please check your Internet connectivity"))
            sys.exit()

        # Tests of project data loading/saving
        self.project = project_data.ProjectDataStore()

        # Init Update Manager
        self.updates = updates.UpdateManager()

        # It is important that the project is the first listener if the key gets update
        self.updates.add_listener(self.project)

        # Load ui theme if not set by OS
        ui_util.load_theme()

        # Start libopenshot logging thread
        self.logger_libopenshot = logger_libopenshot.LoggerLibOpenShot()
        self.logger_libopenshot.start()

        # Track which dockable window received a context menu
        self.context_menu_object = None

        # Set Font for any theme
        if self.settings.get("theme") != "No Theme":
            # Load embedded font
            try:
                log.info("Setting font to %s" % os.path.join(info.IMAGES_PATH, "fonts", "Ubuntu-R.ttf"))
                font_id = QFontDatabase.addApplicationFont(os.path.join(info.IMAGES_PATH, "fonts", "Ubuntu-R.ttf"))
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                font = QFont(font_family)
                font.setPointSizeF(10.5)
                QApplication.setFont(font)
            except Exception as ex:
                log.error("Error setting Ubuntu-R.ttf QFont: %s" % str(ex))

        # Set Experimental Dark Theme
        if self.settings.get("theme") == "Humanity: Dark":
            # Only set if dark theme selected
            log.info("Setting custom dark theme")
            self.setStyle(QStyleFactory.create("Fusion"))

            darkPalette = self.palette()
            darkPalette.setColor(QPalette.Window, QColor(64, 64, 64))
            darkPalette.setColor(QPalette.WindowText,  QColor(236, 239, 241))
            darkPalette.setColor(QPalette.Base, QColor(44, 44, 44))
            darkPalette.setColor(QPalette.AlternateBase,  QColor(64, 64, 64))
            darkPalette.setColor(QPalette.ToolTipBase, QColor(236, 239, 241))
            darkPalette.setColor(QPalette.ToolTipText, QColor(236, 239, 241))
            darkPalette.setColor(QPalette.Text, QColor(212, 208, 200))
            darkPalette.setColor(QPalette.Button, QColor(64, 64, 64))
            darkPalette.setColor(QPalette.ButtonText, QColor(236, 239, 241))
            darkPalette.setColor(QPalette.BrightText, Qt.red)
            darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            darkPalette.setColor(QPalette.HighlightedText, Qt.black)
            darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(104, 104, 104))
            self.setPalette(darkPalette)
            self.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 0px solid white; }")

        # Create main window
        from windows.main_window import MainWindow
        self.window = MainWindow(mode)

        # Reset undo/redo history
        self.updates.reset()
        self.window.updateStatusChanged(False, False)

        log.info('Process command-line arguments: %s' % args)
        if len(args[0]) == 2:
            path = args[0][1]
            if ".mvxp" in path:
                # Auto load project passed as argument
                self.window.open_project(path)
            else:
                # Auto import media file
                self.window.filesTreeView.add_file(path)
        else:
            # Recover backup file (this can't happen until after the Main Window has completely loaded)
            self.window.RecoverBackup.emit()

    def _tr(self, message):
        return self.translate("", message)

    # Start event loop
    def run(self):
        """ Start the primary Qt event loop for the interface """

        res = self.exec_()

        try:
            self.settings.save()
        except Exception as ex:
            log.error("Couldn't save user settings on exit.\n{}".format(ex))

        # return exit result
        return res
