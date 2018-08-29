# Author : Nick Lin 
# Date   : 2019.09.15
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup as bs
from urllib import urlretrieve
import time
import os

def CrawerContent(source,folder):
    res = requests.get(source.strip('\n'))
    soup = bs(res.content,from_encoding="utf8")
    dv = soup.find_all('div',attrs={"id" : "pic"})
    for line in dv:
        for i in line.find_all('a'):    
            PicIdLink = 'http://photo.pchome.com.tw'+i.get('href')
            rs = requests.get(PicIdLink)                       
            imgsoup = bs(rs.content,from_encoding="utf8")
            img = imgsoup.find('img',attrs={"style" : "display:none"})
            RetrievePic(img.get('src'),folder)
                  
def RetrievePic(imgurl,folder):
    ImgName = imgurl.strip('http://link.photo.pchome.com.tw/').split('/')
    Pic = folder+'/'+ImgName[3]+".jpg"
    urlretrieve(imgurl,Pic)
    print 'Capture img from : '+imgurl
    
def getPage(source,directory):
    res = requests.get(source.strip('\n'))
    soup =bs(res.content,from_encoding="utf8")
    dv = soup.find_all('div',attrs={"class" : "page"})
    LinkList=[]
    LinkList.append(source.strip('\n'))
    for line in dv:
        for i in line.find_all('a'):  
            Item='http://photo.pchome.com.tw'+i.get('href')
            if Item not in LinkList:
                LinkList.append(Item)                
   
    for link in LinkList:
        CrawerContent(link,directory)
        
def main():
    t1 = time.time()
    linklist = open('/home/cylin/Code/Pchome/list.txt')
    savefolder = '/home/cylin/Code/Pchome/Pic'
    
    for link in linklist:
        if link != '\n':
            LinkTemp= link.strip('http://photo.pchome.com.tw/')
            PhotoId = LinkTemp.split('/')
            directory = savefolder + '/'+PhotoId[0]
            if not os.path.exists(directory):
                os.makedirs(directory)
            getPage(link,directory)            
            time.sleep(5)
    
    t2 = time.time()
    print 'Crawer Time : ',t2-t1
   
if __name__=='__main__':
    main()


