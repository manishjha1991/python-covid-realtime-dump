import requests
from bs4 import BeautifulSoup
import pymongo


def notifyMe(State_Name):
    myDict = {}
    myDict["state_name"] = State_Name[1]
    myDict["Total infected"] = State_Name[2]
    myDict["Total Recover"] = State_Name[3]
    myDict["Death"] = State_Name[4]
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dblist = myclient.list_database_names()
    if "vedantuTest" in dblist:
        print("The database exists.")
        mydb = myclient["vedantuTest"]
        mycol = mydb["details"]
        collist = mydb.list_collection_names()
        if "details" in collist:
            print(myDict)
            print("The collection exists.")
            inserted_Id = mycol.insert_one(myDict)
            print(inserted_Id.inserted_id)


URL = 'https://www.mohfw.gov.in/'
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
myDataStr = ""
for tr in soup.find_all('tbody'):
    myDataStr += tr.get_text()
    myDataStr = myDataStr[1:]
itemList = myDataStr.split("\n\n")
states = ["Andhra Pradesh", "Andaman and Nicobar Islands", "Arunachal Pradesh", "Assam", "Bihar", "	Chandigarh", "Chhattisgarh", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand",
          "Karnataka", "Kerala", "Ladakh", "Madhya Pradesh", "Maharashtra", "Manipur", "Mizoram", "Odisha", "Puducherry", "Punjab", "Rajasthan", "Tamil Nadu", "Telengana", "Uttarakhand", "Uttar Pradesh", "West Bengal"]
for item in itemList[0:22]:
    dataList = item.split("\n")
    if dataList[2] in states:
        notifyMe(dataList[1:])
