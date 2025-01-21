from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
import datetime
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
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\gurpreet.padam\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Update path as needed

# import tesseract
# Configure the Selenium webdriver

import time


os.environ['WDM_SSL_VERIFY'] = '0'

status='CGCL SMS started'
print(status)
while (status != 'Done for the day PRP SMS CGCL'):
    try:
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_argument("--disable-extensions")
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,  # Disable notifications
            "download.default_directory": r"C:\Users\gurpreet.padam\Capri\Collections\Selenium\CommunicationsReports\SMS\PrpSmsCgcl",  # Set download path
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
        
        
        
        driver.get("http://prpsms.co.in")
        username = driver.find_element(By.ID, "txtUserId")
        username.send_keys("20140797")
        password = driver.find_element(By.ID, "txtPassword")
        password.send_keys("LoansCapri123*")
        accept_button = driver.find_element(By.ID,'chkAccept')
        accept_button.click()
        
        
        # Locate the CAPTCHA image element
        captcha_element = driver.find_element(By.XPATH, "//img[@src='ca.aspx']")  # Adjust selector as needed
        captcha_screenshot = captcha_element.screenshot_as_png
        
        # Save the CAPTCHA as a PNG file
        img_file = "captcha_element.png"
        with open(img_file, "wb") as file:
            file.write(captcha_screenshot)
        
        # Open the CAPTCHA image
        captcha_image = Image.open(img_file)
        # Preprocess the image
        captcha_image = captcha_image.convert("L")  # Convert to grayscale
        captcha_image = captcha_image.filter(ImageFilter.SHARPEN)  # Sharpen the image
        captcha_image = captcha_image.resize((captcha_image.width * 3, captcha_image.height * 3))  # Resize for better OCR
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(captcha_image)
        captcha_image = enhancer.enhance(2)  # Increase contrast
        enhancer = ImageEnhance.Sharpness(captcha_image)
        captcha_image = enhancer.enhance(2)  # Increase Sharpness
        enhancer = ImageEnhance.Brightness(captcha_image)
        captcha_image = enhancer.enhance(2)  # Increase Brightness
        captcha_image
        
        # Save the processed image for debugging (optional)
        captcha_image.save("processed_image.png")
        
        # Extract text from the processed image
        captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6')
        cleaned_text = re.sub(r"[^\d\+\-\*/]", "", captcha_text)  # Keep only digits and math operators
        cleaned_text = cleaned_text.replace("—", "-")  # Replace long dash with standard dash
        
        print(f"Cleaned Text: {cleaned_text}")
        
        # Parse and solve the math problem
        match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", cleaned_text)
        
        # Parse and solve the math problem
        # match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", captcha_text.strip())
        if match:
            num1 = int(match.group(1))
            operator = match.group(2)
            num2 = int(match.group(3))
        
            # Solve the math problem
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                result = num1 / num2
        
            print(f"Extracted CAPTCHA: {captcha_text.strip()}, Result: {result}")
        
        
        # Enter the result in the CAPTCHA input field
        captcha_input = driver.find_element(By.ID, "txtCaptcha")  # Adjust selector as needed
        captcha_input.clear()
        captcha_input.send_keys(str(result))
        
        # Click the login button
        login_button = driver.find_element(By.ID, "btnLogin")  # Adjust selector for the login button
        login_button.click()
    
        time.sleep(3)
        mis = driver.find_element(By.LINK_TEXT,"MIS")
        mis.click()
        time.sleep(3)
        
        drn = driver.find_element(By.LINK_TEXT,"Delivery Report New")
        drn.click()
        time.sleep(3)
        
        dropdown = driver.find_element(By.CLASS_NAME, 'frm_dropdown2')
        dropdown.send_keys('Yesterday')
        time.sleep(3)
        # dropdown.send_keys('send_keys')
        search = driver.find_element(By.XPATH, "//i[@class='fa fa-search']")
        search.click()
        time.sleep(3)
        
        file_type = driver.find_element(By.ID, 'ContentPlaceHolder1_ddlDownload')
        file_type.send_keys('Excel')
        time.sleep(3)
        
        download = driver.find_element(By.XPATH, "//i[@class='fa fa-download']")
        download.click()
        time.sleep(10)
        try:
            read_file=pd.read_table('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCgcl/Report.xls')
            read_file.to_csv('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCgcl/CGCL_ENG_SMS_UI_'+str(datetime.date.today() - datetime.timedelta(days=1))+'.csv', index = None,header=True) 
            os.remove('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCgcl/Report.xls')
        except:
            pass
        print('UI done')
        
        source = driver.find_element(By.ID, 'ContentPlaceHolder1_ddlUploadSource')
        source.send_keys('API')
        search = driver.find_element(By.XPATH, "//i[@class='fa fa-search']")
        search.click()
        time.sleep(3)
        download = driver.find_element(By.XPATH, "//i[@class='fa fa-download']")
        download.click()
        time.sleep(10)
        try:
            read_file=pd.read_table('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCgcl/Report.xls')
            read_file.to_csv('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCgcl/CGCL_ENG_SMS_API_'+str(datetime.date.today() - datetime.timedelta(days=1))+'.csv', index = None,header=True) 
            os.remove('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCgcl/Report.xls')
        except:
            pass
        print('API done')
    
        
        
        driver.quit()
        
        status = 'Done for the day PRP SMS CGCL'
        print('Done for the day PRP SMS CGCL')

    except:
        try:
            driver.quit()
        except:
            pass
        pass




