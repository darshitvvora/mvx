"""
 @file
 @brief This file get the current version of and license validity

 """

import requests
import sys
import uuid
import threading
import datetime
from datetime import date
from classes.app import get_app
from classes import info
from classes.logger import log
from classes import  settings
try:
    import json
except ImportError:
    import simplejson as json


def get_current_Version():
    """Get the current version """
    t = threading.Thread(target=get_version_from_http)
    t.start()

def get_current_Activation():
    """Get the current activation """
    t = threading.Thread(target=get_activation_from_http)
    t.start()

def set_current_Activation():
    """Get the current activation """
    t = threading.Thread(target=register_new_user_from_http)
    t.start()


def get_version_from_http():
    """Get the current version # from openshot.org"""

    url = "http://www.openshot.org/version/json/"

    # Send metric HTTP data
    try:
        r = requests.get(url, headers={"user-agent": "openshot-qt-%s" % info.VERSION}, verify=False)
        log.info("Found current version: %s" % r.text)

        # Parse version
        # openshot_version = r.json()["openshot_version"]
        openshot_version = "2.4.3"

        # Emit signal for the UI
        get_app().window.FoundVersionSignal.emit(openshot_version)

    except Exception as Ex:
        log.error("Failed to get version from: %s" % url)

def get_activation_from_http():
    """Get the current version # from openshot.org"""

    url = "https://api.backendless.com/7585ECA1-8714-3061-FFAB-5ECD6D8E8000/4F4067A2-24E1-5EC2-FF3C-F1BA2AA1D900/users/login"

    # Send metric HTTP data
    try:

        s = settings.get_settings()
        email = s.get("activation_email")
        password = hex(uuid.getnode())
        payload = {"login": email, "password": password}
        log.info("email: %s" % email)
        log.info("password: %s" % password)

        r = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, verify=False)

        # Parse version
        status_code = r.status_code
        account_activation = False
        if status_code == 200:
            account_activation = r.json()["account_activated"]
            validity = r.json()["validity"]
            now = datetime.datetime.now()
            valid_date = datetime.datetime.fromtimestamp(validity/1000)          
            
            if valid_date < now:
                log.info("Validity Expired. Please contact developers")
                account_activation=False


        log.info("Login Details: %s" %r.json())   

        #openshot_version = "2.4.3"

        # Emit signal for the UI
        get_app().window.FoundActivationSignal.emit(account_activation)

    except Exception as Ex:
        log.error("Failed to get activation from: %s" % Ex)

def register_new_user_from_http():
    """Get the current version # from openshot.org"""

    url =  "http://api.backendless.com/7585ECA1-8714-3061-FFAB-5ECD6D8E8000/4F4067A2-24E1-5EC2-FF3C-F1BA2AA1D900/data/Users"
    # Send metric HTTP data
    try:

        s = settings.get_settings()
        email = s.get("activation_email")
        password = hex(uuid.getnode())

        payload = {"email": email, "password": password, "account_activated": False, "name": email}
        log.info("%s", payload)

        r = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

        status_code = r.status_code
        account_activation = False
        if status_code == 200:
            account_activation = r.json()["account_activated"]

        #log.info("Login Details: %s" % r.json())       


        # Emit signal for the UI
        get_app().window.FoundSetActivationSignal.emit(account_activation)

    except Exception as Ex:
        log.error("Failed to set activation from: %s" % Ex)
