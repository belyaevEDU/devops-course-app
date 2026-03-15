import requests
from . import parser
from .cached_session import get_daily

BASE_URL = "http://www.cbr.ru/scripts/XML_daily.asp"
RESPONSE_EXPECTED_ENCODING = "windows-1251"

def get_bank_api_response(currency = "", date = "") -> dict[str, float]:
    """
    This function expects already validated query parameters, if they're being passed.
    The date format expected is yyyy-mm-dd. The currency format expected is ISO4217 in any case (upper/lower/mixed).
    May raise HTTPError or ValueError.
    """
    requestUrl = BASE_URL
    if date != "":
        requestUrl += "?date_req="

        dateSplit = date.split("-") # expected format is yyyy-mm-dd
        # Date format for the API is dd/mm/yyyy
        dateRearranged = dateSplit[2] + '/' + dateSplit[1] + '/' + dateSplit[0]

        requestUrl += dateRearranged

        response = requests.get(requestUrl)
    else:
        response = get_daily(requestUrl)

    response.encoding = RESPONSE_EXPECTED_ENCODING
    if response.status_code != 200:
        response.raise_for_status()

    if currency == "":
        return parser.get_all_currency_rates(response.text)
    else:
        return parser.get_select_currency_rate(response.text, currency)