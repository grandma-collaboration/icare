import requests
import tornado.escape
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.ioloop import IOLoop

from baselayer.app.models import init_db
from baselayer.app.access import auth_or_token
from baselayer.app.env import load_env
from baselayer.log import make_log
from baselayer.app.handlers.base import BaseHandler

from skyportal.utils.services import check_loaded

env, cfg = load_env()
log = make_log("tarot_proxy")

TAROT_BASE_URL = cfg.get("app.tarot_endpoint")
TAROT_CALERN_URL = cfg.get("app.calern_endpoint")
TAROT_CHILI_URL = cfg.get("app.chili_endpoint")
TAROT_REUNION_URL = cfg.get("app.reunion_endpoint")
PORT = cfg.get("ports.tarot_proxy")

is_configured = TAROT_BASE_URL and TAROT_CALERN_URL and TAROT_CHILI_URL and TAROT_REUNION_URL and PORT

init_db(**cfg["database"])

Session = scoped_session(sessionmaker())


class TarotProxyHandler(BaseHandler):
    def prepare(self):
        path = self.request.path

        if path.startswith("/tarot_calern"):
            base_url = TAROT_CALERN_URL
            specific_path = path.replace("/tarot_calern", "")
        elif path.startswith("/tarot_chili"):
            base_url = TAROT_CHILI_URL
            specific_path = path.replace("/tarot_chili", "")
        elif path.startswith("/tarot_reunion"):
            base_url = TAROT_REUNION_URL
            specific_path = path.replace("/tarot_reunion", "")
        else:
            base_url = TAROT_BASE_URL
            specific_path = path

        self.tarot_url = f"{base_url}{specific_path}"

    def forward_request(self):
        method = self.request.method

        browser_username = self.request.headers.get("X-Browser-Username")
        browser_password = self.request.headers.get("X-Browser-Password")

        # Exclude icare, browser authentication and host header to use the real target host,
        exclude = {"authorization", "x-browser-username", "x-browser-password", "host"}
        headers = {k: v for k, v in self.request.headers.items() if k.lower() not in exclude}

        query = self.request.query
        full_url = f"{self.tarot_url}?{query}" if query else self.tarot_url
        resp = requests.request(
            method,
            full_url,
            headers=headers,
            auth=(browser_username, browser_password),
            data=self.request.body,
            allow_redirects=True,
            timeout=5,
        )
        self.set_status(resp.status_code)
        for key, value in resp.headers.items():
            # Exclude headers that should not be set in the response
            if key.lower() not in {"content-length", "transfer-encoding", "connection"}:
                self.set_header(key, value)
        self.finish(resp.content)

    @auth_or_token
    def get(self):
        self.forward_request()

    @auth_or_token
    def post(self):
        self.forward_request()

    @auth_or_token
    def delete(self):
        self.forward_request()


@check_loaded(logger=log)
def service(*args, **kwargs):
    """Start the Tarot proxy service."""
    app = tornado.web.Application([(r"/.*", TarotProxyHandler)])
    app.listen(PORT)
    log(f"TAROT proxy listening on port {PORT}")
    IOLoop.current().start()


if __name__ == "__main__":
    """Start the Tarot proxy server"""
    if not is_configured:
        raise ValueError("tarot_endpoint, calern_endpoint, chili_endpoint, reunion_endpoint and ports.tarot_proxy must be set in the configuration.")
    try:
        service()
    except Exception as e:
        log(f"Error occurred while starting TAROT proxy: {str(e)}")
        raise e
