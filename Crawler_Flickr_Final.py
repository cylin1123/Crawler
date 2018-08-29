# Author : Nick Lin 
# Date   : 2017.08.31
# coding: utf-8

# In[84]:

import requests
from bs4 import BeautifulSoup as bs
import time
import os
from urllib import urlretrieve

def CrawerContent(source,directory):
    res = requests.get(source)
    soup = bs(res.content,from_encoding="utf8")
    div = soup.find_all('div',attrs={'class':'view photo-list-photo-view requiredToShowOnServer photostream awake'})
    for item in div:
        urltemp = item.get('style').split('url(//')
        PicSource = 'https://'+urltemp[1].replace('_n.','_z_d.').rstrip(')')
        RetrievePic(PicSource,directory)
    
def RetrievePic(PicSource,directory):
    picname = PicSource.lstrip('https://').split('/')
    SavePath =directory+'/'+picname[3]
    print SavePath
    urlretrieve(PicSource,SavePath)
    print 'Capture img from : '+PicSource

def getPage(Source,directory):
    PageNum=[]
    Linklist=[]
    res = requests.get(Source)
    print Source
    soup = bs(res.content,from_encoding="utf8")
    div =soup.find('div',attrs={'class':'view pagination-view requiredToShowOnServer photostream'})
    a = div.find_all('a')    
    for tag in a:
        temp = tag.get('href').split('/')
        PageNum.append(int(temp[3].strip('page')))
    
    for i in range(min(PageNum),max(PageNum)+1):
        PageLink =Source+'/page'+str(i)
        Linklist.append(PageLink)
        
    for source in Linklist:
        CrawerContent(source,directory)
        time.sleep(3)

def main():    
    t1 = time.time()
    linklist = open('/home/cylin/Code/Flickr/list.txt')    
    savefolder = '/home/cylin/Code/Flickr/Pic/'
    for link in linklist:
        if link != '\n':
            PhotoId= link.rstrip('\n').lstrip('https://').split('/')
            directory = savefolder + PhotoId[2]
            if not os.path.exists(directory):
                os.makedirs(directory) 
            getPage(link.strip('\n'),directory)
            
    t2 = time.time()
    print 'Time Cost : ',t2-t1

if __name__=='__main__':
    main()



# In[35]:

import requests
from bs4 import BeautifulSoup as bs
import time
import os
from urllib import urlretrieve


def main():
    #link = 'https://www.flickr.com/photos/116866675@N07/'
    link = 'https://www.flickr.com/photos/pt0313/14666153666/in/dateposted/'
    res = requests.get(link)
    soup = bs(res.content,from_encoding='utf8')
    
    print soup
    

if __name__=='__main__':
    main()

