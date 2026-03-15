import iso4217
from datetime import date

CURRENCY_NAMES = [str(x).lower() for x in iso4217.raw_table.keys()]

def validate_currency_name(currencyName: str) -> bool:
    """Validates a currency name to iso4217 standards, supports all cases (lower/upper/mixed)"""
    return currencyName.lower() in CURRENCY_NAMES

def validate_date(dateString: str) -> bool:
    """Expected date format is yyyy-mm-dd (ISO 8601). Also checks if the date is not in the future."""
    try:
        date.fromisoformat(dateString)

        dateSplit = [int(x) for x in dateString.split('-')]
        dateConverted = date(dateSplit[0], dateSplit[1], dateSplit[2])
        return dateConverted <= date.today()
    except ValueError:
        return False