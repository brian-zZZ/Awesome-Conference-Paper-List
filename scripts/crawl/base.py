from joblib import Parallel, delayed
import requests
import os
from collections import Counter
import re


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COLLECTION_ROOT = os.path.join(ROOT, 'collections')
DOWNLOAD_ROOT = os.path.join(ROOT, 'pdfs')


class Crawl:
    def __init__(self) -> None:
        self.dic = {}
        self.download_links = []
        self.conf_name = self.__class__.__name__
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                         'Accept-Language': 'zh-CN,zh;q=0.9',  # 设置接受的语言，这里设置为中国地区
                         'Accept-Encoding': 'gzip, deflate',  # 指定编码方式
                         'Connection': 'keep-alive',  # 维持持久连接
                         'Upgrade-Insecure-Requests': '1',  # 表示客户端希望从HTTP升级到HTTPS
                    }

    def parse(self):
        pass

    def process_title(self, title):
        title = re.sub(r'[/:*<>?|]', '-', title)
        title = re.sub(r"""[\\'"]""", '', title)
        title = re.sub('\s+', ' ', title)
        return title

    def append_item(self, year, title, attrs=None, type=None):
        title = self.process_title(title)
        if type is not None:
            self.dic.setdefault((year, type), []).append([title, attrs])
        else:
            self.dic.setdefault((year, ''), []).append([title, attrs])

    def append_download_item(self, year, title, link):
        title = self.process_title(title)
        self.download_links.append((year, title, link))

    def download(self):
        def req(f, link):
            try:
                r = requests.get(link, headers=self.headers)
                if r.ok:
                    with open(f, 'wb') as w:
                        w.write(r.content)
                else:
                    print("download pdf failed: ", link)
            except Exception as e:
                print(link, e)
                return link

        cand = []
        for year, title, link in self.download_links:
            title = title.strip().lower()
            fdir = os.path.join(DOWNLOAD_ROOT, self.conf_name, year)
            os.makedirs(fdir, exist_ok=True)
            fpath = os.path.join(fdir, f'{title}.pdf')
            if os.path.exists(fpath):
                continue
            cand.append(delayed(req)(fpath, link))
        print(f'Start downloading {len(cand)} papers.')
        Parallel(1, verbose=10)(cand)

    def write(self):
        cc = Counter()
        for k, v in self.dic.items():
            year = k[0]
            k = '_'.join([i for i in k if i is not None]).strip('_')
            res = []
            for i, (title, attrs) in enumerate(v, start=1):
                if attrs is None:
                    # res.append(f'{i}. {title}')
                    res.append(f'{title}')
                else:
                    attrs = ', '.join(
                        [f"[{k}]({v})" for k, v in attrs.items()])
                    # res.append(f'{i}. {title} | {attrs}')
                    res.append(f'{title} | {attrs}')
            cc[year] += len(res)
            os.makedirs(os.path.join(COLLECTION_ROOT, self.conf_name), exist_ok=True)
            fpath = os.path.join(COLLECTION_ROOT, self.conf_name, f'{k}.md')
            with open(fpath, 'a', encoding='utf-8') as w:
                w.write('\n'.join(res))
                print(f' - write {len(res)} papers for {k}.')
        for k, v in cc.items():
            print(f'total {v} papers in {k}.')

    def start_download(self):
        self.parse()
        self.download()

    def start(self):
        print(f'Start crawling for {self.conf_name}')
        self.parse()
        self.write()
        # self.download()
