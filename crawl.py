import urllib.parse, asyncio, aiohttp
from bs4 import BeautifulSoup, Tag

class AsyncCrawler():

    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain =urllib.parse.urlsplit(base_url).hostname
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url: str):
        async with self.lock:

            if self.should_stop:
                return False

            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                #current = asyncio.current_task()

                #for task in list(self.all_tasks):
                #    if task == current:
                #        continue
                #    task.cancel()

                return False

            if normalized_url in self.page_data:
                return False

            print(f"Crawling {normalized_url}")
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
        
        if self.should_stop:
            return

        norm_current = normalize_url(current_url)

        if not await self.add_page_visit(norm_current):
            return

        async with self.semaphore:

            html = await self.get_html(norm_current)

        async with self.lock:
            self.page_data[norm_current] = extract_page_data(html, norm_current)

        if self.should_stop:
            return

        for link in self.page_data[norm_current]["outgoing_links"]:
            if self.should_stop:
                return
            
            self.all_tasks.add(asyncio.create_task(self.run_child(base_url, link)))

    async def crawl(self):

        await self.crawl_page(self.base_url, self.base_url)

        while self.all_tasks:
            tasks = list(self.all_tasks)
            await asyncio.gather(*tasks, return_exceptions=True)
            self.all_tasks.difference_update(task for task in tasks if task.done())

        return self.page_data

    async def run_child(self, base_url, link):
        task = asyncio.current_task()
        try:
            await self.crawl_page(base_url, link)
        finally:
            self.all_tasks.discard(task)

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
        raise Exception("Error")

def get_images_from_html(html, base_url):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        soup_links = soup.find_all('img')
        links = []

        for link in soup_links:
            links.append(urllib.parse.urljoin(base_url, link.get("src")))

        return links

    except:
        raise Exception("Error")

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

async def crawl_site_async(url, max_concurrency, max_pages):
    crawler = AsyncCrawler(normalize_url(url), max_concurrency, max_pages)

    async with crawler:

        page_data = await crawler.crawl()

    
    return page_data