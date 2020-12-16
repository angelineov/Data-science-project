from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import time
import tkinter as tk
from tkinter import filedialog
from pandas import DataFrame

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
#EVERYTHING
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593594815")

#AEROSPACE
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=option_1559593140683")
#ARCHITECTURE
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=option_1559593165314")
#AUTOMOTIVE
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=option_1559593175456")
#CLOUD SERVICES
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=option_1559593181471")
#FINANCE
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=option_1559593199335")
#HEALTHCARE
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=option_1559593230294")
#HIGHER EDUCATION
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=option_1559593237735")
#MEDIA 
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=option_1559593250529")
#NATIONAL LABS
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=1565284091917001Mueq")
#SOFTWARE
#driver.get("https://www.nvidia.com/en-us/gtc/session-catalog-details/?search.sessiontype=option_1559593597329&search.sessiontype=option_1559593594815&search.industrysegment=option_1559593257519")




print(driver.title)

try:
    main_content = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
    ) 
    
    descriptions = main_content.find_elements_by_class_name("description")
    titles = main_content.find_elements_by_class_name("title-text")
    speaker_companies = main_content.find_elements_by_class_name("speaker-details")
    topics = main_content.find_elements_by_class_name("attribute-values")
    industries = main_content.find_elements_by_class_name("attribute-IndustrySegment")
    titles1 = []
    description1 = []
    speaker_companies1 = []
    industry1 = []
    for title in titles:
            t = title.text
            titles1.append(t)
    for description in descriptions:
            content = description.find_element_by_tag_name('p')
            d = content.find_element_by_tag_name('span').text
            description1.append(d)
    for speaker_company in speaker_companies:
            s = speaker_company.find_element_by_tag_name('p').text  
            speaker_companies1.append(s)     
    for industry in industries:
            i = industry.find_element_by_class_name("attribute-values").text   
            industry1.append(i)    
    #df = pd.DataFrame({'title': t, 'description': d, 'company': s,'industry': i})
    df = pd.DataFrame({'title': titles1, 'description': description1, 'company': speaker_companies1, 'industry': industry1})
    print(df)
    root= tk.Tk()
    canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
    canvas1.pack()
    def exportCSV ():
        global df
        export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
        df.to_csv (export_file_path, index = False, header=True)
    saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 150, window=saveAsButton_CSV)
    root.mainloop()
except:
    driver.quit()
