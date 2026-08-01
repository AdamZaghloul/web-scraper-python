import sys, requests, asyncio
import crawl
from json_report import write_json_report

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    
    if len(sys.argv) < 3:
        print("no max concurrency provided")
        sys.exit(1)
    
    if len(sys.argv) < 4:
        print("no max pages provided")
        sys.exit(1)

    if len(sys.argv) > 4:
            print("too many arguments provided")
            sys.exit(1)

    base_url = sys.argv[1]
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])

    print(f"starting crawl of: {base_url}")
    page_data = await crawl.crawl_site_async(base_url, max_concurrency, max_pages)

    print(f"{len(page_data)} pages crawled.")
    write_json_report(page_data)
     
if __name__ == "__main__":
    asyncio.run(main())
