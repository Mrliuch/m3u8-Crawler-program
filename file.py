#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
import urllib.request, urllib.error, requests


# 打开并读取网页内容
def getUrlData(url):
    try:
        urlData = urllib.request.urlopen(url, timeout=3)  # .read().decode('utf-8', 'ignore')
        return urlData
    except Exception as err:
        print(f'err getUrlData({url})\n', err)
        return -1


# 下载文件-urllib.request
def getDown_urllib(url, file_path):
    try:
        urllib.request.urlretrieve(url, filename=file_path)
        return True
    except urllib.error.URLError as e:
        # hasttr(e, 'code')，判断e 是否有.code属性，因为不确定是不是HTTPError错误，URLError包含HTTPError，但是HTTPError以外的错误是不返回错误码(状态码)的
        if hasattr(e, 'code'):
            print(e.code)  # 打印服务器返回的错误码（状态码），如403，404,501之类的
        elif hasattr(e, 'reason'):
            print(e.reason)  # 打印错误原因


def getVideo_urllib(url_m3u8, path, videoName):
    print('begin run ~~\n')
    # urlData = getUrlData(url_m3u8).readlines()
    urlData = getUrlData(url_m3u8)
    num = 0
    tempName_video = os.path.join(path, f'{videoName}.ts')  # f'{}' 相当于'{}'.format() 或 '%s'%videoName
    # print(urlData)
    for line in urlData:
        # 解码，由于是直接使用了所抓取的链接内容，所以需要按行解码，如果提前解码则不能使用直接进行for循环，会报错
        # 改用上面的readlines()或readline()也可以，但更繁琐些，同样需要按行解码，效率更低
        url_ts = line.decode('utf-8')
        tempName_ts = os.path.join(path, f'{num}.ts')  # f'{}' 相当于'{}'.format()
        if not '.ts' in url_ts:
            continue
        else:
            if not url_ts.startswith('http'):  # 判断字符串是否以'http'开头，如果不是则说明url链接不完整，需要拼接
                # 拼接ts流视频的url
                url_ts = url_m3u8.replace(url_m3u8.split('/')[-1], url_ts)
        print(url_ts)
        getDown_urllib(url_ts, tempName_ts)  # 下载视频流
        if num == 0:
            # 重命名，已存在则自动覆盖
            shutil.move(tempName_ts, tempName_video)
            num += 1
            continue
        cmd = f'copy /b {tempName_video}+{tempName_ts} {tempName_video}'
        res = os.system(cmd)
        if res == 0:
            os.system(f'del {tempName_ts}')
            # if num == 20:  # 限制下载的ts流个数，这个视频挺长有四百多个.ts文件，所以限制一下
            #     break
            num += 1
            continue
        print(f'Wrong, copy {num}.ts-->{videoName}.ts failure')
        return False
    os.system(f'del {path}/*.ts')  # 调用windows命令行（即cmd）工具，运行命令
    filename = os.path.join(path, f'{videoName}.mp4')
    shutil.move(tempName_video, filename)
    print(f'{videoName}.mp4 finish down!')


if __name__ == '__main__':
    url_m3u8 = 'http://cntv.hls.cdn.myqcloud.com/asp/hls/2000/0303000a/3/default/e7b1fc31c9af496d85cf647cdffea9db/2000.m3u8'
    path = r'G:\videos'
    videoName = url_m3u8.split('/')[-2]
    getVideo_urllib(url_m3u8, path, videoName)


