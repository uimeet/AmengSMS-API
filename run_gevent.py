# coding=utf-8

#import gevent.monkey
#import gevent_psycopg2

from setup import bm

#gevent.monkey.patch_all()
#gevent_psycopg2.monkey_patch()

application = bm.wsgifunc()
