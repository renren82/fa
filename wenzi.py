#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
利用百度api实现图片文本识别
author: renxh
pip install baidu-aip
"""

import glob
from os import path
import os
from aip import AipOcr


def baiduOCR(picfile, outfile):
    """利用百度api识别文本，并保存提取的文字
    picfile:    图片文件名
    outfile:    输出文件
    """
    filename = path.basename(picfile)

    APP_ID = '22652610'  # 刚才获取的 ID，下同
    API_KEY = 'vUw68G6gbvk5Pt28OWKqTlzN'
    SECRECT_KEY = 'xLlidrS2MtY8wZgL9L71LtmSuQkhR3I9'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)

    i = open(picfile, 'rb')
    img = i.read()
    print("正在识别图片：\t" + filename)
    # message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费
    message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费
    print("识别成功！")
    i.close();

    with open(outfile, 'a+') as fo:
        fo.writelines("+" * 60 + '\n')
        fo.writelines("识别图片：\t" + filename + "\n" * 2)
        fo.writelines("文本内容：\n")
        # 输出文本内容
        for text in message.get('words_result'):
            fo.writelines(text.get('words') + '\n')
        fo.writelines('\n' * 2)
    print("文本导出成功！")
    print()


if __name__ == "__main__":

    outfile = 'h:/picture/export.txt'

    if path.exists(outfile):
        os.remove(outfile)

    print("图片识别...")
    for picfile in glob.glob("h:/picture/*"):
        baiduOCR(picfile, outfile)
        os.remove(picfile)
    print('图片文本提取结束！文本输出结果位于 %s 文件中。' % outfile)
