import calendar
import time
import logging
from dateutil import parser
from fast_api_als.database.db_helper import db_helper_session

from fast_api_als import constants

"""
what exceptions can be thrown here?
"""

def get_enriched_lead_json(adf_json: dict) -> dict:
    try:
        pass
    except IOError:
        print("Invalid Json or empty file")
    except RuntimeError:
        print("Unexpected Error")
    except ValueError:
        print("Decoding Json Failed")
    except PermissionError:
        print("permission denied")