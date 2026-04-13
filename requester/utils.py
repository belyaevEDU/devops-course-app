import defusedxml.ElementTree as ET
from datetime import date, datetime

PARAMETER_ERROR_MESSAGE = "Error in parameters"

def check_for_error_in_response(root: ET):
    """
    If the date is long in the past, the central bank's API returns a single ValCurs element with the text 'Error in parameters'.
    This function checks for that response.
    """
    if root is not None:
        if root.text == PARAMETER_ERROR_MESSAGE:
            raise ValueError(PARAMETER_ERROR_MESSAGE)

def get_todays_datetime_object() -> datetime:
    """Returns a datetime object with today's date with 0 hours, 0 minutes and 0 seconds"""
    return datetime.combine(date.today(), datetime.min.time())