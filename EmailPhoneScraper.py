import re
import requests
import csv
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


class EmailPhoneScraper:
    def __init__(self):
        super().__init__()
        self.outfile = open('sixty-one.csv','w+', newline='')
        self.writer = csv.writer(self.outfile,quoting=csv.QUOTE_ALL)
        self.writer.writerow(["Emails           ", "Website          ","Phone Number         ", "Facebook               ","Twitter               ","Instagram                ","Linkedin             ","Youtube              "])
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) self.leWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        self.original_url = """https://www.adamdpope.co.uk/
https://www.abchairextension.co.uk/
https://www.allsettled.com/
https://www.adebesoshodiya.com/
https://www.alisonandjack.co.uk/
https://www.69harleyst.com/
https://www.2021census.com/
https://www.alanstewart.co.uk/
https://www.activelifestyleprotection.com/
https://www.4psm.co.uk/
https://www.2jjsplant.co.uk/
https://www.allsaintswithstjamesb-sea.co.uk/
https://www.worlduniversitypreparation.com/
https://www.yecco.co.uk/
https://www.yakamazi.com/
https://www.yourcaresolutions.com/
https://www.yoursingingwaiters.co/
https://www.zanmail.co.uk/
https://www.yourfinancialtoolbox.co.uk/
https://www.yourselfempowered.com/
https://www.unikaprodukte.de/
https://www.wearemachine.co.uk/
https://www.xpressbanners.co.uk/
https://www.villazinnia.com/
https://www.worcestersurfacing.co.uk/
https://www.world-compare.com/
https://www.witchsworkshop.com/
https://www.yellmusic.com/
https://www.umbrianliving.com/
https://www.wlmf.net/
https://www.youthfulyou.wales/
""".replace("\n", " ").split(" ")
#.replace("\n", " ").replace("//","http://").split(" ")


    def parseData(self, original_url):
        response = ''

        try:
            response = requests.get(original_url,verify = False ,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) self.leWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'})
            soup = BeautifulSoup(response.text, 'lxml')
        

            result =[]

            # print(phone)
            facebook = ''
            twitter = ''
            linkedin = ''
            instagram =''
            youtube =''
            contactus = ''
            email =''
            phoneNumber= ''

            for link in soup.find_all('a', href=True):

                if "facebook.com" in link['href']:
                    facebook = link['href']

                if "twitter.com" in link['href']:
                    twitter = link['href']

                if "linkedin.com" in link['href']:
                    linkedin = link['href']

                if "instagram.com" in link['href']:
                    instagram =link['href']

                if "youtube.com" in link['href']:
                    youtube = link['href']

                if "contact" in link['href'] and "contact" not in original_url:
                    if 'http' in link['href']:
                        contactus = link['href']
                    else:
                        contactus = original_url+link['href']

            email = self.getEmailFinder(str(soup))
            phoneNum = self.getPhone(str(soup))


            if email == "":
                email = self.findEmail(soup)

            if phoneNum == "":
                phoneNum = "(" + self.findPhoneNumber(soup) +")"

            if email =="" and contactus != "" and original_url != contactus:
                self.parseData(contactus)
                return 

            print(email)
            print(phoneNum)
            result.append(email)
            result.append(original_url)
            result.append(phoneNum)
            result.append(facebook)
            result.append(twitter)
            result.append(linkedin)
            result.append(instagram)
            result.append(youtube)


            print(result)
            print("email " + email)
            print(" number " + phoneNum)
            self.writer.writerow(result)
        except Exception as e:
            print(e)
            
        

    
    def getEmailFinder(self,string):
            email = ''
            emailRegEx = re.compile('\"mailto\:[0-9a-zA-Z\@\.]{1,}\"')
            m = emailRegEx.search(string)
            if m:
                email = m.group(0)[8:-1]
            return email

    def getPhone(self,string):
            phone = ''
            phoneRegEx = re.compile('\"tel\:[\(\)\-0-9\ ]{1,}\"')
            m = phoneRegEx.search(string)
            if m:
                phone = m.group(0)[5:-1]
            return phone
        
    def findNumberHelper(self,resultString , index):
        resultNumber = ''
        
        if index != -1:
            #substring from index to 30 ahead string and convert to array
            # after the array select second string index 1 to get number 
            if(len(resultString) > index+30):
                resultNumberArray = resultString[index:index+30].replace("\n"," ").split(" ")
                print(resultNumberArray)
                numberFlag = False 
                stringFlag = False
                for rn in resultNumberArray:
                    if rn.isdigit() and not stringFlag:
                        resultNumber += rn
                        numberFlag = True
                    elif numberFlag:
                        stringFlag = True
                    
            else:
                resultNumberArray = resultString[index:len(resultString)].replace("\n"," ").split(" ")
                numberFlag = False 
                stringFlag = False
                for rn in resultNumberArray:
                    if rn.isdigit() and not stringFlag:
                        resultNumber += rn
                        numberFlag = True
                    elif numberFlag:
                        stringFlag = True 
            
            
        return resultNumber 

        
        
    def findPhoneNumber(self,soupValue):
        resultString = soupValue.getText().lower()
        resultNumber = ''
        
        index = resultString.find("phonenumber")
        if resultNumber == "":
            resultNumber = self.findNumberHelper(resultString, index)
            
        index = resultString.find("telephone")
        if resultNumber == "":
            resultNumber = self.findNumberHelper(resultString, index)
        
        index = resultString.find("phone")
        if resultNumber == "":
            resultNumber = self.findNumberHelper(resultString, index)
        
        index = resultString.find("number")
        if resultNumber == "":
            resultNumber = self.findNumberHelper(resultString, index)
        
        index = resultString.find("tel")
        if resultNumber == "":
            resultNumber = self.findNumberHelper(resultString, index)
            
        index = resultString.find("contact")
        if resultNumber == "":
            resultNumber = self.findNumberHelper(resultString, index)
            
            
        return resultNumber
            
        
        
    def findEmail(self,soupValue):
        #lower the all the string values 
        resultString = soupValue.getText().lower()
        resultEmail = ''
        
        for val in resultString.strip().replace("\n"," ").replace(","," ").replace("\""," ").split(" "):
                if re.findall('\S+@\S+', val):
                    print("the email is " + val + " end email")
                    resultEmail = val

        return resultEmail
            

    def runScraper(self):
        #Multithreading for looping All links
        try:
            with ThreadPoolExecutor(max_workers=1000) as executor:
                executor.map(self.parseData,self.original_url)
        except Exception as e: print(e)
        # for url in self.original_url:
            # print(url)
            # self.parseData(url)
            

        self.outfile.close()

    







emailPhoneScraper = EmailPhoneScraper()
emailPhoneScraper.runScraper()
