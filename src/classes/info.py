""" 
 @file
 @brief This file contains the current version number of EditX Pro, along with other global settings.

 """

import os

from PyQt5.QtCore import QDir

VERSION = "2.4.3-dev3"
MINIMUM_LIBOPENSHOT_VERSION = "0.2.2"
DATE = "20180922000000"
NAME = "editxpro-qt"
PRODUCT_NAME = "Edit X Pro"
GPL_VERSION = "3"
DESCRIPTION = "Create and edit amazing wedding videos and movies"
COMPANY_NAME = "Edit X Pro"
COPYRIGHT = "Copyright (c) 2019 %s" % COMPANY_NAME
CWD = os.getcwd()
PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # Primary openshot folder
HOME_PATH = os.path.join(os.path.expanduser("~"))
USER_PATH = os.path.join(HOME_PATH, ".editxpro_qt")
BACKUP_PATH = os.path.join(USER_PATH, "backup")
BLENDER_PATH = os.path.join(USER_PATH, "blender")
ASSETS_PATH = os.path.join(USER_PATH, "assets")
THUMBNAIL_PATH = os.path.join(USER_PATH, "thumbnail")
CACHE_PATH = os.path.join(USER_PATH, "cache")
PREVIEW_CACHE_PATH = os.path.join(USER_PATH, "preview-cache")
TITLE_PATH = os.path.join(USER_PATH, "title")
PROFILES_PATH = os.path.join(PATH, "profiles")
IMAGES_PATH = os.path.join(PATH, "images")
TRANSITIONS_PATH = os.path.join(USER_PATH, "transitions")
EXPORT_PRESETS_PATH = os.path.join(PATH, "presets")
EXPORT_TESTS = os.path.join(USER_PATH, "tests")
USER_PROFILES_PATH = os.path.join(USER_PATH, "profiles")
USER_PRESETS_PATH = os.path.join(USER_PATH, "presets")

# Create PATHS if they do not exist (this is where temp files are stored... such as cached thumbnails)
for folder in [USER_PATH, THUMBNAIL_PATH, CACHE_PATH, BLENDER_PATH, ASSETS_PATH, TITLE_PATH, PROFILES_PATH, IMAGES_PATH,
               TRANSITIONS_PATH, EXPORT_TESTS, BACKUP_PATH, USER_PROFILES_PATH, USER_PRESETS_PATH, PREVIEW_CACHE_PATH]:
    if not os.path.exists(folder.encode("UTF-8")):
        os.makedirs(folder, exist_ok=True)

# names of all contributors, using "u" for unicode encoding
JT = {"name": u"D V", "email": "hello@editxpro.com", "website":"http://editxpro.org/"}

# Languages
CMDLINE_LANGUAGE = None
CURRENT_LANGUAGE = 'en_US'
SUPPORTED_LANGUAGES = ['en_US']

try:
    from language import openshot_lang
    language_path=":/locale/"
except ImportError:
    language_path=os.path.join(PATH, 'language')
    print("Compiled translation resources missing!")
    print("Loading translations from: {}".format(language_path))

# Compile language list from :/locale resource
langdir = QDir(language_path)
langs = langdir.entryList(['OpenShot.*.qm'], QDir.NoDotAndDotDot|QDir.Files,
                          sort=QDir.Name)
for trpath in langs:
    SUPPORTED_LANGUAGES.append(trpath.split('.')[1])

SETUP = {
    "name": NAME,
    "version": VERSION,
    "author": JT["name"] + " and others",
    "author_email": JT["email"],
    "maintainer": JT["name"],
    "maintainer_email": JT["email"],
    "url": "http://www.editxpr.com/",
    "license": "GNU GPL v." + GPL_VERSION,
    "description": DESCRIPTION,
    "long_description": "Create and edit videos and movies\n"
                        " Edit X Pro is a non-linear video editor. It\n"
                        " can create and edit videos and movies using many popular video, audio, \n"
                        " image formats.  This is specially designed for wedding video. It can be exported for\n"
                        " DVD, TV, Youtube, Xbox, and many more common formats!\n"
                        ".\n"
                        " Features include:\n"
                        "  * Unlimited tracks Sequencer\n"
                        "  * Video Compositing, image overlays, and watermarks\n"
                        "  * Creating image sequences (rotoscoping)\n"
                        "  * Key-frame animation\n  * Video and audio effects (chroma-key)\n"
                        "  * Transitions (lumas and masks)\n"
                        "  * 3D animation (titles and simulations)\n"
                        "  * Upload videos (YouTube and Vimeo supported)",

    # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "classifiers": [
                       "Development Status :: 5 - Production/Stable",
                       "Environment :: X11 Applications",
                       "Environment :: X11 Applications :: GTK",
                       "Intended Audience :: End Users/Desktop",
                       "License :: OSI Approved :: GNU General Public License (GPL)",
                       "Operating System :: OS Independent",
                       "Operating System :: POSIX :: Linux",
                       "Programming Language :: Python",
                       "Topic :: Artistic Software",
                       "Topic :: Multimedia :: Video :: Non-Linear Editor", ] +
                   ["Natural Language :: " + language for language in SUPPORTED_LANGUAGES],

    # Automatic launch script creation
    "entry_points": {
        "gui_scripts": [
            "openshot-qt = openshot_qt.launch:main"
        ]
    }
}

def website_language():
    """Get the current website language code for URLs"""
    if CURRENT_LANGUAGE == "zh_CN":
        return "zh-hans/"
    elif CURRENT_LANGUAGE == "zh_TW":
        return "zh-hant/"
    elif CURRENT_LANGUAGE == "en_US":
        return ""
    else:
        return "%s/" % CURRENT_LANGUAGE.split("_")[0].lower()
