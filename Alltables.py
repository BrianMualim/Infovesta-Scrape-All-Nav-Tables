import csv
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv
import os

# Load environment variables from .env file
env_path = "C:\\Users\\brian\\Downloads\\HPAM\\dotenv.env"
load_dotenv(dotenv_path=env_path)

# Access environment variables
api_key = os.getenv("API_KEY")
actualUsername = os.getenv("DBUSERNAME")
actualPassword = os.getenv("DBPASSWORD")

# Date must be Month-Date, Set up a list of months and a list of dates??
month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
year = ["2018", "2019", "2020", "2021", "2022", "2023"]

# Setting up webdriver
os.environ['PATH'] += r"C:/Program Files/ChromeDriver"
driver = webdriver.Chrome()

# Set driver to login website
driver.get("https://login.infovesta.com/login")

# Look for login details of username and password
username = driver.find_element("id", "username")
password = driver.find_element("id", "password")

# Send user details into login
username.send_keys(actualUsername)
password.send_keys(actualPassword)
# time.sleep(30)

# Click button to login
button = driver.find_element(By.CLASS_NAME, "btn")
button.click()
# time.sleep(5)

# Click button to cancel saham search value
button2 = driver.find_element(By.XPATH, "//ul[@id='chntype_taglist']/li/span[2]")
button2.click()

# Click button to activate the dropdown menu
inputElement = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/input")
inputElement.send_keys("Semua")
inputElement.send_keys(Keys.ENTER)
time.sleep(2)

# PHASE WEBSCRAPING
dates = []

# Make if statements for month
# 31 Days: Jan Mar May Jul Aug Oct Dec
# 30 Days: Apr Jun Sep Nov
# 28 Days: Feb

for i in range(len(year)):
    for j in range(len(month)):
        if month[j] == "Jan" or month[j] == "Mar" or month[j] == "May" or month[j] == "Jul" or month[j] == "Aug" or month[j] == "Oct" or month[j] == "Dec":
            setDate = "31-" + month[j] + "-" + year[i]
        if month[j] == "Apr" or month[j] == "Jun" or month[j] == "Sep" or month[j] == "Nov":
            setDate = "30-" + month[j] + "-" + year[i]
        if month[j] == "Feb":
            setDate = "28-" + month[j] + "-" + year[i]
        # setDateDictionary = {
        #     "date": setDate
        # }
        dates.append(setDate)

        if setDate == "31-Jul-2023":
            break

data = []
for i in range(len(dates)):
    #
    # setDate = "31-Jan-2018"
    driver.get("https://data.infovesta.com/reksadana/data/datafeed?date=" + dates[i])
    time.sleep(1)

    string_before = "{"
    string_after = "}"

    page_source = driver.page_source

    end_index = 0
    for char in page_source:
        if char == "{":
            start_index = page_source.find(string_before, end_index)
            end_index = page_source.find(string_after, start_index) + len(string_before)
            companyDetails = page_source[start_index:end_index].strip()

            companyDetails = re.sub(r'\b' + re.escape("null") + r'\b', '"null"', companyDetails)
            companyDetails = re.sub(r'\b' + re.escape("false") + r'\b', 'False', companyDetails)
            companyDetails = re.sub(r'\b' + re.escape("true") + r'\b', 'True', companyDetails)

            dictionary = eval(companyDetails)
            data.append(dictionary.values())

    if i == 12:
        break

filename = "C:\\Users\\brian\\Downloads\\crime.csv"

column_names = ['Nama', 'Jenis','Manajer Investasi', 'Kustodian', 'Denominasi', 'Deviden', 'Syariah', 'NAB/UP', '1hr(%)','1mgg(%)','MTD(%)','1bln(%)', '3bln(%)','6bln(%)','YTD(%)','1thn(%)','3thn(%)','5thn(%)','AUM','Unit','AUM MI', 'AUM Dolar', 'Kepemilikan', 'Tanggal Penawaran Umum']
data.insert(0, column_names)

with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)

# rightButton = driver.find_element(By.XPATH, "//div[@id='kendogrid']/div[5]/a[3]")
#
# while "disabled" not in rightButton.get_attribute("class"):
#     # Click the button
#     rightButton.click()
#     time.sleep(1)  # Wait for a second (optional)

# So now I have dates
# https://data.infovesta.com/reksadana/data/datafeed?date=28-Apr-2018
# //div[@id="kendogrid"]/div[4]/table/tbody/tr[1]/td[3]
