""" 
 @file
 @brief Setup script to install EditX Pro (on Linux and without any dependencies such as libopenshot)
 @author DV
 """

import os
import sys
import fnmatch
import subprocess
from setuptools import setup
from shutil import copytree, rmtree, copy


# Determine absolute PATH of OpenShot folder
PATH = os.path.dirname(os.path.realpath(__file__))  # Primary openshot folder

# Make a copy of the src tree (temporary for naming reasons only)
if os.path.exists(os.path.join(PATH, "src")):
    print("Copying modules to openshot_qt directory: %s" % os.path.join(PATH, "openshot_qt"))
    # Only make a copy if the SRC directory is present (otherwise ignore this)
    copytree(os.path.join(PATH, "src"), os.path.join(PATH, "openshot_qt"))

if os.path.exists(os.path.join(PATH, "openshot_qt")):
    # Append path to system path
    sys.path.append(os.path.join(PATH, "openshot_qt"))
    print("Loaded modules from openshot_qt directory: %s" % os.path.join(PATH, "openshot_qt"))


from classes import info
from classes.logger import log

log.info("Execution path: %s" % os.path.abspath(__file__))

# Boolean: running as root?
ROOT = os.geteuid() == 0
# For Debian packaging it could be a fakeroot so reset flag to prevent execution of
# system update services for Mime and Desktop registrations.
# The debian/openshot.postinst script must do those.
if not os.getenv("FAKEROOTKEY") == None:
    log.info("NOTICE: Detected execution in a FakeRoot so disabling calls to system update services.")
    ROOT = False

os_files = [
    # XDG application description
    ('share/applications', ['xdg/openshot-qt.desktop']),
    # AppStream metadata
    ('share/metainfo', ['xdg/openshot-qt.appdata.xml']),
    # Debian menu system application icon
    ('share/pixmaps', ['xdg/openshot-qt.svg']),
    # XDG Freedesktop icon paths
    ('share/icons/hicolor/scalable/apps', ['xdg/openshot-qt.svg']),
    ('share/icons/hicolor/64/apps', ['xdg/icon/64/openshot-qt.png']),
    ('share/icons/hicolor/256/apps', ['xdg/icon/256/openshot-qt.png']),
    ('share/icons/hicolor/512/apps', ['xdg/icon/512/openshot-qt.png']),
    # XDG desktop mime types cache
    ('share/mime/packages', ['xdg/openshot-qt.xml']),
    # launcher (mime.types)
    ('lib/mime/packages', ['xdg/openshot-qt']),
]

# Find files matching patterns
def find_files(directory, patterns):
    """ Recursively find all files in a folder tree """
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if ".pyc" not in basename and "__pycache__" not in basename:
                for pattern in patterns:
                    if fnmatch.fnmatch(basename, pattern):
                        filename = os.path.join(root, basename)
                        yield filename


package_data = {}

# Find all project files
src_files = []
for filename in find_files(os.path.join(PATH, "openshot_qt"), ["*"]):
    src_files.append(filename.replace(os.path.join(PATH, "openshot_qt"), ""))
package_data["openshot_qt"] = src_files

# Call the main Distutils setup command
# -------------------------------------
dist = setup(
    packages=[('openshot_qt')],
    package_data=package_data,
    data_files=os_files,
    include_package_data=True,
    **info.SETUP
)
# -------------------------------------

# Remove temporary folder (if SRC folder present)
if os.path.exists(os.path.join(PATH, "src")):
    rmtree(os.path.join(PATH, "openshot_qt"), True)

FAILED = 'Failed to update.\n'

if ROOT and dist != None:
    # update the XDG Shared MIME-Info database cache
    try:
        sys.stdout.write('Updating the Shared MIME-Info database cache.\n')
        subprocess.call(["update-mime-database", os.path.join(sys.prefix, "share/mime/")])
    except:
        sys.stderr.write(FAILED)

    # update the mime.types database
    try:
        sys.stdout.write('Updating the mime.types database\n')
        subprocess.call("update-mime")
    except:
        sys.stderr.write(FAILED)

    # update the XDG .desktop file database
    try:
        sys.stdout.write('Updating the .desktop file database.\n')
        subprocess.call(["update-desktop-database"])
    except:
        sys.stderr.write(FAILED)
    sys.stdout.write("\n-----------------------------------------------")
    sys.stdout.write("\nInstallation Finished!")
    sys.stdout.write("\nRun EditX Pro by typing 'openshot-qt' or through the Applications menu.")
    sys.stdout.write("\n-----------------------------------------------\n")
