from wordcloud import WordCloud
import pandas as pd
import os
import re
import collections

def plot_wordcloud(data, save_dir):
    """ Plot wordcloud of keywords """
    wc = WordCloud(#stopwords, font_path
                    width = 3000,
                    height = 2000,
                    background_color='white',
                    max_words=100)

    wc.generate(data)
    wc.to_file(save_dir)

if __name__ == '__main__':
    # base_path = r"E:\Brian\Projects\Awesome-Paper-List-py-master\collections\AAAI"
    # save_path = r"E:\Brian\Projects\Awesome-Paper-List-py-master\wordclouds\AAAI"
    base_path = r"E:\Brian\Projects\Awesome-Paper-List-py-master\collections\WACV"
    save_path = r"E:\Brian\Projects\Awesome-Paper-List-py-master\wordclouds\WACV"
    os.makedirs(save_path, exist_ok=True)
    for f in os.listdir(base_path):
        f_name, ext = os.path.splitext(f)
        if ext == '.csv':
            print("Ploting wordcloud for year ", f_name)
            df = pd.read_csv(os.path.join(base_path, f))
            df = df.dropna(axis=0, how='all')
            titles_list = df['title'].tolist()
            plot_wordcloud('\n'.join(titles_list),
                            os.path.join(save_path, f_name + '_titles_wordcloud.jpg'))
            
            keywords_list = df['keywords'].tolist()
            keywords = []
            for kws in keywords_list:
                if type(kws) != str or not kws:
                    continue
                matches = re.findall(r':\s*(.*?)(?:,\s*|\Z)', kws)
                if matches:
                    keywords += matches
            # Keywords is none
            if not keywords:
                continue

            plot_wordcloud('\n'.join(keywords),
                            os.path.join(save_path, f_name + '_keyword_wordcloud.jpg'))
            
                        