status='CGHFL SMS started'
print(status)
while (status != 'Done for the day PRP SMS CGHFL'):
    try:
        
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_argument("--disable-extensions")
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,  # Disable notifications
            "download.default_directory": r"C:\Users\gurpreet.padam\Capri\Collections\Selenium\CommunicationsReports\SMS\PrpSmsCghfl",  # Set download path
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
        
        
        
        driver.get("http://prpsms.co.in")
        username = driver.find_element(By.ID, "txtUserId")
        username.send_keys("20180234")
        password = driver.find_element(By.ID, "txtPassword")
        password.send_keys("LoansCghfl1234*")
        accept_button = driver.find_element(By.ID,'chkAccept')
        accept_button.click()
        
        
        # Locate the CAPTCHA image element
        captcha_element = driver.find_element(By.XPATH, "//img[@src='ca.aspx']")  # Adjust selector as needed
        captcha_screenshot = captcha_element.screenshot_as_png
        
        # Save the CAPTCHA as a PNG file
        img_file = "captcha_element.png"
        with open(img_file, "wb") as file:
            file.write(captcha_screenshot)
        
        # Open the CAPTCHA image
        captcha_image = Image.open(img_file)
        # Preprocess the image
        captcha_image = captcha_image.convert("L")  # Convert to grayscale
        captcha_image = captcha_image.filter(ImageFilter.SHARPEN)  # Sharpen the image
        captcha_image = captcha_image.resize((captcha_image.width * 3, captcha_image.height * 3))  # Resize for better OCR
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(captcha_image)
        captcha_image = enhancer.enhance(2)  # Increase contrast
        enhancer = ImageEnhance.Sharpness(captcha_image)
        captcha_image = enhancer.enhance(2)  # Increase Sharpness
        enhancer = ImageEnhance.Brightness(captcha_image)
        captcha_image = enhancer.enhance(2)  # Increase Brightness
        captcha_image
        
        # Save the processed image for debugging (optional)
        captcha_image.save("processed_image.png")
        
        # Extract text from the processed image
        captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6')
        cleaned_text = re.sub(r"[^\d\+\-\*/]", "", captcha_text)  # Keep only digits and math operators
        cleaned_text = cleaned_text.replace("—", "-")  # Replace long dash with standard dash
        
        print(f"Cleaned Text: {cleaned_text}")
        
        # Parse and solve the math problem
        match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", cleaned_text)
        
        # Parse and solve the math problem
        # match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", captcha_text.strip())
        if match:
            num1 = int(match.group(1))
            operator = match.group(2)
            num2 = int(match.group(3))
        
            # Solve the math problem
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                result = num1 / num2
        
            print(f"Extracted CAPTCHA: {captcha_text.strip()}, Result: {result}")
        
        
        # Enter the result in the CAPTCHA input field
        captcha_input = driver.find_element(By.ID, "txtCaptcha")  # Adjust selector as needed
        captcha_input.clear()
        captcha_input.send_keys(str(result))
        
        # Click the login button
        login_button = driver.find_element(By.ID, "btnLogin")  # Adjust selector for the login button
        login_button.click()
        time.sleep(3)
        
        
        mis = driver.find_element(By.LINK_TEXT,"MIS")
        mis.click()
        time.sleep(3)
        
        drn = driver.find_element(By.LINK_TEXT,"Delivery Report New")
        drn.click()
        time.sleep(3)
        
        dropdown = driver.find_element(By.CLASS_NAME, 'frm_dropdown2')
        dropdown.send_keys('Yesterday')
        time.sleep(3)
        # dropdown.send_keys('send_keys')
        search = driver.find_element(By.XPATH, "//i[@class='fa fa-search']")
        search.click()
        time.sleep(3)
        
        file_type = driver.find_element(By.ID, 'ContentPlaceHolder1_ddlDownload')
        file_type.send_keys('Excel')
        time.sleep(3)
        
        download = driver.find_element(By.XPATH, "//i[@class='fa fa-download']")
        download.click()
        time.sleep(10)
        try:
            read_file=pd.read_table('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCghfl/Report.xls')
            read_file.to_csv('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCghfl/CGHFL_ENG_SMS_UI_'+str(datetime.date.today() - datetime.timedelta(days=1))+'.csv', index = None,header=True) 
            os.remove('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCghfl/Report.xls')
        except:
            pass
        print('UI done')
        
        source = driver.find_element(By.ID, 'ContentPlaceHolder1_ddlUploadSource')
        source.send_keys('API')
        search = driver.find_element(By.XPATH, "//i[@class='fa fa-search']")
        search.click()
        time.sleep(3)
        download = driver.find_element(By.XPATH, "//i[@class='fa fa-download']")
        download.click()
        time.sleep(10)
        try:
            read_file=pd.read_table('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCghfl/Report.xls')
            read_file.to_csv('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCghfl/CGHFL_ENG_SMS_API_'+str(datetime.date.today() - datetime.timedelta(days=1))+'.csv', index = None,header=True) 
            os.remove('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsCghfl/Report.xls')
        except:
            pass
        print('API done')
    
        
        driver.quit()
        
        status = 'Done for the day PRP SMS CGHFL'
        print('Done for the day PRP SMS CGHFL')
    except:
        try:
            driver.quit()
        except:
            pass
        pass




