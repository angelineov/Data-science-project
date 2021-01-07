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
driver.get("https://www.dwexperience.com/agenda/")
print(driver.title)

try:
    main_content = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tabr-cont"))
    ) 
    descriptions = main_content.find_elements_by_class_name("expandable")
    titles = main_content.find_elements_by_class_name("heading-day")
    speaker_companies = main_content.find_elements_by_class_name("day-contact")
    speaker_companies2 = main_content.find_elements_by_class_name("day-contacts")
    titles1 = []
    description1 = []
    speaker_companies1 = []
    for title in titles:
            t = title
            t1 = t.text
            titles1.append(t1)
    #print('1')
    for description in descriptions:
            content = description.find_element_by_tag_name('p').text
            description1.append(content)
    #print('2')
    #temp = []
    #for speaker_company in speaker_companies:
    #        s = speaker_company.find_element_by_tag_name('p').text
    #        temp.append(s)  
            #speaker_companies1.append(s)     
            #print(speaker_company)
    #speaker_companies1 = ",".join(temp)
    #print(len(speaker_companies1))
    #df = pd.DataFrame({'title': titles1, 'description': description1})
    #print(df)
    #df1 = pd.DataFrame({'c': speaker_companies1})
    #print(df1)
    df2 = pd.DataFrame({'title': titles1, 'description': description1})
    #print(df2)
    
    
    root= tk.Tk()
    canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
    canvas1.pack()
    def exportCSV ():
        global df2
        export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
        df2.to_csv (export_file_path, index = False, header=True)
    saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 150, window=saveAsButton_CSV)
    root.mainloop()
except:
    driver.quit()
