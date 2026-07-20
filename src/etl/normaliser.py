def normalize_year(year):
    """
    Convert year to integer.
    Returns None if the year is invalid.
    """
    try:
        return int(year)
    except (ValueError, TypeError):
        return None


def normalize_ticker(ticker):
    """
    Convert ticker to uppercase and remove extra spaces.
    """
    if ticker is None:
        return None

    return str(ticker).strip().upper()