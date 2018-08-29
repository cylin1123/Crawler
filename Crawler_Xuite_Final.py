# Author : Nick Lin 
# Date   : 2016.08.31
# coding: utf-8

# In[15]:

import requests
from bs4 import BeautifulSoup as bs
import time
import os
from urllib import urlretrieve

def CrawerContent(link,directory):
    print link
    res = requests.get(link)
    soup = bs(res.content,from_encoding="utf8")
    #print soup
    
    ImgLink=soup.find_all('img',attrs={'class':'photo_cover fixed'})
    if ImgLink ==[]:
        ImgLink=soup.find_all('img',attrs={'class':'photo_cover '})
    else:
        pass
      
    for item in ImgLink:
        print "src:"+item.get('src')
        RetrievePic(item.get('src').replace('_c.','_x.'),directory)

def RetrievePic(imgsrc,directory):
    picname = imgsrc.lstrip('http://').split('/')
    SavePath =directory+'/'+picname[4]
    urlretrieve(imgsrc,SavePath)
    print 'Capture img from : '+imgsrc

def getPage(link,directory):
    PageNum=[]
    LinkList=[]
    LinkList.append(link)
    res = requests.get(link.strip('\n'))
    soup =bs(res.content,from_encoding="utf8")
    dv = soup.find_all('div',attrs={"class" : "page"})        
    for line in dv:
        for i in line.find_all('a'):
            num = i.get('href').split('*')
            if num not in PageNum:
                PageNum.append(int(num[1]))
                
    if len(PageNum) !=0:
        for i in range(2,max(PageNum)+1):
            PageLink=link+'*'+str(i)
            LinkList.append(PageLink)
             
    if len(LinkList)==1:
            CrawerContent(link,directory) 
    else:
        for source in LinkList:
            CrawerContent(source,directory)            
    
def main():
    t1 = time.time()
    linklist = open('/home/cylin/Code/Xuite/list.txt')
    savefolder = '/home/cylin/Code/Xuite/Pic/'
    for link in linklist:
        if link != '\n':
            LinkTemp= link.strip('http://')
            PhotoId = LinkTemp.split('/')
            directory = savefolder +PhotoId[1]+'/'+PhotoId[2]
            if not os.path.exists(directory):
                os.makedirs(directory) 
            getPage(link.strip('\n'),directory)
    
    t2 = time.time()
    print 'Time Cost : ',t2-t1

if __name__=='__main__':
    main()

