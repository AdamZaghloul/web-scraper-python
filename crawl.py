import urllib.parse
from bs4 import BeautifulSoup, Tag

def normalize_url(url: str):
    split = urllib.parse.urlsplit(url)
    string = f"{split.netloc}{split.path}"
    return string.removesuffix("/")

def get_heading_from_html(html: str) -> str:

    soup = BeautifulSoup(html, 'html.parser')

    h_tag = soup.find('h1')

    if h_tag is None:
        h_tag = soup.find('h2')

    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    
    main_tag = soup.find('main')

    if main_tag is None:
        main_tag = soup.find('p')
    else:
        main_tag = main_tag.find('p')

        if main_tag is None:
                main_tag = soup.find('p')

    return main_tag.get_text(strip=True) if isinstance(main_tag, Tag) else ""