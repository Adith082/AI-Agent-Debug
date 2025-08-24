import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def session_with_retries(timeout=5):
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    s.request = _wrap_with_timeout(s.request, timeout)
    return s

def _wrap_with_timeout(fn, timeout):
    def _f(method, url, **kwargs):
        kwargs.setdefault("timeout", timeout)
        return fn(method, url, **kwargs)
    return _f