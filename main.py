# Created By  : Cheng-Yi Lee
# Created Date: 04/29/2024
import re
from collections import Counter
from configparser import ConfigParser
from string import punctuation

import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://en.wikipedia.org/wiki/Microsoft'
    default_config = '''
    [number_of_words]
    number = 10
    
    [words_to_exclude]
    string = 
    '''
    config = ConfigParser()
    config.read_string(default_config)
    config.read('CrawlerWikiMSFT.ini')
    return_word_cnt = int(config.get('number_of_words', 'number'))
    exclusion_list = config.get('words_to_exclude', 'string').split(',')
    words = []

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    found_history = False

    for c in list(soup.findAll(['h2', 'p', 'h3'])):
        if c.name == 'h2' and c.text == 'History':
            found_history = True
        elif c.name in ('p', 'h3') and found_history:
            words.extend(re.sub(r'\[\d+]', '', w).strip(punctuation) for w in c.text.split() if w not in exclusion_list)
        elif found_history and c.name == 'h2':
            break

    print(Counter(words).most_common(return_word_cnt))


if __name__ == '__main__':
    main()
