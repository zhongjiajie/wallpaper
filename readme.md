# wallpaper
wallpaper是一个通过爬虫获取桌面壁纸的程序，从[Social Wallpapering](http://www.socwall.com/)中指定数量、大小的壁纸到指定目录

## 使用方法

### 安装依赖
wallpaper项目根目录运行
```shell
pip install -r requirements.txt
```
* ps: 本来打算该项目都用Python2.7原生模块，减少相关依赖，但是在写cmd解析参数的时候用[docopt](https://github.com/docopt/docopt)真是爽得不要不要，所以目前这是用的唯一一个第三方库

### Usage
```
"""Usage:
  download_wp.py [-n=<num>] [-s=<size>] [-t=<timeout>] [-r=<max_retry_time>] [-p=<path>]
  download_wp.py (--help | -h)

Options:
  --help -h                     Show this screen.
  --num -n=<num>                Number of picture to download, default 10.
  --size -s=(size)              Size of download picture, `small` or `big`, default `small`.
  --timeout -t=<timeout>        Timeout of request, default 60.
  --retry_time -r=<retry_time>  Max Retry Time of request, default 3.
  --path -p=<path>              Path to download picture, default `$project/pic/`.
"""
```
进入wallpaper项目目录，运行
```python
python download_wp.py [your select from Usage]
```
进行相应的下载操作

## Features
* 用了Python2.7的原生模块完成HTTP访问及异常处理
* 自定义下载图片的数据及大小

## 目录结构
```shell
│ download_wp.py
└─wallpaper
     user_agents.py
     wallpaper.py
     __init__.py
```
* `download_wp.py`: 程序调用，包含了**Usage**信息
* `./wallpaper/user_agents.py`: user agent模块，存放了UA常量
* `./wallpaper/wallpaper.py`: 程序主模块，包含了访问[Social Wallpapering](http://www.socwall.com/)、下载图片数量、下载大小图、下载路径、timeout等方法

## TODO
* [x] 通过cmd命令行来运行
* [x] 默认下载在项目根目录并以`pic`做文件名
* [x] 全部换成内置库
* [ ] 异常处理
* [ ] 查看能不能python调用调用win的设置自动桌面壁纸

## Change Log
* 20170820: 重写了repository，重命名为**wallpaper**，用了Python2.7原生的库完成了主程序设计
* 20160224: 完成了第一版本爬虫，用了`requests`完成HTTP访问，`re`完成提取操作，`multiprocessing`完成多线程操作。该版本直接访问[Social Wallpapering](http://www.socwall.com/)的[文件服务器](www.socwall.com/images/wallpapers/)中爬取图片
