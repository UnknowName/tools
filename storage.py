#!/bin/env python
#coding:utf8

from django.conf import settings
from django.core.files.storage import Storage
import oss2
import time


class AliOSS(Storage):
    def __init__(self,option=None):
        if not option:
            self.endpoint = settings.OSS_ENDPOINT
            self.bucket_name = settings.OSS_BUCKET_NAME
            self.key = settings.OSS_KEY
            self.secret = settings.OSS_SECRET
            self.auth = oss2.Auth(self.key,self.secret)
            self.bucket = oss2.Bucket(self.auth,self.endpoint,self.bucket_name)
            #print 'init sucess'
    def _open(self):
        return self.bucket


    def _save(self,name,content):
        "Upload the file to AliOSS,content is a file object"
         self.bucket.put_object(name,content)
         return name


    def get_valid_name(self,name):
        "Return the file name to get_available_name func"
        file_time = time.strftime('%Y%m%d%H%M%S',time.localtime())
        return  '{file_time}_{origin_name}'.format(file_time=file_time,origin_name=name)


        
    def get_available_name(self,name,max_length=100):
        "Return the file name to _save func"
        return name.split('/')[-1]

