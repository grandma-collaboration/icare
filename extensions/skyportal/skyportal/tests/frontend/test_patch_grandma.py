from skyportal.tests import api
from selenium.webdriver.common.keys import Keys
from datetime import date, timedelta
import uuid


def test_patch_icare(super_admin_user, driver):

    driver.get(f"/become_user/{super_admin_user.id}")
    driver.get("/")
    driver.wait_for_xpath(f'//*[contains(.,"Icare")]', timeout=20)
