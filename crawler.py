from datetime import datetime
from time import sleep
import requests
from lxml import etree
import re


class Crawler():
    def __init__(self,
                 base_url='https://www.csie.ntu.edu.tw/news/',
                 rel_url='news.php?class=101'):
        self.base_url = base_url
        self.rel_url = rel_url

    def crawl(self, start_date, end_date,
              date_thres=datetime(2012, 1, 1)):
        """Main crawl API

        1. Note that you need to sleep 0.1 seconds for any request.
        2. It is welcome to modify TA's template.
        """

        if end_date < date_thres:
            end_date = date_thres
        contents = []
        page_num = 0
        while True:
            rets, last_date = self.crawl_page(
                start_date, end_date, page=f'&no={page_num}')
            page_num += 10
            if rets:
                contents += rets
            if last_date < start_date:
                break
        return contents

    def crawl_page(self, start_date, end_date, page=''):
        """Parse ten rows of the given page

        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
            page (str): the relative url specified page num
        Returns:
            contents (list): a list of dictionaries including date, title and content
            last_date (datetime): the smallest date in the page
        """
        res = requests.get(
            self.base_url + self.rel_url + page,
            headers={'Accept-Language':
                     'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode()
        sleep(0.1)

        root = etree.HTML(res)

        rel_urls = root.xpath('//div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/a/@href')
        last_date = None
        contents = []
        for idx, rel_url in enumerate(rel_urls):
            content = {}
            date = root.xpath(f'//div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr[{idx+1}]/td[1]/text()')[0]
            last_date = datetime.strptime(date, "%Y-%m-%d")
            if last_date < start_date or last_date > end_date:
                continue
            content['date'] = date
            title = root.xpath(f'//div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr[{idx+1}]/td[2]/a/text()')[0]

            content['title'] = re.sub("\"", "\"\"", title)
            content_url = self.base_url + rel_url
            content['content'] = self.crawl_content(content_url)
            contents.append(content)
        return contents, last_date

    def crawl_content(self, url):
        """Crawl the content of given url
        Parameters:
            url (str)
        Returns:
            content (str)
        """
        res = requests.get(
            url,
            headers={'Accept-Language':
                     'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode()
        sleep(0.1)
        root = etree.HTML(res)
        content = root.xpath('//div[1]/div/div[2]/div/div/div[2]/div/div[2]//text()')
        content = "".join(content)
        content = re.sub('[\xa0\r\n]', '', content)
        content = re.sub("\"", "\"\"", content)
        return content
