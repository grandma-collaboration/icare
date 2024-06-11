import asyncio
import concurrent

from skyportal.app_server import make_app

from skyportal.handlers.api.fink_photometry import FinkPhotometryHandler

print("Loading Icare-specific handlers...")


icare_handlers = [
    (r'/api/sources(/[0-9A-Za-z-_\.\+]+)/fink', FinkPhotometryHandler),
]

def make_app_icare(cfg, baselayer_handlers, baselayer_settings, process=None, env=None):
    """Create and return a `tornado.web.Application` object with (Icare-specific) specified
    handlers and settings.

    Parameters
    ----------
    cfg : Config
        Loaded configuration.  Can be specified with '--config'
        (multiple uses allowed).
    baselayer_handlers : list
        Tornado handlers needed for baselayer to function.
    baselayer_settings : cfg
        Settings needed for baselayer to function.

    """
    app = make_app(cfg, baselayer_handlers, baselayer_settings, process, env)

    # Limit the number of threads on each Tornado instance.
    # This is to ensure that we don't run out of database connections,
    # or overload our SQLAlchemy connection pool.
    asyncio.get_event_loop().set_default_executor(
        concurrent.futures.ThreadPoolExecutor(max_workers=8)
    )

    app.add_handlers(r".*", icare_handlers)  # match any host
    print("Icare-specific handlers loaded.")

    return app
