"""icare-specific frontend test configuration.

icare authenticates via an IAM OAuth2 provider, whereas skyportal's default
Playwright login helper (skyportal/tests/test_util.py:playwright_login) clicks
the ``/login/google-oauth2`` link. Rather than fork the whole ``test_util`` /
session ``page`` fixture, we override just the login: the fixture calls
``playwright_login`` by name on the test_util module, so reassigning that
module attribute here (at conftest import, before the session ``page`` fixture
is first instantiated) is enough.
"""

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect
from skyportal.tests import test_util


def _icare_playwright_login(page):
    """Log in the shared page via icare's IAM OAuth2 debug-login flow."""
    page.goto("/")
    # Already logged in?
    if page.locator(test_util.TESTUSER_XPATH).first.is_visible():
        return
    login_link = page.locator('//a[contains(@href,"/login/iam-oauth2")]').first
    try:
        login_link.wait_for(state="visible", timeout=20_000)
        login_link.click()
    except PlaywrightTimeoutError:
        pass  # no login link -> assume already authenticated
    # Dismiss the Terms of Service dialog if it appears after login
    tos_agree = page.locator('button:has-text("I Agree")').first
    try:
        tos_agree.wait_for(state="visible", timeout=10_000)
        tos_agree.click()
    except PlaywrightTimeoutError:
        pass
    expect(page.locator(test_util.TESTUSER_XPATH).first).to_be_visible(timeout=20_000)


test_util.playwright_login = _icare_playwright_login
