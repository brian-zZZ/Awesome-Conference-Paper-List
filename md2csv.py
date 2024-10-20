# 将Markdown格式转出CSV格式

import pandas as pd
import os
import re

def splitter(line):
    title_match = re.search(r'^(.*)\|', line)
    link_match = re.search(r'\[link\]\((.*?)\),', line)
    pdf_match = re.search(r'\[pdf\]\((.*?)\),', line)
    keywords_match = re.search(r'\[keywords\]\((.*?)\),', line)
    abstract_match = re.search(r'\[abstract\]\((.*?)\),', line)
    group_match = re.search(r'\[group\]\((.*?)\)', line)

    title = title_match.group(1).strip() if title_match else None
    link = link_match.group(1).strip() if link_match else None
    pdf = pdf_match.group(1).strip() if pdf_match else None
    keywords = keywords_match.group(1).strip() if keywords_match else None
    abstract = abstract_match.group(1).strip() if abstract_match else None
    group = group_match.group(1).strip() if group_match else None

    data = {
        'title': [title],
        'keywords': [keywords],
        'abstract': [abstract],
        'group': [group],
        'link': [link],
        'pdf': [pdf]
    }

    return data

base_path = r"E:/Brian/Projects/Awesome-Paper-List-py-master/collections/AAAI"
for f in os.listdir(base_path):
    f_name, ext = os.path.splitext(f)

    if ext == '.md':
        print("Converting ", f)
        csv_df = pd.DataFrame(columns=['title', 'keywords', 'group', 'link', 'pdf'])
        with open(os.path.join(base_path, f), 'r', encoding='utf-8') as fr:
            for line in fr.readlines():
                data = splitter(line)
                csv_df = pd.concat([csv_df, pd.DataFrame(data)], axis=0)
        csv_df.to_csv(os.path.join(base_path, f_name + '.csv'), index=False)
