import http.client as httplib

import pytest


def is_internet_available(host="8.8.8.8", timeout=2) -> bool:
    """Check if the internet is available by pinging a given host.

    Parameters
    ----------
    host : str
        The host to ping, default is Google's primary DNS.
    timeout : int
        Timeout for each ping in seconds.

    Returns
    -------
    True if the internet is available, False otherwise.
    """
    conn = httplib.HTTPSConnection(host, timeout=timeout)

    try:
        conn.request("HEAD", "/")
    except Exception:
        return False
    else:
        return True
    finally:
        conn.close()


@pytest.mark.integration
def test_internet_connection():
    assert is_internet_available(), "Internet connection test failed."
