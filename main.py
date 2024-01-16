# Created By  : Cheng-Yi Lee
# Created Date: 01/15/2024
import re
from collections import Counter
from string import punctuation

import requests
from bs4 import BeautifulSoup


def main():
    url = "https://en.wikipedia.org/wiki/Microsoft"
    return_word_cnt = 10
    exclusion_list = 'the to and'.split()
    words = []

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    found_history = False

    for c in list(soup.findAll(["h2", "p", "h3"])):
        if c.name == 'h2' and c.text == 'History':
            found_history = True
        elif c.name in ('p', 'h3') and found_history:
            words.extend(re.sub(r'\[\d+]', '', w).strip(punctuation) for w in c.text.split() if w not in exclusion_list)
        elif found_history and c.name == 'h2':
            break

    print(Counter(words).most_common(return_word_cnt))


if __name__ == '__main__':
    main()
