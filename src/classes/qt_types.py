""" 
 @file
 @brief This file contains helper functions for Qt types (string to base64)

 """

from PyQt5.QtCore import QByteArray


# Utility functions for handling qt types

# QByteArray helpers
def str_to_bytes(string):
    """ This is required to save Qt byte arrays into a base64 string (to save screen preferences) """
    return QByteArray.fromBase64(string.encode("utf-8"))


def bytes_to_str(bytes):
    """ This is required to load base64 Qt byte array strings into a Qt byte array (to load screen preferences) """
    return bytes.toBase64().data().decode("utf-8")
