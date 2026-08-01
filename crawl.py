import urllib.parse, asyncio, aiohttp
from bs4 import BeautifulSoup, Tag

class AsyncCrawler():

    def __init__(self, base_url, max_concurrency):
        self.base_url = base_url
        self.base_domain =urllib.parse.urlsplit(base_url).hostname
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data:
                return False

            self.page_data[normalized_url] = {}
            return True

    async def get_html(self, url):
        async with self.session.get(url) as response:

            if response.status >= 400:
                raise Exception(f"Error: {response.status}")

            if "text/html" not in response.headers["content-type"]:
                raise Exception(f"Error: content-type is {response.headers['content-type']}")

            return await response.text()

    async def crawl_page(self, base_url, current_url=None):
        if not is_same_domain(base_url, current_url):
            return

        norm_current = normalize_url(current_url)

        if not await self.add_page_visit(norm_current):
            return

        async with self.semaphore:

            print(f"Getting html from {norm_current}")
            html = await self.get_html(norm_current)

        async with self.lock:
            self.page_data[norm_current] = extract_page_data(html, norm_current)

        tasks = []

        for link in self.page_data[norm_current]["outgoing_links"]:
            tasks.append(asyncio.create_task(self.crawl_page(base_url, link)))
        
        await asyncio.gather(*tasks)

    async def crawl(self):

        await self.crawl_page(self.base_url, self.base_url)

        return self.page_data

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

async def crawl_site_async(url, max_concurrency):
    crawler = AsyncCrawler(normalize_url(url), max_concurrency)

    async with crawler:

        page_data = await crawler.crawl()

    
    return page_data