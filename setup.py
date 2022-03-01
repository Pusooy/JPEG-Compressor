# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

'''
compressed #压缩
bundle_files #所有文件打包成一个exe文件
'''
options = {"py2exe":{"compressed":1,"optimize":2,"bundle_files":1}}

'''
version #版本号
description #类似于打开任务管理器后，后边的进程描述。这里自己可以定义自己的名称
name #作者
options #将所有文件打包成一个exe,如果无此代码则会在dist文件夹内生成许多依赖的文件，加上此代码则会把依赖文件都加入一个exe，发给他人使用时不
script、icon_resources #前一个参数都好理解是你的python文件名，后一个参数就是图标所依赖的资源文件，只需要给出合理的ico图标路径
'''
setup(
    version='1.0',
    description='a JPEG Commpressor',
    name='TrumpHe',
    options=options,
    zipfile=None,
    windows=[{'script':'GUI.py','icon_resources':[(1,r'E:\Download\jpeg-encoder-master\jpeg-encoder-master\favicon.ico')]}]
)
