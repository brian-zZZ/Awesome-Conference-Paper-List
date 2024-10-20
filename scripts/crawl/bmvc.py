import re
import os
from joblib import Parallel, delayed
from bs4 import BeautifulSoup
import requests
from collections import Counter
from base import Crawl


class BMVC(Crawl):
    def __init__(self, year, link) -> None:
        super().__init__()
        self.year = year
        self.link = link
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                         'Accept-Language': 'zh-CN,zh;q=0.9',  # 设置接受的语言，这里设置为中国地区
                         'Accept-Encoding': 'gzip, deflate',  # 指定编码方式
                         'Connection': 'keep-alive',  # 维持持久连接
                         'Upgrade-Insecure-Requests': '1',  # 表示客户端希望从HTTP升级到HTTPS
                    }

    def parse(self):
        res = requests.get(self.link, headers=self.headers)
        soup = BeautifulSoup(res.content.decode(), features='lxml')
        ps = soup.find('table', class_='table')

        paper_group = ps.find_all('tr')
        for g in paper_group:
            if len(g) == 1:
                continue

            title = g.find_all('td')[1].strong.get_text().strip()
            refs = g.find_all('a')

            oral = None

            attrs = {}
            for r in refs:
                ctt = r.get_text()
                if ctt in {'Paper', 'Supplemental', 'Code'}:
                    rurl = r.attrs['href']
                elif 'Poster Session' in ctt:
                    continue
                elif 'Oral Session' in ctt:
                    oral = 'Oral'
                    continue
                else:
                    print('ignore', ctt, f'of {r}')
                    continue
                attrs[ctt] = rurl

                if ctt == 'Paper':
                    self.append_download_item(self.year, title, rurl)

            self.append_item(self.year, title, attrs, type=oral)



BMVC('2023',
     "https://proceedings.bmvc2023.org/"
     ).start()

BMVC('2022',
     "https://bmvc2022.mpi-inf.mpg.de/"
     ).start()

BMVC('2021',
     "https://www.bmvc2021-virtualconference.com/programme/accepted-papers/"
     ).start()

BMVC('2021',
     "https://www.bmvc2021-virtualconference.com/programme/accepted-papers/"
     ).start()

BMVC(
    '2020',
    "https://www.bmvc2020-conference.com/programme/accepted-papers/").start()
