import atexit
from requests_cache import CachedSession, Response
from datetime import timedelta
from .utils import get_todays_datetime_object

CACHE_FILE_PATH = "requester/cache/http_cache"

def create_daily_session():
    """
    Uses CachedSession from the requests_cache module to cache HTTP responses.
    This creates and manages a CachedSession object, that has the expiration date set to the next day.
    If it is used past the expiration date, it just clears out it's cache, closes and remakes itself.
    Only used for the query of today's exchange rate from the CBRF API.
    """
    session = None
    expiration = None

    def create_session():
        nonlocal session, expiration # i <3 functional
        expiration = get_todays_datetime_object() + timedelta(days=1)
        session = CachedSession(CACHE_FILE_PATH, backend='sqlite', expire_after=expiration)

    def get(path) -> Response:
        nonlocal session, expiration

        if session is None:
            create_session()
        elif get_todays_datetime_object() >= expiration:
            session.cache.clear()
            session.close()
            create_session()

        return session.get(path)

    def cleanup():
        if session is not None:
            session.close()

    atexit.register(cleanup) # auto closing the session on program exit

    return get

get_daily = create_daily_session()