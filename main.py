import sys, requests, asyncio
import crawl

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
            print("too many arguments provided")
            sys.exit(1)

    base_url = sys.argv[1]

    print(f"starting crawl of: {base_url}")
    page_data = await crawl.crawl_site_async(base_url, 10)

    print(f"{len(page_data)} pages crawled.")
     
if __name__ == "__main__":
    asyncio.run(main())
