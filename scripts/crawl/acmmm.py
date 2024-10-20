import re
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
from collections import Counter
from base import Crawl, COLLECTION_ROOT
from urllib.parse import urljoin


class ACMMM(Crawl):
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
        year = self.year
        res = requests.get(self.link, headers=self.headers)
        soup = BeautifulSoup(res.content.decode(), features='lxml')
        sessions = [i for i in soup.find_all(
            'a', class_='section__title') if i.attrs['href'] != '#']
        for session in tqdm(sessions):
            res = requests.get(urljoin(
                "https://dl.acm.org/doi/proceedings/10.1145/3503161", session.attrs['href']), headers=self.headers)
            soup = BeautifulSoup(res.content.decode(), features='lxml')
            session_name = re.search(
                'SESSION:(.*)', session.get_text()).group(1).lower().strip().replace(' ', '_')
            session_name = re.sub('[-+:_]+', '_', session_name)
            r = soup.find('a', id=session.attrs['id'])
            items = r.find_parent().find_all('h5', 'issue-item__title')
            for item in items:
                title = item.get_text()
                link = item.a.attrs['href']
                link = urljoin(self.link, link)
                self.append_item(year, title,
                                 attrs={'link': link, 'group': session_name})


# ACMMM('2023', 'https://dl.acm.org/doi/proceedings/10.1145/3581783').start()
ACMMM('2022', 'https://dl.acm.org/doi/proceedings/10.1145/3503161').start()
ACMMM('2021', 'https://dl.acm.org/doi/proceedings/10.1145/3474085').start()
ACMMM('2020', 'https://dl.acm.org/doi/proceedings/10.1145/3394171').start()
ACMMM('2019', 'https://dl.acm.org/doi/proceedings/10.1145/3343031').start()
ACMMM('2018', 'https://dl.acm.org/doi/proceedings/10.1145/3240508').start()
