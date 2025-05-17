import curl_cffi

class Session:
    def __init__(self, impersonate: str = "chrome136"):
        self._session = curl_cffi.Session(impersonate=impersonate)
        self._has_sent_request = False
        self._last_response = None

    def get(self, url: str, **kwargs):
        response = self._session.get(url, **kwargs)
        self._record_response(response)
        return response

    def post(self, url: str, data=None, json=None, **kwargs):
        response = self._session.post(url, data=data, json=json, **kwargs)
        self._record_response(response)
        return response

    def _record_response(self, response):
        self._has_sent_request = True
        self._last_response = response

    def _ensure_response(self):
        if not self._has_sent_request or self._last_response is None:
            raise RuntimeError("You must send at least one request before accessing this property.")

    @property
    def proxies(self):
        return self._session.proxies

    @proxies.setter
    def proxies(self, value):
        self._session.proxies = value

    @property
    def timeout(self):
        return self._session.timeout

    @timeout.setter
    def timeout(self, value):
        self._session.timeout = value

    @property
    def auth(self):
        return self._session.auth

    @auth.setter
    def auth(self, value):
        self._session.auth = value

    @property
    def verify(self):
        return self._session.verify

    @verify.setter
    def verify(self, value):
        self._session.verify = value

    @property
    def last_response(self):
        self._ensure_response()
        return self._last_response

    @property
    def cookies(self):
        return self.last_response.cookies

    @property
    def request(self):
        return self.last_response.request

    @property
    def url(self):
        return self.last_response.url

    @property
    def content(self):
        return self.last_response.content

    @property
    def status_code(self):
        return self.last_response.status_code

    @property
    def ok(self):
        return self.last_response.ok

    @property
    def response_headers(self):
        return self.last_response.headers

    @property
    def history(self):
        return self.last_response.history

    @property
    def elapsed(self):
        return self.last_response.elapsed

    @property
    def encoding(self):
        return self.last_response.encoding

    @property
    def redirect_count(self):
        return len(self.history)

    @property
    def http_version(self):
        return self.last_response.http_version

    @property
    def curl(self):
        return self.last_response.curl

    @property
    def primary_ip(self):
        return self.last_response.primary_ip

    @property
    def primary_port(self):
        return self.last_response.primary_port

    @property
    def local_ip(self):
        return self.last_response.local_ip

    @property
    def local_port(self):
        return self.last_response.local_port

    @property
    def infos(self):
        return self.last_response.infos
