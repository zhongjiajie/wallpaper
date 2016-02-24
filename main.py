# -*- coding:utf-8 -*-
'''
多线程，防止网络阻塞（有超时），伪装IE , 无休眠 ，记录时间 ， 爬数据库
'''
import requests
import re
import time
from multiprocessing.dummy import Pool as ThreadPool

#从数据库中获取所有图片的URL并生成列表
def GetPictureUrl():
    #访问网站的数据库，并获取相应的html
    url1 = 'http://www.socwall.com/images/wallpapers/'
    html1 = requests.get(url1).text

    #正则表达求出相应的图片链接
    content1 = re.search('<a href="/views/images/">(.*?)<a href="staging/">',html1,re.S).group(1)
    content2 = re.findall('<a href="(.*?)">',content1,re.S)

    #生成网页列表
    UrlList = []
    for each in content2:
        url2 = 'http://www.socwall.com/images/wallpapers/' + each
        UrlList.append(url2)
    return UrlList

#模拟IE下载图片
def DownloadPicture(url):
    try:
        head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        html = requests.get(url,headers = head,timeout = 40)      #模拟IE下载，40s超时退出
        with open(r'E://picture2//%s'%url[41:], 'wb+') as f:
            f.write(html.content)
    except:
        with open(r'failure_url.txt','a') as f:
            f.write(url + '\n')
        print 'download ' + url + ' failure!'

if __name__ == '__main__':
    time1 = time.time()             #记录开始的时间time1
    UrlList = GetPictureUrl()       #获取图片的URL

    pool = ThreadPool(4)            #开四线程
    results = pool.map(DownloadPicture, UrlList)   #多线程下载
    pool.close()
    pool.join()
    time2 = time.time()             #记录结束时间time2
    print u'合计耗时： ' + str(time2 - time1)        #计算耗时量