#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/3/3 11:33
# @Author  : 亦轩
# @File    : 111.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2i
import zipfile
import os
def zipDir(dirpath_list,outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zips = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    filenamelist=[]
    for filepath in dirpath_list:
        filenamelist.append(filepath.split('\\')[-1])
    for filename in filenamelist:
        zips.write(os.path.join('static/file',filename),os.path.join('',filename))
    zips.close()
    print(outFullName)

def zipDirs(dirpath,outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath,'')

        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()

if __name__ == '__main__':
    dirpath_list = [
        r'C:\Users\Administrator\Desktop\project\individual_event\pdf_collect_porject\Paper\static\file\15832272147465403A58d0db2c78s_牡蛎君_重庆新增确诊新冠肺炎病例3例 累计489例.docx',
        r'C:\Users\Administrator\Desktop\project\individual_event\pdf_collect_porject\Paper\static\file\1583227337364272Aab82bfoyxn9_牡蛎君_重庆新增确诊新冠肺炎病例3例 累计489例.docx',
        r'C:\Users\Administrator\Desktop\project\individual_event\pdf_collect_porject\Paper\static\file\158322728388596A58d0db2c78s_牡蛎君_重庆新增确诊新冠肺炎病例3例 累计489例.docx',
    ]
    outfullname= 'static/zipfiles/2222.zip'
    zipDir(dirpath_list,outfullname)