from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import sys
sys.path.append("..")
from Scraper.db import get_hackathons, save_hackathons, delete_hackathons
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://devpost.com/hackathons")
# hackathons = []
website = "DEVPOST"
hacks = get_hackathons(website)
hacks_db= [i['name'] for i in hacks]
class Devpost:
    def __init__(self,name,start_date,end_date, location, mode, url, image):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.mode = mode
        self.url = url
        self.image = image
        self.website = "DEVPOST"

def check_hackathon(scraped_hacks):
    delete = list(list(set(hacks_db)-set(scraped_hacks)))
    insert = list(list(set(scraped_hacks)-set(hacks_db)))
    print(insert)
    website = "Devpost"
    for i in delete:
        delete_hackathons(i,website)
      
    for i in insert:
        for j in hackathons:
            if i == j.name:
                save_hackathons(j.name,j.start_date,j.end_date,j.mode,j.location,j.url,j.image,j.website)
                break
hackathons = []
time.sleep(5)
while True:
    try:
        load_button = WebDriverWait(driver,10).until(
            lambda d: d.find_element(By.XPATH,'/html/body/section/div/div/div/div[1]/div[2]/a')
        )
        time.sleep(1)
        load_button.click()
        
        # /html/body/section/div/div/div/div[1]/div[1]/div[2]/div/article/a/div[1]/section/div/h2
    except:
        print("scroll finished")
        break
try:
    for i in range(1,100):
        status = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[1]/div[1]/div['+str(i)+']/div/article/a/div[2]/section/ul/li[2]/div/span')
        status = status.get_attribute('innerHTML')
        print(status)
        if(status == 'Submissions open soon'):
            name = driver.find_element(By.XPATH,'/html/body/section/div/div/div/div[1]/div[1]/div['+str(i)+']/div/article/a/div[1]/section/div/h2')
            name = name.get_attribute('innerHTML')
            name = name.strip()
            print(name,end="")
            location = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[1]/div[1]/div['+str(i)+']/div/article/a/div[1]/section/div/p[1]')
            location = location.get_attribute('innerHTML')
            # location = location.strip()
            print(location)
            url = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[1]/div[1]/div['+str(i)+']/div/article/a')
            url = url.get_attribute('href')
            print(url)
            image = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[1]/div[1]/div['+str(i)+']/div/article/a/div[1]/section/figure/img')
            image = image.get_attribute('src')
            print(image)
            mode = "Digital"
            # if(location != 'Online'):
                # mode = "Physical"
            hack = Devpost(name,'-','-',location,mode,url,image)
            hackathons.append(hack)
except Exception:
    print("Exception occured")

names = [i.name for i in hackathons]
print(hackathons)
check_hackathon(names)
driver.quit()