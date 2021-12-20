# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import json
from scrapy.exceptions import DropItem
import csv
import os
import codecs
import numpy as np

this_directory = os.getcwd()
parent_directory = os.path.dirname(os.getcwd())


class LiuliangspiderPipeline:
    # def process_item(self, item, spider):
    #     return item

    def __init__(self):

        DATAPATH = this_directory + "/DB/csv/liuliang-63.csv"
        if os.path.exists(DATAPATH):  # 判断数据文件是否存在
            df_old = pd.read_csv(DATAPATH)
            df_old.to_csv("./DB//update/update_old.csv", encoding="utf-8-sig", mode="w",
                           index=False)
        else:
            pass

        # json
        self.file = open('./DB/liuliang.json', 'wb')

        # csv
        self.df = pd.DataFrame(columns=['pkg_sort', 'pkg_url', 'pkg_title', 'pkg_full_title', 'pkg_price', 'pkg_flow_size', 'pkg_content', 'pkg_image_urls', 'pkg_images'])
        self.df.to_csv("./DB//csv/liuliang-63.csv", encoding="utf-8-sig", mode="w", index=False) # mode='w', 覆盖原数据；mode='a'，便可以追加写入数据

        self.update_df = pd.DataFrame(columns=['pkg_sort', 'pkg_url', 'pkg_title', 'pkg_full_title', 'pkg_price', 'pkg_flow_size', 'pkg_content', 'pkg_image_urls', 'pkg_images'])
        self.df.to_csv("./DB//update/update.csv", encoding="utf-8-sig", mode="w", index=False)


    def update_info(self, item):
        '''
        Verify if there is data update
        '''


        DATAPATH_old = this_directory + "/DB/update/update_old.csv"

        if os.path.exists(DATAPATH_old):
            df_old = pd.read_csv(DATAPATH_old)
            # os.remove(DATAPATH_old)
        else:
            df_old = pd.DataFrame(
                columns=['pkg_sort', 'pkg_url', 'pkg_title', 'pkg_full_title', 'pkg_price', 'pkg_flow_size',
                         'pkg_content', 'pkg_image_urls', 'pkg_images'])


        df_new = pd.DataFrame.from_dict(item, orient='index').T

        # Compared
        slice_lable = (
            df_new[['pkg_url', 'pkg_full_title']].apply(tuple, axis=1)
                .isin(df_old[['pkg_url', 'pkg_full_title']].apply(tuple, axis=1)
                      .to_list()
                      )
        )

        df_update = df_new[~slice_lable]
        if df_update.empty:
            pass
        else:
            df_update.to_csv("./DB/update/update.csv", encoding="utf-8-sig", mode="a", header=False,
                      index=False)



    def save_csv_file(self, data):

        '''
        # method 1：
        list_1 = list(data.values())
        df_tmp = pd.DataFrame(list_1).T
        # df_tmp.to_csv("./DB/csv/liuliang-63.csv", encoding="utf-8-sig", mode="a", header=False, index=False)
        df_tmp.to_csv("./DB/csv/liuliang-63.csv", encoding="utf-8-sig", mode="a",header=False,  index=False)
        '''

        # method 2：
        df = pd.DataFrame.from_dict(data, orient='index').T
        df.to_csv("./DB/csv/liuliang-63.csv", encoding="utf-8-sig", mode="a", header=False, index=False)


    def process_item(self, item, spider):
        '''
        :param item:
        :param spider:
        :return:
        '''
        if item['pkg_title']:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line.encode('utf-8'))
            self.save_csv_file(item) #  method 2
            self.update_info(item)

            return item
        else:
            raise DropItem("Missing pkg_title in %s"%item)


    def close_spider(self, spider):
        self.file.close()
        # self.file_cvs.close()



