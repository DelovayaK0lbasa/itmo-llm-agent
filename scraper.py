import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def scrapping_websites(urls):
    headers={
        "User-Agent": UserAgent().random
    }
    res = ''
    for url in urls:
        r = requests.get(
            url=url,
            headers=headers
        )
        soup = BeautifulSoup(r.content, 'html.parser')
        news = soup.find_all('div', class_='thumb')
        for n in news:
            link = f"https://news.itmo.ru{n.find('a')['href']}"
            res += extract_info(link, headers)
            if len(res) >= 10_000:
                return res
    return res

def extract_info(url, headers):
    r = requests.get(
        url=url,
        headers=headers
    )
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('p', class_='lead').find('strong').getText()
    post_content = '\n'.join(soup.find_all('p', class_='ltr'))
    return f"{title}\n\n {post_content}\n\n"

