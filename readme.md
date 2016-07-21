# crawler-photo
Python爬虫，获取www.socwall.com上面的图片

#主要应用了requests,re,multiprocessing模块
特点为：多线程，防止网络阻塞（有超时），伪装IE , 无休眠 ，记录时间 ， 爬数据库

发现了www.socwall.com服务器的公共数据库为www.socwall.com/images/wallpapers/
所以直接访问该数据库，然后发现了该数据没有对爬虫进行处理，直接用无休眠的多线程爬虫进行爬取
