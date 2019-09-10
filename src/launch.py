#!/usr/bin/env python3

""" 
 @file
 @brief This file is used to launch EditX Pro

 @mainpage EditX Pro
 

 """

import sys
from argparse import ArgumentParser, REMAINDER

try:
    from classes import info
    print("Loaded modules from current directory: %s" % info.PATH)
except ImportError:
    import openshot_qt
    sys.path.append(openshot_qt.OPENSHOT_PATH)
    from classes import info
    print("Loaded modules from installed directory: %s" % info.PATH)

from classes.app import OpenShotApp
from classes.logger import log, reroute_output
from classes.language import get_all_languages


def main():
    """"Initialize settings (not implemented) and create main window/application."""

    parser = ArgumentParser(description = 'Edit X Pro version ' + info.SETUP['version'])
    parser.add_argument('-l', '--lang', action='store',
                        help='language code for interface (overrides '
                        'preferences and system environment)')
    parser.add_argument('--list-languages', dest='list_languages',
                        action='store_true', help='List all language '
                        'codes supported by Edit X Pro')
    parser.add_argument('-V', '--version', action='store_true')
    parser.add_argument('remain', nargs=REMAINDER)

    args = parser.parse_args()

    # Display version and exit (if requested)
    if args.version:
        print("MagicVideoXPro version %s" % info.SETUP['version'])
        sys.exit()

    if args.list_languages:
        print("Supported Languages:")
        for lang in get_all_languages():
            print("  {:>12}  {}".format(lang[0],lang[1]))
        sys.exit()

    if args.lang:
        if args.lang in info.SUPPORTED_LANGUAGES:
            info.CMDLINE_LANGUAGE = args.lang
        else:
            print("Unsupported language '{}'! (See --list-languages)".format(args.lang))
            sys.exit(-1)

    reroute_output()

    log.info("------------------------------------------------")
    log.info("   Edit X Pro (version %s)" % info.SETUP['version'])
    log.info("------------------------------------------------")

    # Create Qt application, pass any unprocessed arguments
    argv = [sys.argv[0]]
    for arg in args.remain:
        argv.append(arg)
    app = OpenShotApp(argv)

    # Run and return result
    sys.exit(app.run())


if __name__ == "__main__":
    main()
