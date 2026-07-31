import urllib.parse
from bs4 import BeautifulSoup, Tag

def normalize_url(url: str):
    split = urllib.parse.urlsplit(url)
    string = f"{split.scheme}://{split.netloc}{split.path}"
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

def get_urls_from_html(html, base_url):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        soup_links = soup.find_all('a')
        links = []

        for link in soup_links:
            links.append(urllib.parse.urljoin(base_url, link.get("href")))

        return links

    except:
        return Exception("Error")

def get_images_from_html(html, base_url):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        soup_links = soup.find_all('img')
        links = []

        for link in soup_links:
            links.append(urllib.parse.urljoin(base_url, link.get("src")))

        return links

    except:
        return Exception("Error")

def extract_page_data(html: str, page_url: str):
    page_dic = {}

    page_dic["url"] = page_url
    page_dic["heading"] = get_heading_from_html(html)
    page_dic["first_paragraph"] = get_first_paragraph_from_html(html)
    page_dic["outgoing_links"] = get_urls_from_html(html, page_url)
    page_dic["image_urls"] = get_images_from_html(html, page_url)

    return page_dic

def is_same_domain(url1, url2)  -> bool:
    split1 = urllib.parse.urlsplit(url1)
    split2 = urllib.parse.urlsplit(url2)

    if split1.netloc == split2.netloc:
        return True

    return False