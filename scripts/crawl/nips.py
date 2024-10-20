import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from urllib.parse import urljoin
from collections import Counter
from base import Crawl

YEAR_THRESH = 2023

class NIPS(Crawl):
    def __init__(self):
        super().__init__()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                         'Accept-Language': 'zh-CN,zh;q=0.9',  # 设置接受的语言，这里设置为中国地区
                         'Accept-Encoding': 'gzip, deflate',  # 指定编码方式
                         'Connection': 'keep-alive',  # 维持持久连接
                         'Upgrade-Insecure-Requests': '1',  # 表示客户端希望从HTTP升级到HTTPS
                    }

    def parse(self):
        root = "https://papers.nips.cc/"
        res = requests.get(root, headers=self.headers)
        soup = BeautifulSoup(res.content.decode(), features="lxml")
        lists = soup.find('div', class_='col-sm').find_all('a')
        match_year = re.compile('([0-9]{4})')
        for item in tqdm(lists):
            link = urljoin(root, item.attrs['href'])
            year = match_year.search(item.get_text()).group()
            if int(year) < YEAR_THRESH:
                continue
            res = requests.get(link, headers=self.headers)
            content = res.content.decode()
            soup = BeautifulSoup(content, features="lxml")
            ps = soup.find('div', class_='container-fluid').find_all('li')

            for item in ps:
                item = item.a
                link = item.attrs["href"]
                if 'http' not in link:
                    link = urljoin(root, link)
                # pdf_link = link.replace('Abstract.html', 'Paper.pdf').replace('hash','file')
                # link : https://papers.nips.cc/paper_files/paper/2023/hash/00dada608b8db212ea7d9d92b24c68de-Abstract-Datasets_and_Benchmarks.html
                # pdf: https://papers.nips.cc/paper_files/paper/2023/file/00dada608b8db212ea7d9d92b24c68de-Paper-Datasets_and_Benchmarks.pdf
                pdf_link = link.replace('hash','file').replace('Abstract', 'Paper').replace('html', 'pdf')
                title = item.get_text().strip()
                self.append_item(year,
                                 title,
                                 attrs={'link': link, 'pdf': pdf_link})
                self.append_download_item(year, title, pdf_link)


NIPS().start()
