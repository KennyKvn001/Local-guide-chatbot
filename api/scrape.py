import asyncio
from crawl4ai import AsyncWebCrawler
import os


async def scrape_rwanda_data(urls, output_file="rwanda_data.txt"):
    async with AsyncWebCrawler() as crawler:

        # Clear existing file to avoid duplication
        if os.path.exists(output_file):
            os.remove(output_file)

        for url in urls:
            try:
                result = await crawler.arun(url=url)
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"\nSource: {url}\n{result.markdown}\n")
                print(f"Scraped {url}")
            except Exception as e:
                print(f"{url} → {e}")


if __name__ == "__main__":
    urls = [
        "https://www.visitrwanda.com/",
        "https://www.visitrwanda.com/destinations/",
        "https://visitrwanda.com/meet-in-rwanda/",
        "https://www.visitrwanda.com/accommodations/",
        "https://www.visitrwanda.com/events/",
        "https://igihe.com",
        "https://www.gov.rw/",
        "https://en.wikipedia.org/wiki/Rwanda",
        "https://www.lonelyplanet.com/rwanda",
        "https://www.rdb.rw/",
        "https://www.rdb.rw/en/about-rdb",
    ]
    asyncio.run(scrape_rwanda_data(urls))
