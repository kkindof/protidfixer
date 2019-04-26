# -*- coding: utf-8 -*-
#用于给proto文件修复id值或者添加id值
#目前修复标准为 行内包含 以下3个串，同时包含分号 "optional ", "required ", "repeated "

import os
import sys
import time
import MySQLdb
import traceback

import thread
import shutil
import json

import traceback
from datetime import date
import datetime


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def fix(file):
    file =os.path.abspath(file)

    if not os.path.exists(file):
        print file,'is not a file'
        return  0
    a = os.path.splitext(file)


    t = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime())
    newpath = a[0]+str(t)+a[1]
    print newpath
    fp  = open(file)
    id=1
    typelist=["optional ", "required ", "repeated "]
    content =""
    for l in fp:

        if l.startswith("message "):
          id = 1

        if l.find(";")==-1:
            content = content+l
            continue

        if l.strip().startswith("//"):

            content = content+l
            continue

        found =0
        for t in typelist:

            if l.strip().startswith(t):
                found=1
                break

        if not found :
            content = content+l
            continue

        pos = l.find(";")
        pos2 = l.find("=",0,pos)
        left = l[0:pos]
        if pos2!=-1:
            left=l[0:pos2]
        sid = "="+str(id)

        newline = left+sid+l[pos:]

        content = content+newline
        id = id + 1
    open(newpath,"w").write(content)
    print 'new file', newpath
if len(sys.argv)!=2:
    print 'par is missing'
    sys.exit(0)

fix(sys.argv[1])
