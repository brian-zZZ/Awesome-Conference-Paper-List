import fitz  # pip install pymupdf
import requests
import os
from bs4 import BeautifulSoup
import re
from collections import Counter
from base import Crawl


def iter_group(div):
    res = []
    for i in list(div.children):
        if i == '\n':
            continue

        rstr = i.get_text()

        if rstr is not None:
            if re.search(' *[0-9]+:.*', rstr):
                yield ' '.join(res)
                res = []
            elif re.search('[,;()]', rstr):
                continue
            rstr = re.sub('-­‐', '-', rstr)
            res.append(' '.join(rstr.split()))
    yield ' '.join(res)


class AAAI(Crawl):
    def __init__(self, year, link, type) -> None:
        super().__init__()
        self.year = year
        self.link = link
        self.type = type
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                         'Accept-Language': 'zh-CN,zh;q=0.9',  # 设置接受的语言，这里设置为中国地区
                         'Accept-Encoding': 'gzip, deflate',  # 指定编码方式
                         'Connection': 'keep-alive',  # 维持持久连接
                         'Upgrade-Insecure-Requests': '1',  # 表示客户端希望从HTTP升级到HTTPS
                    }

    def parse_pdf(self):
        # deprecated
        doc = fitz.open(self.file)
        res = []
        for page in doc:
            soup = BeautifulSoup(page.get_text('html'), features='lxml')
            res.extend(list(iter_group(soup.div)))

        res = [i.strip() for i in res]
        res = [i for i in res if re.search('^[0-9]+:', i)]
        res = [re.sub('^[0-9]+: +', '', i) for i in res]
        for item in res:
            self.append_item(self.year, item)

    def parse(self):
        year = self.year
        res = requests.get(self.link, headers=self.headers)
        if res.status_code != 200:
            raise ValueError(f"请求状态码异常: {res.status_code}")
        # import ipdb; ipdb.set_trace()
        soup = BeautifulSoup(res.content.decode(), features='lxml')
        items = soup.find_all('div', class_='obj_article_summary')
        print(f"Parsing {len(items)} articles")
        from tqdm import tqdm
        for item in tqdm(items):
            title = item.h3.get_text().strip()
            link = item.h3.a.attrs['href']
            pdf_item = item.find('a', class_='pdf')
            attrs = {'link': link}
            if pdf_item is not None:
                pdf = pdf_item.attrs['href']
                attrs['pdf'] = pdf
                self.append_download_item(year, title, pdf)
            else:
                print(item)
            # 新增关键词、摘要获取
            article_res = requests.get(link, headers=self.headers)
            if article_res.status_code != 200:
                raise ValueError(f"{link}请求状态码异常: {article_res.status_code}")
            art_soup = BeautifulSoup(article_res.content.decode(), features='lxml')
            #   import ipdb; ipdb.set_trace()
            try:
               keywords = art_soup.find('section', class_='item keywords').span.get_text().strip().replace('\t', '')
               attrs['keywords'] = keywords
               abstract = art_soup.find('section', class_='item abstract').get_text().strip().replace('\t', '')
               attrs['abstract'] = abstract
            except:
               attrs['keywords'] = None
               attrs['abstract'] = None
            field = art_soup.find('li', class_='current').span.get_text().strip().replace('\t', '')
                
            if self.type is not None:
                attrs['group'] = self.type + ': ' + field
            self.append_item(year, title, attrs=attrs)


# if __name__ == '__main__':
#     AAAI('2019', '../../archive/AAAI-19_Accepted_Papers.pdf').start()

#     AAAI('2020', '../../archive/AAAI-20-Accepted-Paper-List.pdf').start()

#     AAAI('2021',
#          '../../archive/AAAI-21_Accepted-Paper-List.Main_.Technical.Track_.pdf').start()

#     AAAI('2022',
#          '../../archive/AAAI-22_Accepted_Paper_List_Main_Technical_Track.pdf').start()


# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/595', 'Special Track AI for Social Impact, Senior Member Presentations, New Faculty Highlights, Journal Track').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/594', 'Special Track Safe, Robust and Responsible AI Track').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/593', 'Technical Tracks 18').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/592', 'Technical Tracks 17').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/591', 'Technical Tracks 16').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/590', 'Technical Tracks 15').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/599', 'Technical Tracks 14').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/588', 'Technical Tracks 13').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/587', 'Technical Tracks 12').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/586', 'Technical Tracks 11').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/585', 'Technical Tracks 10').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/584', 'Technical Tracks 9').start()
# AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/583', 'Technical Tracks 8').start()
AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/582', 'Technical Tracks 7').start()
AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/581', 'Technical Tracks 6').start()
AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/580', 'Technical Tracks 5').start()
AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/579', 'Technical Tracks 4').start()
AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/578', 'Technical Tracks 3').start()
AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/577', 'Technical Tracks 2').start()
AAAI('2024', 'https://ojs.aaai.org/index.php/AAAI/issue/view/576', 'Technical Tracks 1').start()


AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/559', 'Special Tracks').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/558', 'Technical Tracks 11').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/557', 'Technical Tracks 10').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/556', 'Technical Tracks 9').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/555', 'Technical Tracks 8').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/554', 'Technical Tracks 7').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/553', 'Technical Tracks 6').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/552', 'Technical Tracks 5').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/551', 'Technical Tracks 4').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/550', 'Technical Tracks 3').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/549', 'Technical Tracks 2').start()
AAAI('2023', 'https://ojs.aaai.org/index.php/AAAI/issue/view/548', 'Technical Tracks 1').start()


AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/402', 'Special Programs and Special Track, Student Papers and Demonstrations').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/520', 'Technical Tracks 10').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/519', 'Technical Tracks 9').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/514', 'Technical Tracks 8').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/513', 'Technical Tracks 7').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/512', 'Technical Tracks 6').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/511', 'Technical Tracks 5').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/510', 'Technical Tracks 4').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/509', 'Technical Tracks 3').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/508', 'Technical Tracks 2').start()
AAAI('2022', 'https://ojs.aaai.org/index.php/AAAI/issue/view/507', 'Technical Tracks 1').start()


AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/402', 'Student Papers and Demonstrations').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/401', 'Special Program').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/400', 'Technical Tracks 16').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/399', 'Technical Tracks 15').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/398', 'Technical Tracks 14').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/397', 'Technical Tracks 13').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/396', 'Technical Tracks 12').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/395', 'Technical Tracks 11').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/394', 'Technical Tracks 10').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/393', 'Technical Tracks 9').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/392', 'Technical Tracks 8').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/391', 'Technical Tracks 7').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/390', 'Technical Tracks 6').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/389', 'Technical Tracks 5').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/388', 'Technical Tracks 4').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/387', 'Technical Tracks 3').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/386', 'Technical Tracks 2').start()
AAAI('2021', 'https://ojs.aaai.org/index.php/AAAI/issue/view/385', 'Technical Tracks 1').start()


AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/258', 'Student Track').start()
AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/257', 'Special Program').start()
AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/256', 'Technical Tracks').start()
AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/255', 'Technical Tracks').start()
AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/254', 'Technical Tracks').start()
AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/253', 'Technical Tracks').start()
AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/252', 'Technical Tracks').start()
AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/251', 'Technical Tracks').start()
AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/250', 'Technical Tracks').start()
AAAI('2020', 'https://ojs.aaai.org/index.php/AAAI/issue/view/249', 'Technical Tracks').start()


AAAI('2010', 'https://ojs.aaai.org/index.php/AAAI/issue/view/468',
     'Symposium on Education Advances').start()
AAAI('2010', 'https://ojs.aaai.org/index.php/AAAI/issue/view/467',
     'Innovative Applications').start()
AAAI('2010', 'https://ojs.aaai.org/index.php/AAAI/issue/view/309', None).start()


AAAI('2011', 'https://ojs.aaai.org/index.php/AAAI/issue/view/470',
     'Symposium on Education Advances').start()
AAAI('2011', 'https://ojs.aaai.org/index.php/AAAI/issue/view/469',
     'Innovative Applications').start()
AAAI('2011', 'https://ojs.aaai.org/index.php/AAAI/issue/view/308', None).start()



AAAI('2012', 'https://ojs.aaai.org/index.php/AAAI/issue/view/478',
     'Symposium on Education Advances').start()
AAAI('2012', 'https://ojs.aaai.org/index.php/AAAI/issue/view/477',
     'Innovative Applications').start()
AAAI('2012', 'https://ojs.aaai.org/index.php/AAAI/issue/view/307', None).start()



AAAI('2013', 'https://ojs.aaai.org/index.php/AAAI/issue/view/480',
     'Symposium on Education Advances').start()
AAAI('2013', 'https://ojs.aaai.org/index.php/AAAI/issue/view/479',
     'Innovative Applications').start()
AAAI('2013', 'https://ojs.aaai.org/index.php/AAAI/issue/view/306', None).start()

AAAI('2014', 'https://ojs.aaai.org/index.php/AAAI/issue/view/482',
     'Symposium on Education Advances').start()
AAAI('2014', 'https://ojs.aaai.org/index.php/AAAI/issue/view/481',
     'Innovative Applications').start()
AAAI('2014', 'https://ojs.aaai.org/index.php/AAAI/issue/view/305', None).start()


AAAI('2015', 'https://ojs.aaai.org/index.php/AAAI/issue/view/483',
     'Innovative Applications').start()
AAAI('2015', 'https://ojs.aaai.org/index.php/AAAI/issue/view/304', None).start()


AAAI('2016', 'https://ojs.aaai.org/index.php/AAAI/issue/view/484',
     'Innovative Applications').start()
AAAI('2016', 'https://ojs.aaai.org/index.php/AAAI/issue/view/303', None).start()

AAAI('2017', 'https://ojs.aaai.org/index.php/AAAI/issue/view/485',
     'Innovative Applications').start()
AAAI('2017', 'https://ojs.aaai.org/index.php/AAAI/issue/view/302', None).start()

AAAI('2018', 'https://ojs.aaai.org/index.php/AAAI/issue/view/301', None).start()

AAAI('2019', 'https://ojs.aaai.org/index.php/AAAI/issue/view/246', None).start()