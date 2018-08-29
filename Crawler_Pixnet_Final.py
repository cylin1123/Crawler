# Author : Nick Lin 
# Date   : 2016.09.02
# coding: utf-8

# In[62]:

import requests
import time
import os
from bs4 import BeautifulSoup as bs
from urllib import urlretrieve

linklist=[]

def CrawerContent(source,directory):
    PicLink=[]
    domain = source.lstrip('http://').split('/')
    res = requests.get(source)
    soup = bs(res.content,from_encoding="utf8")
    try :        
        PicSource = soup.find_all('a',attrs={'class':'photolink'})        
        for item in PicSource:
            pic = item.get('href')
            if (pic.find('photo')>0):
                PicLink.append(pic)      
        for Pic in PicLink:
            CrawerPicInfo(Pic,directory) 
    except:        
        pass 
    
def CrawerPicInfo(Pic,directory):
    source = Pic
    res = requests.get(source)
    soup = bs(res.content,from_encoding="utf8")      
    img = soup.find('img',attrs={"id" : "item-frame-img"})
    imgsrc = img.get('src').replace('_n.','.')    
    #print imgsrc    
    RetrievePic(imgsrc ,directory)

def RetrievePic(imgsrc,directory):
    picname = imgsrc.lstrip('http://pic.pimg.tw/').split('/')
    SavePath =directory+'/'+picname[1]
    #print SavePath
    urlretrieve(imgsrc,SavePath)
    print 'Capture img from : '+imgsrc

def getPage(link):
    link = link.strip('\n')
    if link in linklist:
        savefolder = '/home/cylin/Code/Pixnet/Pic/'
        linklist.append(link.rstrip('\n'))
        UserID = link.lstrip('http://').split('.')
        directory = savefolder+UserID[0]
        if not os.path.exists(directory):
            os.makedirs(directory)
        CrawerContent(link,directory)        
        domain = link.lstrip('http://').split('/')    
        res = requests.get(link)   
        soup = bs(res.content,from_encoding="utf8")
        try :        
            pagelink = soup.find('a',attrs={'class':'nextBtn'}) 
            Newlink = 'http://'+domain[0] +pagelink.get('href')
            if Newlink not in linklist:
                linklist.append(Newlink)
                getPage(Newlink) 
        except:        
            pass
       
def main():    
    t1 = time.time()
    Tagetlist = open('/home/cylin/Code/Pixnet/list.txt')
    
    for link in Tagetlist:
        if link != '\n':
            linklist.append(link.strip('\n'))
            getPage(link)                              
            
    t2 = time.time()
    print 'Time Cost : ',t2-t1
if __name__=='__main__':
    main()

