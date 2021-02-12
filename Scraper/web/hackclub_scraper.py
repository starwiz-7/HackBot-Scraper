from selenium import webdriver
import os
from selenium.webdriver.common.by import By
import time
import sys
sys.path.append("..")
from db import get_hackathons, save_hackathons, delete_hackathons
# GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
# CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# driver = webdriver.Chrome(PATH)

driver.get("https://hackathons.hackclub.com/")
website = "HACKCLUB"
hacks = get_hackathons(website)

hacks_db = [i['name'] for i in hacks]
class HackClub:
    def __init__(self,name,start_date,end_date, location, mode, url, image):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.mode = mode
        self.url = url
        self.image = image
        self.website = "HACKCLUB"
def check_hackathon(scraped_hacks):
    delete = list(list(set(hacks_db)-set(scraped_hacks)))
    insert = list(list(set(scraped_hacks)-set(hacks_db)))
    print(insert)
    website = "HACKCLUB"
    for i in delete:
        delete_hackathons(i,website)
    
    for i in insert:
        for j in hackathons:
            if i == j.name:
                save_hackathons(j.name,j.start_date,j.end_date,j.mode,j.location,j.url,j.image,j.website)
                break  
hackathons = []
time.sleep(5)
try:
    l = 1
    while l<20:
        url = driver.find_element(By.XPATH, '/html/body/div/main/div/div/a['+str(l)+']')
        url = url.get_attribute('href')
        name = driver.find_element(By.XPATH, '/html/body/div/main/div/div/a['+str(l)+']/h3')
        name = name.get_attribute('innerHTML')
        date = driver.find_element(By.XPATH, '/html/body/div/main/div/div/a['+str(l)+']/footer/span[1]')
        date = date.get_attribute("innerHTML")
        date = list(map(str,date.split()))
            # print(date)
        st = date[1].split("–")
            # print(st)
        start = str(st[0]+" "+date[0])
        end = str(st[1]+" "+date[0])
        image = driver.find_element(By.XPATH, '/html/body/div/main/div/div/a['+str(l)+']/img[1]')
        image = image.get_attribute("src")
        if image == "https://hackathons.hackclub.com/mlh-logo-grayscale.svg":
            l+=1
            continue
        location = driver.find_element(By.XPATH, '/html/body/div/main/div/div/a['+str(l)+']/footer/span[2]/span')
        location = location.get_attribute("innerHTML")

        mode = ""
        if location == "Online":
            mode = "Digital"
        else:
            mode = "Physical"

        hack = HackClub(name,start,end,location,mode,url,image)
        print(hack.name)
        hackathons.append(hack)
        l+=1
except Exception as e:
    print(e)

names = [i.name for i in hackathons]
check_hackathon(names)
print("HackClub scraped")
driver.quit()