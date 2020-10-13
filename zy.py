from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz
from getpass import getpass

url = input("textbook url: ")
email = input("email: ")
password  = getpass(f"password: ")


xpaths = {
    'email-input': '//*[@id="ember13"]',
    'password-input': '//*[@id="ember15"]',
    'assignments-btn': '//*[@id="ember150"]/div[2]/button[3]'
}

driver = webdriver.Chrome()
driver.get(url)

email_inp = driver.find_element_by_xpath(xpaths['email-input'])
email_inp.send_keys(email)

pwd_inp = driver.find_element_by_xpath(xpaths['password-input'])
pwd_inp.send_keys(password)

pwd_inp.send_keys(Keys.ENTER)


assignments_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpaths['assignments-btn']))
    )
assignments_btn.click()


assignments = driver.find_elements_by_class_name("assignment-summary");




cal = Calendar()


for assignment in assignments:
    name = assignment.find_elements_by_tag_name('h4')[0].get_attribute('innerHTML')
    date_time_str = assignment.find_elements_by_class_name('due-date-text')[0].find_elements_by_tag_name("div")[0].get_attribute('innerHTML')[:-1]

    eventName = "Assignment due: "+name
    eventDuration = {'minutes':30}

    eventStartTime = datetime.strptime(date_time_str, '%m/%d/%Y, %H:%M %p')
    eventStartTime_aware = eventStartTime+timedelta(hours=7)

    e = Event(name = eventName, duration = eventDuration, begin = eventStartTime_aware.strftime("%Y-%m-%d %H:%M") )
    cal.events.add(e)
    print(f"{e.name} due {e.begin}")

print(cal.events)


with open('calendar.ics', 'w') as f:
    f.write(str(cal))