import socket
import logging
import requests
from selenium.webdriver.common.action_chains import ActionChains

def click_element_js(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        ActionChains(driver).move_to_element(element).perform()
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        logging.warning(f"Error clicking on element: {str(e)}")

def get_ip_address(url):
    try:
        hostname = requests.utils.urlparse(url).hostname
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return None
