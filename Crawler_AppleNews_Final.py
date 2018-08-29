# Author : Nick Lin 
# Date   : 2017.09.18
# coding: utf-8

# In[1]:


import requests
import jieba
import jieba.analyse as jalz
import datetime
import time
import re
import json
import sys
from bs4 import BeautifulSoup
from pymongo import MongoClient

def ParseDateTime(gettime):
    Time = re.findall("[0-9]+",str(gettime)) #去除中文字元
    return datetime.datetime(int(Time[0]), int(Time[1]) ,int(Time[2]) ,int(Time[3]) ,int(Time[4]) ,00, 00000)

def isExist(NewsLink):
     NewsCount = db.News.find({"NewsLink":NewsLink}).count()
     if NewsCount == 0:
            return False
     else:
            return True
        
def Extract_Tags(sentence):    
    jieba.load_userdict("/home/cylin/Code/user_dict") #自訂詞庫檔
    jieba.analyse.set_stop_words("/home/cylin/Code/stopwords")
    words = jalz.extract_tags(sentence,15,allowPOS=['n'])
    #print ",".join(words)
    return words

t1 = time.time()       


for i in range(int(sys.argv[1]),int(sys.argv[2])):
    domainurl='http://www.appledaily.com.tw/realtimenews/section/new/'
    domain = 'http://www.appledaily.com.tw/'
    if i==1:
        domainurl='http://www.appledaily.com.tw/realtimenews/section/new/'
    else:
        
        domainurl='http://www.appledaily.com.tw/realtimenews/section/new/'+str(i+1)

    res = requests.get(domainurl)
    soup = BeautifulSoup(res.text)

    for news in soup.select('.rtddt'):
        link = news.select('a')[0]['href']
        Type = news.select('h2')[0].text
     
        if  link.find(domain) ==-1:       
            NewsLink = domain+link
        else:
            NewsLink = link
    
        rs =requests.get(NewsLink)
        soup_news = BeautifulSoup(rs.text)    
        Title = soup_news.find_all('h1',attrs={"id" : "h1"})[0].text.encode('utf-8') 
        NewsTime = ParseDateTime(soup_news.find_all('div',attrs={"class" : "gggs"})[0].text.encode('utf-8')) 
    
        #decompose unnecessary tag content
        for div in soup_news.find_all('div',attrs={"id" : "teadstv"}):
            div.decompose()
        for div in soup_news.find_all('div',attrs={"id" : "goldenhorse"}):
            div.decompose()
        for div in soup_news.find_all('div',attrs={"id" : "textlink"}):
            div.decompose()
        for div in soup_news.find_all('a'):
            div.decompose()
        for div in soup_news.find_all('strong'):
            div.decompose()
        for div in soup_news.find_all('Script'):
            div.decompose()
        p=re.compile('\s+')   
        Content= (soup_news.find_all('div',attrs={"class" : "articulum trans"}))[0].text.encode('utf-8').strip()    
        Content=re.sub(p,'',Content)
        #print NewsTime,NewsLink,Type,Title,Content
    
        conn = MongoClient(host='127.0.0.1',port=27017)
        db = conn.SocialMedia #連接資料庫MyPyMongo
        News = db.AppleNews #連接Collection News
    
        keywords = Extract_Tags(Content)
    
        bsonNews ={ "Source" :"AppleNews",
                    "Type":Type,
                    "Title":Title,
                    "Content":Content,
                    "NewsLink":NewsLink,
                    "ReleaseTime":NewsTime,
                    "ImportDate": datetime.datetime.utcnow()
                    #"Tags" : Extract_Tags(Content)
                 }    
    
        if(isExist(NewsLink) == True):
            print('Is Exist...',Title)
            News.update({"NewsLink":NewsLink},{"$set":bsonNews},upsert=True,multi=False)
        else:
            print('Insert Success...',Title)
            News.update({"NewsLink":NewsLink},{"$set":bsonNews},upsert=True,multi=False)

t2 = time.time()
print ("Time Cost: ",t2-t1)

