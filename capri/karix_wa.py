from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
import datetime
import xlrd
import pickle
import os.path
from googleapiclient import discovery
from httplib2 import Http
import pandas as pd
import numpy as np
import datetime as dt
import requests
import shutil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import zipfile 
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\gurpreet.padam\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Update path as needed

# import tesseract
# Configure the Selenium webdriver

import time

yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d')

today = (datetime.date.today()).strftime('%d')
os.environ['WDM_SSL_VERIFY'] = '0'


opt = Options()
# opt.add_argument('--headless')
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,  # Disable notifications
    "download.default_directory": r"C:\Users\gurpreet.padam\Capri\Collections\Selenium\CommunicationsReports\WA\karix_wa",  # Set download path
    "directory_upgrade": True
    # "download.prompt_for_download": False,  # Disable download prompt
    # "plugins.always_open_pdf_externally": True  # Open PDFs directly without download prompt
})


opt.add_argument('--disable-gpu')
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
opt.add_experimental_option('useAutomationExtension', False)
# Configure Chrome options.
# opts = Options()

# Configure ChromeDriver service.
service = Service(ChromeDriverManager().install())

# Start the Chrome driver with the configured options and service.
driver = webdriver.Chrome(service=service, options=opt)

driver.get("https://managebot.karix.solutions/bot_builder_gui/#/login")
time.sleep(10)
username = driver.find_element(By.ID, "entrp-username")
username.send_keys("prpcapri")
password = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
password.send_keys("Capri@0987")
login = driver.find_element(By.XPATH, "//button[@type='submit']")
login.click()
time.sleep(12)


report_page = driver.find_element(By.XPATH, "//a[span[text()='Reports Insights']]")
report_page.click()

time.sleep(5)


window_handles = driver.window_handles
time.sleep(30)
driver.switch_to.window(window_handles[-1])
cam_rep = driver.find_element(By.XPATH, "//a[span[text()='Campaign Reports']]")
cam_rep.click()

date_time = driver.find_element(By.XPATH, "//li[input[@startkey='start' and @endkey='end']]")
date_time.click()
time.sleep(2)

month = 'Old'
while month != 'Current':
    try:
        driver.find_element(By.XPATH,"//div[contains(@class, 'calendar left')]//th[contains(@class,'next available')]").click()
    except:
        # print('prevoise date error or nor avail')
        month = 'Current'

date_list = driver.find_elements(By.XPATH, "//div[contains(@class,'calendar left')]//td[contains(@class, 'available')]")
# Iterate through the cells to find the one containing the correct <span> text
for date in date_list:
    # Check if the <span> inside the <td> matches the expected text
    span = date.find_element(By.XPATH, ".//span")  # Locate the <span> inside the <td>
    if span.text == yesterday:
        # Click the <td> element
        date.click()
        print(f"Clicked on the date: {yesterday}")
        break
else:
    print(f"No cell found with the date: {yesterday}")



month = 'Old'
while month != 'Current':
    try:
        driver.find_element(By.XPATH,"//div[contains(@class, 'calendar left')]//th[contains(@class,'next available')]").click()
    except:
        month = 'Current'
date_list = driver.find_elements(By.XPATH, "//div[contains(@class, 'calendar left')]//td[contains(@class, 'available')]")

# Iterate through the cells to find the one containing the correct <span> text
for date in date_list:
    # Check if the <span> inside the <td> matches the expected text
    span = date.find_element(By.XPATH, ".//span")  # Locate the <span> inside the <td>
    if span.text == yesterday:
        # Click the <td> element
        date.click()
        print(f"Clicked on the date: {yesterday}")
        break
else:
    print(f"No cell found with the date: {yesterday}")


time.sleep(2)

driver.find_element(By.XPATH, "//button[@class='btn' and text() = 'ok']").click()
print('click ok')

driver.find_element(By.XPATH,"//option[text()=' PRPcapri ']").click()
print('click PRP capri from dropdown')


driver.find_element(By.XPATH,"//option[text()=' 918451021021 ']").click()
print('click waba number')


print('click on go')
driver.find_element(By.XPATH, "//button[@class='btn mr-3'  and text() = ' Go ']").click()

time.sleep(5)




total_elements = driver.find_elements(By.XPATH, "//div[@class='row template-det1']")
print(total_elements)
print(len(total_elements))




