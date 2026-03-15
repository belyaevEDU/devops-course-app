import xml.etree.ElementTree as ET
from . import utils

def get_select_currency_rate(response: str, userCurrency: str) -> dict[str, float]:
    """
    Helper function for getting select currency rates from the central bank's API response.
    Returns a dictionary with one item: uppercase currency name as key and the rate as value.
    May raise ValueError.
    """
    userCurrency = userCurrency.lower()

    allCurrencies = get_currency_list(response)
    for currency in allCurrencies:
        if currency.find('CharCode').text.lower() == userCurrency:
            valueString = currency.find('Value').text
            return {userCurrency.upper(): float(valueString.replace(',', '.'))}

    # Sticking with ValueError for this one, even though the float conversion can also raise the same thing
    # just because the theoretical issue is of the same root.
    raise ValueError("Currency not found")

def get_all_currency_rates(response: str) -> dict[str, float]:
    """
    Helper function for getting all currency rates from the central bank's API response.
    Returns a dictionary with uppercase currency names as keys and the rates as values.
    May raise ValueError.
    """
    result = {}

    allCurrencies = get_currency_list(response)
    for currency in allCurrencies:
        valueString = currency.find('Value').text
        result[currency.find('CharCode').text] = float(valueString.replace(',', '.'))

    if not result:
        raise ValueError("Empty data (bad query parameters?)")

    return result

def get_currency_list(response: str) -> list:
    """
    Helper function for getting the currency rates list out of the central bank's API response.
    May raise ValueError.
    """
    root = ET.fromstring(response)

    utils.check_for_error_in_response(root)

    return root.findall("Valute")