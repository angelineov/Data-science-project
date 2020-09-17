from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import time
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/")
print(driver.title)



try:
    main_content = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
    ) 
    #blocks = main_content.find_elements_by_class_name("catalog-result session-result show-session-title-icon")
    print(main_content.text)
    #for block in blocks:
        #attributes = blocks.find_elements_by_class_name("rf-attribute")
        #print(attributes.text)
        #for attribute in attributes:
        #    description = attributes.find_element_by_class_name("description")
        #    print(description.text)
except:
    driver.quit()
