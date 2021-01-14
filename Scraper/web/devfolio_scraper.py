from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import sys
sys.path.append("..")
from Scraper.db import get_hackathons, save_hackathons, delete_hackathons
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://devfolio.co/hackathons")
hackathons = []
website = "DEVFOLIO"
hacks = get_hackathons(website)
hacks_db= [i['name'] for i in hacks]

class Devfolio:
    def __init__(self,name,start_date,end_date, location, mode, url):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.mode = mode
        self.url = url
        self.image = None
        self.website = "DEVFOLIO"

def check_hackathon(scraped_hacks):
    delete = list(list(set(hacks_db)-set(scraped_hacks)))
    insert = list(list(set(scraped_hacks)-set(hacks_db)))
    print(insert)
    website = "Devfolio"
    for i in delete:
        delete_hackathons(i,website)
      
    for i in insert:
        for j in hackathons:
            if i == j.name:
                save_hackathons(j.name,j.start_date,j.end_date,j.mode,j.location,j.url,j.image,j.website)
                break

time.sleep(5)
try:
    for i in range(1,15):
        name = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/section/div/div/div['+str(i)+']/div/div/div/div[1]/a/span/span[1]')
        # /html/body/div/div/div[2]/div/section/div/div/div[2]/div/div/div/div[1]/a/span/span[1]
        start = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/section/div/div/div['+str(i)+']/div/div/div/div[2]/div[1]/span[2]')
        end = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/section/div/div/div['+str(i)+']/div/div/div/div[2]/div[2]/span[2]')
        start = start.get_attribute('innerHTML')
        end = end.get_attribute('innerHTML')
        location = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/section/div/div/div['+str(i)+']/div/div/div/div[2]/div[3]/span')
        location = location.get_attribute('innerHTML')
        mode = ''
        if(location == 'Happening online'):
            mode = "Digital"
        url = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/section/div/div/div['+str(i)+']/div/div/div/div[1]/a')
        url = url.get_attribute('href')
        button_data = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/section/div/div/div['+str(i)+']/div/div/div/div[3]/button')    
        button_data = button_data.get_attribute('innerHTML')
        if(button_data == 'Apply now' or button_data == 'Participate'):
            name = name.get_attribute('innerHTML')
            hack = Devfolio(name,start,end,location,mode,url)
            hackathons.append(hack)
        else:
            break
except:
    print("Devfolio scraped")

# //*[@id="root"]/div/div[2]/div/section/div/div/div[9]/div/div/div/div[3]/button
# //*[@id="root"]/div/div[2]/div/section/div/div/div[8]/div/div/div/div[3]/button
# for i in hackathons:
#     print(i.name+" "+i.url+" "+i.start_date+"-"+i.end_date+" "+i.location+" "+i.mode)
names = [i.name for i in hackathons]
print(hackathons)
check_hackathon(names)
driver.quit()