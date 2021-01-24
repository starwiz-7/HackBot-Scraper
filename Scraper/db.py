from pymongo import MongoClient
import os
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)

bot = client.get_database("HackBot")
hackathons = bot.get_collection("Hackathons")


def save_hackathons(name,start,end,mode,location,url,image,website):
    hackathons.insert_one(
        {'name':name,'url':url,'image':image,'start':start,'end':end,'mode':mode,'location':location, 'website':website, 'new':True}
    )

def delete_hackathons(name,website):
    hackathons.delete_one(
        {'name':name,'website':website}
    )

def get_hackathons(website):
    return list(hackathons.find({'website':website},{"_id":0,"name":1}))

