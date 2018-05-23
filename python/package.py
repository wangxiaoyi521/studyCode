#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import time
import subprocess

try:
    buildUserName = sys.argv[1]
    jrePath = sys.argv[2]
    zetaPath = sys.argv[3]
    gitUser = sys.argv[4]
    gitPwd = sys.argv[5]
    gitTagVersion = sys.argv[6]
except IndexError:
    print("该脚本实现在当前用户目录下,自动下载并构建zeta的工作。")
    print("USAGE: python build.py build_user  JRE_PATH  ZETA_DIR  git_user  git_passwd  tag_num")
    print("示例：  python package.py  fexo  /home/jre.zip  /home/fexo  wangxy  Sun55kong  3.0.0.5")
    print("或：  ./package.py  fexo  /home/jre.zip  /home/fexo  wangxy  Sun55kong  3.0.0.5")
    print("参数说明：")
    print("build_user 用户的名字，一般这个用户没有密码  fexo")
    print("JRE_PATH 打包依赖的jre路径  /home/jre.zip")
    print("ZETA_DIR 打包到什么路径下  /home/bulid_user/zate")
    print("git_user  git下载代码的用户名")
    print("git_passwd  git下载代码的用户密码")
    print("tag_num git打包的TAG版本号")
    sys.exit()

# 检查系统是否有jre.zip
if not os.path.isfile(jrePath):
    print(jrePath + "不存在")
    sys.exit()

# git --version  查看当前linux 系统是否安装git
result = os.popen("git --version")
if not result.read()[:11] == "git version":
    print("请给系统安装git")
    sys.exit()

# 如果指定路径下zeta目录存在，则重命名文件，,若不存在创建该目录
if os.path.exists(zetaPath + "/zeta"):
    os.rename(zetaPath + "/zeta", zetaPath + "/zeta" + time.strftime("%Y%m%d%H%M%S", time.localtime()))

os.chdir(zetaPath)
os.system("pwd")

# git 下载文件 并切换到指定tag
os.system("git clone http://" + gitUser + ":" + gitPwd + "@gitlab.raysdata-lab.com/DK/zeta.git")

# 解压Jre
os.system("nohup unzip " + jrePath + " -d " + zetaPath + "/zeta &")

os.chdir("zeta")
os.system("pwd")
os.system("git checkout " + gitTagVersion)
os.chdir("lib")
os.system("pwd")
os.system("./install_jar.sh ")
os.chdir("..")
os.system("pwd")

# maven  打包
os.popen("mvn clean package")
