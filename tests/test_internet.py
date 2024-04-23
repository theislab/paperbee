import pytest
import http.client as httplib

def is_internet_available(host="8.8.8.8", count=4, timeout=2) -> bool:
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
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=timeout)
    
    try:
        conn.request("HEAD", "/")
        return True
    
    except Exception:
        return False
    
    finally:
        conn.close()

@pytest.mark.integration
def test_internet_connection():
    assert is_internet_available(), "Internet connection test failed."
