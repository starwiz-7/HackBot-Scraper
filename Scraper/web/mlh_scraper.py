from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
sys.path.append("..")
from Scraper.db import get_hackathons, save_hackathons, delete_hackathons
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://mlh.io")
website = "MLH"
hacks = get_hackathons(website)
# print(hacks)
hacks_db = [i['name'] for i in hacks]
# print(hacks_db)
class MLH:
    def __init__(self,name,start_date,end_date,location,mode,image,url):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.mode = mode
        self.image = image
        self.url = url
        self.website = "MLH"
    
def check_hackathon(scraped_hacks):
    delete = list(list(set(hacks_db)-set(scraped_hacks)))
    insert = list(list(set(scraped_hacks)-set(hacks_db)))
    print(insert)
    website = "MLH"
    for i in delete:
        delete_hackathons(i,website)
    
    for i in insert:
        for j in hackathons:
            if i == j.name:
                save_hackathons(j.name,j.start_date,j.end_date,j.mode,j.location,j.url,j.image,j.website)
                break        


attend_button = driver.find_element_by_class_name('join-area-btn')
attend_button.click()
time.sleep(2)
driver.switch_to.window(driver.window_handles[0])
hackathons = []
try:
    for l in range(1,27):
        name = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div['+str(l)+']/div/a')
        url = name.get_attribute('href')
        name = name.get_attribute('title')
        start = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div['+str(l)+']/div/a/div/meta[1]')
        start = start.get_attribute('content')
        end = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[1]/div['+str(l)+']/div/a/div/meta[2]')
        end = end.get_attribute('content')
        location = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div['+str(l)+']/div/a/div/div[4]/span[2]')
        location = location.get_attribute('innerHTML')
        mode = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div['+str(l)+']/div/a/div/div[1]/div')
        mode = mode.get_attribute('innerHTML')
        mode = mode.strip()
        image = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div['+str(l)+']/div/a/div/div[3]/img')
        image = image.get_attribute('src')
        hack = MLH(name,start,end,location,mode,image,url)
        hackathons.append(hack)
except Exception as e:
    print(e)
names = [i.name for i in hackathons]
print(hackathons)
check_hackathon(names)
driver.quit()