from contextlib import contextmanager
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import onu


TIMEOUT = 30  # seconds

class FirewallLevel(Enum):
    high = 3
    # medium = 2
    low = 1
    off = 0
    loading = -1


def logout(driver):
    logout_link = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'LogOffLnk'))
    )
    logout_link.click()


@contextmanager
def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('prefs', {
        "profile.default_content_settings": {
            "images": 2,
            "javascript": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "midi_sysex": 2,
            "background_sync": 2,
            "bluetooth": 2,
            "camera": 2,
            "microphone": 2,
            "payment_handler": 2,
            "usb": 2
        },
    })
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    try:
        yield driver
        logout(driver)
    finally:
        driver.quit()


def goto_firewall_settings(driver):
    driver.get(f"http://{onu.host}/")

    username_input = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "Frm_Username"))
    )
    password_input = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "Frm_Password"))
    )
    login_button = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'LoginId'))
    )

    username_input.send_keys(onu.username)
    password_input.send_keys(onu.password)
    login_button.click()

    internet_tab = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'internet'))
    )
    internet_tab.click()

    security_menu = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'securityv2'))
    )
    security_menu.click()


def retrieve_firewall_levels(driver) -> FirewallLevel | None:
    selected_option = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="radio"][name="Level"]:checked'))
    )

    value = selected_option.get_attribute("value")
    return FirewallLevel(int(value)) if value else None


def get_current_firewall_level() -> FirewallLevel | None:
    with create_driver() as driver:
        goto_firewall_settings(driver)
        return retrieve_firewall_levels(driver)


def set_firewall_level(level: FirewallLevel) -> FirewallLevel | None:
    with create_driver() as driver:
        goto_firewall_settings(driver)

        option = WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, f'Level{level.value}'))
        )
        option.click()

        apply_button = WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, 'Btn_apply_FirewallConf'))
        )
        apply_button.click()

        return retrieve_firewall_levels(driver)