status='Gold SMS started'
print(status)
while (status != 'Done for the day PRP SMS Gold'):
    try:
        
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_argument("--disable-extensions")
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,  # Disable notifications
            "download.default_directory": r"C:\Users\gurpreet.padam\Capri\Collections\Selenium\CommunicationsReports\SMS\PrpSmsGold",  # Set download path
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
        
        
        
        driver.get("http://prpsms.co.in")
        username = driver.find_element(By.ID, "txtUserId")
        username.send_keys("20220239")
        password = driver.find_element(By.ID, "txtPassword")
        password.send_keys("LcvkH4e9")
        accept_button = driver.find_element(By.ID,'chkAccept')
        accept_button.click()
        
        
        # Locate the CAPTCHA image element
        captcha_element = driver.find_element(By.XPATH, "//img[@src='ca.aspx']")  # Adjust selector as needed
        captcha_screenshot = captcha_element.screenshot_as_png
        
        # Save the CAPTCHA as a PNG file
        img_file = "captcha_element.png"
        with open(img_file, "wb") as file:
            file.write(captcha_screenshot)
        
        # Open the CAPTCHA image
        captcha_image = Image.open(img_file)
        # Preprocess the image
        captcha_image = captcha_image.convert("L")  # Convert to grayscale
        captcha_image = captcha_image.filter(ImageFilter.SHARPEN)  # Sharpen the image
        captcha_image = captcha_image.resize((captcha_image.width * 3, captcha_image.height * 3))  # Resize for better OCR
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(captcha_image)
        captcha_image = enhancer.enhance(2)  # Increase contrast
        enhancer = ImageEnhance.Sharpness(captcha_image)
        captcha_image = enhancer.enhance(2)  # Increase Sharpness
        enhancer = ImageEnhance.Brightness(captcha_image)
        captcha_image = enhancer.enhance(2)  # Increase Brightness
        captcha_image
        
        # Save the processed image for debugging (optional)
        captcha_image.save("processed_image.png")
        
        # Extract text from the processed image
        captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6')
        cleaned_text = re.sub(r"[^\d\+\-\*/]", "", captcha_text)  # Keep only digits and math operators
        cleaned_text = cleaned_text.replace("—", "-")  # Replace long dash with standard dash
        
        print(f"Cleaned Text: {cleaned_text}")
        
        # Parse and solve the math problem
        match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", cleaned_text)
        
        # Parse and solve the math problem
        # match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", captcha_text.strip())
        if match:
            num1 = int(match.group(1))
            operator = match.group(2)
            num2 = int(match.group(3))
        
            # Solve the math problem
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                result = num1 / num2
        
            print(f"Extracted CAPTCHA: {captcha_text.strip()}, Result: {result}")
        
        
        # Enter the result in the CAPTCHA input field
        captcha_input = driver.find_element(By.ID, "txtCaptcha")  # Adjust selector as needed
        captcha_input.clear()
        captcha_input.send_keys(str(result))
        
        # Click the login button
        login_button = driver.find_element(By.ID, "btnLogin")  # Adjust selector for the login button
        login_button.click()
        time.sleep(3)
    
        
        mis = driver.find_element(By.LINK_TEXT,"MIS")
        mis.click()
        time.sleep(3)
        
        drn = driver.find_element(By.LINK_TEXT,"Delivery Report New")
        drn.click()
        time.sleep(3)
        
        dropdown = driver.find_element(By.CLASS_NAME, 'frm_dropdown2')
        dropdown.send_keys('Yesterday')
        time.sleep(3)
        # dropdown.send_keys('send_keys')
        search = driver.find_element(By.XPATH, "//i[@class='fa fa-search']")
        search.click()
        time.sleep(3)
        
        file_type = driver.find_element(By.ID, 'ContentPlaceHolder1_ddlDownload')
        file_type.send_keys('Excel')
        time.sleep(3)
        
        download = driver.find_element(By.XPATH, "//i[@class='fa fa-download']")
        download.click()
        time.sleep(10)
        try:
            read_file=pd.read_table('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsGold/Report.xls')
            read_file.to_csv('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsGold/GOLD_ENG_SMS_UI_'+str(datetime.date.today() - datetime.timedelta(days=1))+'.csv', index = None,header=True) 
            os.remove('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsGold/Report.xls')
        except:
            pass
        print('UI done')
        
        source = driver.find_element(By.ID, 'ContentPlaceHolder1_ddlUploadSource')
        source.send_keys('API')
        search = driver.find_element(By.XPATH, "//i[@class='fa fa-search']")
        search.click()
        time.sleep(3)
        download = driver.find_element(By.XPATH, "//i[@class='fa fa-download']")
        download.click()
        time.sleep(10)
        try:
            read_file=pd.read_table('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsGold/Report.xls')
            read_file.to_csv('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsGold/GOLD_ENG_SMS_API_'+str(datetime.date.today() - datetime.timedelta(days=1))+'.csv', index = None,header=True) 
            os.remove('C:/Users/gurpreet.padam/Capri/Collections/Selenium/CommunicationsReports/SMS/PrpSmsGold/Report.xls')
        except:
            pass
        print('API done')
    
        
        driver.quit()
        
        status = 'Done for the day PRP SMS Gold'
        print('Done for the day PRP SMS Gold')
    except:
        try:
            driver.quit()
        except:
            pass
        pass
    