if (len(total_elements)>0):
    for i in range(len(total_elements)):
        desired_y = (total_elements[i].size['height'] / 2) + total_elements[i].location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        time.sleep(1)
        total_elements[i].click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollTop);")
        time.sleep(1)
        driver.find_element(By.XPATH, "//i[@class='fa fa-2x fa-download']").click()
        time.sleep(3)
        print(i)
        
    
    time.sleep(10)
    
    
    driver.find_element(By.XPATH, "//a[contains(@href, '#/downloadcenter?activeTab=campaign') and .//b[text()='Download Center']]").click()
    
    date_time = driver.find_element(By.XPATH, "//div[input[@startkey='start' and @endkey='end']]")
    date_time.click()
    
    
    time.sleep(8)
    month = 'Old'
    while month != 'Current':
        try:
            driver.find_element(By.XPATH,"//div[contains(@class, 'calendar left')]//th[contains(@class,'next available')]").click()
        except:
            month = 'Current'
    
    
    date_list = driver.find_elements(By.XPATH, "//div[contains(@class,'calendar left')]//td[contains(@class, 'available')]")
    
    # Iterate through the cells to find the one containing the correct <span> text
    for date in date_list:
        # Check if the <span> inside the <td> matches the expected text
        span = date.find_element(By.XPATH, ".//span")  # Locate the <span> inside the <td>
        if span.text == today:
            # Click the <td> element
            date.click()
            print(f"Clicked on the date: {today}")
            break
    else:
        print(f"No cell found with the date: {today}")
    
    
    month = 'Old'
    while month != 'Current':
        try:
            driver.find_element(By.XPATH,"//div[contains(@class, 'calendar right')]//th[contains(@class, 'next available')]").click()
        except:
            month = 'Current'
    date_list = driver.find_elements(By.XPATH, "//div[contains(@class,'calendar right')]//td[contains(@class, 'available')]")
    
    # Iterate through the cells to find the one containing the correct <span> text
    for date in date_list:
        # Check if the <span> inside the <td> matches the expected text
        span = date.find_element(By.XPATH, ".//span")  # Locate the <span> inside the <td>
        if span.text == today:
            # Click the <td> element
            date.click()
            print(f"Clicked on the date: {today}")
            break
    else:
        print(f"No cell found with the date: {today}")
    
    
    
    driver.find_element(By.XPATH, "//button[@class='btn' and text() = 'ok']").click()
    print('click ok')
    
    driver.find_element(By.XPATH, "//i[@class='fa fa-refresh']").click()
    
    total_avail_pages = len(driver.find_elements(By.XPATH, "//button[@aria-label='Next Page']"))
    for i in range(0,total_avail_pages+1):
        total_list = driver.find_elements(By.XPATH, "//table[@id='pn_id_2-table']//i[@class='fa fa-download']")
        for file in range(len(total_list)):
            total_list[file].click() #to download
            time.sleep(3)
            directory_path ='C:\\Users\\gurpreet.padam\\Capri\\Collections\\Selenium\\CommunicationsReports\\WA\\karix_wa'
            all_files = os.listdir(directory_path)
            zip_files = [file for file in all_files if file.endswith(".zip")]
            zip_files_with_path = [os.path.join(directory_path, file) for file in all_files if file.endswith(".zip")]
            for zip_fi in range(len(zip_files_with_path)):
                
                with zipfile.ZipFile(zip_files_with_path[zip_fi], 'r') as zip_ref:
                    
                    zip_ref.extractall(directory_path)  # Extract all files to the directory
                    print(zip_files_with_path[zip_fi])
                    print("Files extracted:", zip_ref.namelist())  # List of files in the zip
                    zip_ref.close()
                    os.remove(zip_files_with_path[zip_fi])
    
            print(file)
        try:
            driver.find_element(By.XPATH, "//button[@aria-label='Next Page']").click()
        except:
            pass


    time.sleep(20)
    driver.quit()

else:
    print(total_elements)
    
    
print('karix WA done')



opt = Options()
# opt.add_argument('--headless')
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,  # Disable notifications
    "download.default_directory": r"C:\Users\gurpreet.padam\Capri\Collections\Selenium\CommunicationsReports\WA\karix_wa_api",  # Set download path
    "directory_upgrade": True
    # "download.prompt_for_download": False,  # Disable download prompt
    # "plugins.always_open_pdf_externally": True  # Open PDFs directly without download prompt
})


opt.add_argument('--disable-gpu')
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
opt.add_experimental_option('useAutomationExtension', False)
    
    

# Configure Chrome options.
# opts = Options()

# Configure ChromeDriver service.
service = Service(ChromeDriverManager().install())

# Start the Chrome driver with the configured options and service.
driver = webdriver.Chrome(service=service, options=opt)

driver.get("https://wa.chatmybot.in/#/")
time.sleep(10)

username = driver.find_element(By.ID, "username")
username.send_keys("20352")


password = driver.find_element(By.ID, "password")
password.send_keys("8451021021")


first_num = driver.find_element(By.XPATH, "//input[@id='number1']").get_attribute("value")
second_num = driver.find_element(By.XPATH, "//input[@id='number2']").get_attribute("value")
calc_sign = driver.find_element(By.XPATH, "//span[contains(@class,'calculate')]").text

result = eval(f"{first_num} {calc_sign} {second_num}")

entr_tot = driver.find_element(By.XPATH, "//input[@placeholder='Enter Total']")
entr_tot.send_keys(result)

login = driver.find_element(By.XPATH, "//button[@class='btn btn-success']")
login.click()
time.sleep(12)

report_page = driver.find_element(By.XPATH, "//button[@title='Click Here To Select Service As Default' and text() = 'Select Service']")
report_page.click()

time.sleep(5)

fltr = driver.find_element(By.XPATH, "//button[@class='btn btn-add buttonStyle' and text() = 'Filter']")
fltr.click()
time.sleep(3)


strt_dt = driver.find_element(By.XPATH, "//input[@type='date' and @name = 'startdate']")
strt_dt.send_keys('00'+str(yesterday))

time.sleep(3)

end_dt = driver.find_element(By.XPATH, "//input[@type='date' and @name = 'enddate']")
end_dt.send_keys('00'+str(yesterday))

time.sleep(2)

driver.find_element(By.XPATH, "//button[@type='submit' and text() = 'Filter ']").click()
time.sleep(36)

driver.find_element(By.XPATH, "//button[@class='btn btn-add' and text() = 'Download DLR Report ']").click()
time.sleep(30)



try:
    read_file=pd.read_excel('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/WA/karix_wa_api/DLReport.xlsx')
    read_file.to_csv('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/WA/karix_wa_api/karix_wa_API_'+str(datetime.date.today() - datetime.timedelta(days=1))+'.csv', index = None,header=True) 
    os.remove('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/WA/karix_wa_api/DLReport.xlsx')
except:
    pass



    
    
