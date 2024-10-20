import re
import os
from joblib import Parallel, delayed
from bs4 import BeautifulSoup
import requests
from collections import Counter
from urllib.parse import urljoin
from base import Crawl

def iter_paper(c):
    tmp = []
    for i in c:
        if i.name == 'dt':
            yield tmp
            tmp = []
        if i != '\n':
            tmp.append(i)
    yield tmp


class CVPR(Crawl):
    def __init__(self, year, links) -> None:
        super().__init__()
        self.year = year
        self.links = links
    
    def parse(self):
        root = 'https://openaccess.thecvf.com/'
        for link in self.links:
            res = requests.get(link)
            content = res.content.decode()
            soup = BeautifulSoup(content, features="lxml")
            paper_group = list(iter_paper(soup.dl.children))
            for g in paper_group:
                if len(g) == 0 or len(g) == 1 or g[0].name != 'dt':
                    continue

                href = g[0].a

                title = href.get_text().strip()
                url = urljoin('https://openaccess.thecvf.com/',
                              href.attrs['href'])

                attrs = {'link': url}
                refs = g[2].find_all('a')
                rres = [f'[[link]({url})]']
                for r in refs:
                    ctt = r.get_text()
                    if ctt in {'pdf', 'supp'}:
                        rurl = urljoin(root, r.attrs['href'])
                    elif ctt in {'arXiv', 'video', 'dataset'}:
                        rurl = r.attrs['href']
                    elif ctt in {'bibtex'}:
                        continue
                    else:
                        print('ignore', ctt, f'of {r}')
                        pass
                    
                    if ctt == 'pdf':
                        self.append_download_item(self.year,title,rurl)
                    attrs[ctt] = rurl
                self.append_item(self.year, title, attrs=attrs)
                rres = ' '.join(rres)



# CVPR('2024', [
#     'https://openaccess.thecvf.com/CVPR2024?day=2024-06-19',
#     'https://openaccess.thecvf.com/CVPR2024?day=2024-06-20',
#     'https://openaccess.thecvf.com/CVPR2024?day=2024-06-21',
# ]).start()

# CVPR('2023', [
#     'https://openaccess.thecvf.com/CVPR2023?day=2023-06-20',
#     'https://openaccess.thecvf.com/CVPR2023?day=2023-06-21',
#     'https://openaccess.thecvf.com/CVPR2023?day=2023-06-22',
# ]).start()
        
# CVPR('2022', [
#     'https://openaccess.thecvf.com/CVPR2022?day=2022-06-21',
#     'https://openaccess.thecvf.com/CVPR2022?day=2022-06-22',
#     'https://openaccess.thecvf.com/CVPR2022?day=2022-06-23',
#     'https://openaccess.thecvf.com/CVPR2022?day=2022-06-24',
# ]).start()

# CVPR('2021', [
#     'https://openaccess.thecvf.com/CVPR2021?day=2021-06-21',
#     'https://openaccess.thecvf.com/CVPR2021?day=2021-06-22',
#     'https://openaccess.thecvf.com/CVPR2021?day=2021-06-23',
#     'https://openaccess.thecvf.com/CVPR2021?day=2021-06-24',
#     'https://openaccess.thecvf.com/CVPR2021?day=2021-06-25',
# ]).start()

# CVPR('2020', [
#     'https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-16',
#     'https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-17',
#     'https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-18',
# ]).start()

# CVPR('2019', [
#     'https://openaccess.thecvf.com/CVPR2019.py?day=2019-06-18',
#     'https://openaccess.thecvf.com/CVPR2019.py?day=2019-06-19',
#     'https://openaccess.thecvf.com/CVPR2019.py?day=2019-06-20',
# ]).start()

CVPR('2018', [
    'https://openaccess.thecvf.com/CVPR2018.py?day=2018-06-19',
    'https://openaccess.thecvf.com/CVPR2018.py?day=2018-06-20',
    'https://openaccess.thecvf.com/CVPR2018.py?day=2018-06-21',
]).start()

CVPR('2017', [
    'https://openaccess.thecvf.com/CVPR2017',
]).start()

CVPR('2016', [
    'https://openaccess.thecvf.com/CVPR2016',
]).start()

CVPR('2015', [
    'https://openaccess.thecvf.com/CVPR2015',
]).start()