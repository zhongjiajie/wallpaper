#!/usr/bin/env python
# -*- coding:utf-8 -*-

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

from docopt import docopt

from wallpaper import WallPaper

__version__ = 'wallpaper v0.2'


def main():
    args = docopt(__doc__, version=__version__)
    kwargs = {
        'url': 'http://www.socwall.com/',
        'num': args['--num'],
        'size': args['--size'],
        'path': args['--path'],
        'timeout': args['--timeout'],
        'max_retry_time': args['--retry_time']
    }

    wp = WallPaper(**kwargs)
    wp.parse()


if __name__ == '__main__':
    main()
