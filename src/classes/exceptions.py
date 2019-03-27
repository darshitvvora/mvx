""" 
 @file
 @brief This file deals with unhandled exceptions

 """

import traceback
from classes.logger import log
from classes.metrics import track_exception_stacktrace


def ExceptionHandler(exeception_type, exeception_value, exeception_traceback):
    """Callback for any unhandled exceptions"""
    log.error('Unhandled Exception', exc_info=(exeception_type, exeception_value, exeception_traceback))

    # Build string of stack trace
    stacktrace = "Python %s" % "".join(traceback.format_exception(exeception_type, exeception_value, exeception_traceback))

    # Report traceback to webservice (if enabled)
    track_exception_stacktrace(stacktrace, "openshot-qt")
