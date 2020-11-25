import scrapy
import re
from testYymp3.items import TestYymp3Item
from scrapy.utils.project import get_project_settings
import os


class Yymp3Spider(scrapy.Spider):
    name = 'yymp3'
    allowed_domains = ['yymp3.com']
    start_urls = ['http://www.yymp3.com/top/top_7.html']
    mp3showurl = 'http://www.yymp3.com'
    mp3url = 'http://ting6.yymp3.net:82/'
    settingarr = get_project_settings()
#    print(settings.get('FILES_STORE'))

    # def start_requests(self):
    #     cookies = "guid=2539513a0f2634db21f7d59dfbfba94a; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; _ujz=MTY4Njg2NjU4MA%3D%3D; slife=lastvisit%3D010000%26%7C%26lowbrowser%3Dnot%26%7C%26lastlogindate%3D20201123%26%7C%26securetime%3DADwBNAJkAGADZAQ%252BATtdMwczAjA%253D; ps=needv%3D0; 51job=cuid%3D168686658%26%7C%26cusername%3Dphone_13522593742_202002233263%26%7C%26cpassword%3D%26%7C%26cname%3D%25C0%25EE%25BA%25A3%25C1%25BC%26%7C%26cemail%3D914777535%2540qq.com%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0zzcOG9GRvlU%26%7C%26cconfirmkey%3D91S%252FL3RG73Jac%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D91GExDavPg5iY%26%7C%26to%3Df068412c4a39a93386ba68246889f56f5fbb4b70%26%7C%26; search=jobarea%7E%60010000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAphp%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAPHP%BF%AA%B7%A2%B9%A4%B3%CC%CA%A6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA07%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAphp%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60010000%A1%FB%A1%FA010200%A1%FB%A1%FA0100%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0100%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21collapse_expansion%7E%601%7C%21"
    #     '''转化为字典的形式'''
    #     cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
    #     yield scrapy.Request(
    #         self.start_urls[0],
    #         callback=self.parse,
    #         cookies=cookies  # 设置cookie参数
    #     )

    def parse(self, response):

        r = response.xpath("//ul[@class='list_rank c']//a")
        for re in r:
            url = self.mp3showurl + re.xpath("./@href").get()
            yield scrapy.Request(
            url,
            callback=self.parse_detial
        )

    def parse_detial(self, response):
        res = re.findall(r'\[0\]="(.*)\|\|";',response.text)
        item = TestYymp3Item()
        if len(res) > 0:
            content = res[0].split('|')
            item['title'] = content[1]
            item['author'] = content[3]
            ##判断文件是否已经下载过
            file_name = '{}-{}'.format(item['title'], item['author']) + '.mp3'
            filePath = self.settingarr.get('FILES_STORE')
            if(os.path.exists(filePath + '\\' + file_name)):
                print("文件存在:",file_name)
                return

            item['file_urls'] = self.mp3url + content[4].replace('wma','mp3')
            yield item




