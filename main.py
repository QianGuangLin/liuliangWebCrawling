#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
@Time       : 2021/12/2  17:05
@ Author by : QGLin
@ File      : main.py

@Code Analysis:



"""


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os, re, time
import numpy as np
import pandas as pd
import prettytable as pt

import warnings
warnings.filterwarnings("ignore")

this_directory = os.getcwd()
parent_directory = os.path.dirname(os.getcwd())



# 打印菜单
def menu():
    # print("\n")
    menu_info = '''=================================
      Crawling tool
          A:  start
          B:  display
          C:  update
          D:  Waiting for development
        EXIT: Press any key + <Enter>
================================='''
    print(menu_info)
    # print("\n")


# 爬虫启动
def liuliangCrawlStart():
    # 启动爬虫
    # 可以在CrawlerProcess初始化时传入项目的settings信息，在crawl方法中传入爬虫的名字。
    process = CrawlerProcess(get_project_settings())
    process.crawl('liuliang')
    process.start()


# 显示爬取数据
def showDataInfo():
    DATAPATH = this_directory + "/DB/csv/liuliang-63.csv"
    if os.path.exists(DATAPATH):
        print("显示爬取数据...")
        # 使用 pandas 读取
        df = pd.read_csv(DATAPATH)
        tb = pt.PrettyTable()
        tb.add_column('indexs', df.index)
        for col in df.columns.values:
            tb.add_column(col, df[col])
        print(tb)

    else:
        print("No data file, please go crawl...")

# 更新数据
def updateDataInfo():

    os.system("scrapy crawl liuliang")

    DATAPATH = this_directory + "/DB/update/update.csv"
    # 先判断数据是否存在
    if os.path.exists(DATAPATH):

        df = pd.read_csv(DATAPATH)
        if df.empty:
            print("No data update...")
        else:
            print("Data Update...")

            tb = pt.PrettyTable()
            tb.add_column('indexs', df.index)
            for col in df.columns.values:
                tb.add_column(col, df[col])
            print(tb)

    else:
        print("No data update file...")



if __name__ == "__main__":
    print("hello world")

    while True:
        menu()
        select = input("Please choose an operation:")
        # print("\n")
        if select == 'A' or select == 'a': # A:  Start
            liuliangCrawlStart()
            print("[!] Data crawling completed")
            print("\n")

        elif select == 'B' or select == 'b': # B:  Display
            # pass
            showDataInfo()

        elif select == 'C' or select == 'c': # C:  Update
            updateDataInfo()
            # pass

        elif select == 'D' or select == 'd': # D:  Waiting for development
            pass

        else: # EXIT
            break

