from selenium.webdriver import Chrome, Firefox
from config import CHROME_DRIVER_LOCATION, FIREFOX_DRIVER_LOCATION

NVIDIA_GTC_URL = "https://www.nvidia.com/en-us/gtc/session-catalog/?search.language=1594320459782001LCjF&search=&tab.day=20201007"

# driver = Chrome(CHROME_DRIVER_LOCATION)


# driver.get(NVIDIA_GTC_URL)
# driver.find_element_by_id("rf-").click()


driver = Firefox(FIREFOX_DRIVER_LOCATION)


driver.get(NVIDIA_GTC_URL)
driver.find_element_by_id("rf-").click()