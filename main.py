import sys, requests
import crawl

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
            print("too many arguments provided")
            sys.exit(1)

    base_url = sys.argv[1]

    print(f"starting crawl of: {base_url}")
    page_data = crawl_page(base_url, base_url, {})

    print(f"{len(page_data)} pages crawled.")

def get_html(url):
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})

    if response.status_code > 400:
         raise Exception(f"Error: {response.status_code}")

    if "text/html" not in response.headers["content-type"]:
         raise Exception(f"Error: content-type is {response.headers['content-type']}")

    return response.text

def crawl_page(base_url, current_url=None, page_data=None):
    if not crawl.is_same_domain(base_url, current_url):
        return

    norm_current = crawl.normalize_url(current_url)

    if norm_current in page_data:
        return

    print(f"Getting html from {norm_current}")
    html = get_html(norm_current)

    page_data[norm_current] = crawl.extract_page_data(html, norm_current)

    for link in page_data[norm_current]["outgoing_links"]:
        crawl_page(base_url, link, page_data)

    return page_data
     
if __name__ == "__main__":
    main()
