import scrapy
from liuliangSpider.items import LiuliangspiderItem
import itertools

class LiuliangSpider(scrapy.Spider):
    name = 'liuliang'
    '''
    Hide to avoid trouble
    '''
    allowed_domains = ["xxx.cn"]
    start_urls = ['https://www.xxx.cn/xx/liuliang/']

    def info_gather(self, list_1, list_2, list_3):
        list_0 = []
        list_0.extend(list_1)
        list_0.extend(list_2)
        list_0.extend(list_3)
        return list_0

    def info_gather_2(self, list_tmp):
        return list(itertools.chain(*list_tmp))


    def parse(self, response, **kwargs):

        print("Start parse ...")

        rep = response.xpath('.//*[@id="totop"]')

        pkg_sort_tmp = []
        pkg_url_tmp = []
        pkg_title_tmp = []

        '''
        job
        '''
        jobPackages = rep.xpath('.//*[@class="wrap"]')
        job_pkg_url = jobPackages.xpath('.//*[@class="content-slide"]/a/@href').extract()
        job_pkg_title = jobPackages.xpath('.//*[@class="sw_l"]/p[@class="sw_wz_01"]/text()').extract()
        job_pkg_sort  = ['job'] * len(job_pkg_url)
        pkg_sort_tmp.append(job_pkg_sort)
        pkg_url_tmp.append(job_pkg_url)
        pkg_title_tmp.append(job_pkg_title)


        '''
        myVIP
        '''
        myVIPPackages = rep.xpath('.//*[@class="wdzx"]')
        # print(myVIPPackages)
        myvip_pkg_url = myVIPPackages.xpath('.//li[@class="wdzx_li"]/a/@href').extract()
        myvip_pkg_title = myVIPPackages.xpath('.//*[@class="wdzx_l"]/p[@class="wdzx_4G"]/text()').extract()
        myVIP_pkg_sort  = ['myVIP'] * len(myvip_pkg_url)
        pkg_sort_tmp.append(myVIP_pkg_sort)
        pkg_url_tmp.append(myvip_pkg_url)
        pkg_title_tmp.append(myvip_pkg_title)

        '''
        regularUser
        '''
        regularUserPackages = rep.xpath('.//*[@class="lyhzx"]')
        # print(regularUserPackages)
        regularUser_pkg_url = regularUserPackages.xpath('.//li[@class="wdzx_li lyhzx_li"]/a/@href').extract()
        regularUser_pkg_title = regularUserPackages.xpath('.//*[@class="wdzx_l"]/p[@class="wdzx_4G"]/text()').extract()
        regularUser_pkg_sort  = ['regularUser'] * len(regularUser_pkg_url)
        pkg_sort_tmp.append(regularUser_pkg_sort)
        pkg_url_tmp.append(regularUser_pkg_url)
        pkg_title_tmp.append(regularUser_pkg_title)

        '''
        highlights
        '''
        highlightsPackages = rep.xpath('.//*[@class="llbjc"]')
        # 流量包_01
        pkg_highlights_01_url = highlightsPackages.xpath('.//*[@class="llbjc_01"]/li[@class="llbjc_li"]/a/@href').extract()
        pkg_highlights_01_title = highlightsPackages.xpath('.//*[@class="llbjc_01"]/li[@class="llbjc_li"]/a/p[@class ="b_4G"]/text()').extract()
        pkg_highlights_01_sort = ['highlights'] * len(pkg_highlights_01_url)
        pkg_sort_tmp.append(pkg_highlights_01_sort)
        pkg_url_tmp.append(pkg_highlights_01_url)
        pkg_title_tmp.append(pkg_highlights_01_title)

        pkg_highlights_03_url = highlightsPackages.xpath('.//*[@class="jc_03_ul"]/li[@class="jc_03_li"]/a/@href').extract()
        pkg_highlights_03_title = highlightsPackages.xpath('.//*[@class="jc_03_li"]/a/p[@class="jc_03_li_p"]/text()').extract()
        pkg_highlights_03_sort = ['highlights'] * len(pkg_highlights_03_url)
        pkg_sort_tmp.append(pkg_highlights_03_sort)
        pkg_url_tmp.append(pkg_highlights_03_url)
        pkg_title_tmp.append(pkg_highlights_03_title)

        pkg_sort = self.info_gather_2(pkg_sort_tmp)
        pkg_url = self.info_gather_2(pkg_url_tmp)
        pkg_title = self.info_gather_2(pkg_title_tmp)

        for i in range(len(pkg_url)):

            if pkg_title[i] != "All":

                item = LiuliangspiderItem(pkg_sort=pkg_sort[i], pkg_url=pkg_url[i], pkg_title=pkg_title[i])
                # yield item
                request = scrapy.Request(url=pkg_url[i], callback=self.parse_pkg_detail)
                request.meta['item'] = item

                yield request
            else:
                '''
                Jump to another page
                '''
                pass


    def parse_pkg_detail(self, response):
        # pass
        item = response.meta['item']
        pkg_detail = response.xpath(".//body")
        pkg_img_url = pkg_detail.xpath('.//li[@id="sibphoto1"]/img//@src').extract() # 提取套餐图片链接

        tmp_pkg_img_url = []
        tmp_pkg_img_url.extend(pkg_img_url)

        pkg_full_title = pkg_detail.xpath('.//*[@class="main_title"]/text()').extract()
        pkg_price = pkg_detail.xpath('.//span[@class="font_size_red"]/text()').extract()
        pkg_flow_size = pkg_detail.xpath('.//*[@class="selected"]/a/span[@class="ggz_text"]/text()').extract()
        pkg_content = pkg_detail.xpath('.//*[@id="tabcontent4"]/div/p/text()').extract()

        tmp = "".join(pkg_content)
        tmp_pkg_content = []
        tmp_pkg_content.append(tmp)


        item['pkg_full_title'] = pkg_full_title[0]
        item['pkg_price'] = pkg_price[0]
        item['pkg_flow_size'] = pkg_flow_size[0]
        item['pkg_content'] = tmp_pkg_content[0]

        item['pkg_image_urls'] = tmp_pkg_img_url

        yield item


