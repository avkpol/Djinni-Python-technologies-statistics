import asyncio
import csv
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin


class DjinniSpider:
    name = 'djinni'
    start_url = 'https://djinni.co/jobs/?primary_keyword=Python'
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    results = []

    async def parse(self, response):
        self.driver.get(response)
        await self.wait_for_element(By.CLASS_NAME, "list-jobs__item")
        html = self.driver.page_source
        selector = Selector(text=html)

        job_items = selector.css('.list-jobs__item')

        for job_item in job_items:
            title = job_item.css('.list-jobs__title > a > span::text').get()
            title = title.strip() if title else ''
            if title:
                description = job_item.css('.list-jobs__description .text-card::text').extract()
                description = ' '.join(description).strip() if description else ''
                self.results.append({
                    'title': title,
                    'description': description
                })

        next_page = selector.css(".pagination > li")[-1].css("a::attr(href)").get()
        if next_page is not None:
            next_url = urljoin(response, next_page)
            if next_url == response:
                return
            await self.parse(response=next_url)

    async def wait_for_element(self, by, value):
        element = await asyncio.get_event_loop().run_in_executor(
            None, lambda: WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, value)))
        )
        return element

    def write_to_file(self):
        with open('../data/python_vacancies.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)


async def crawl():
    spider = DjinniSpider()
    await spider.parse(response=spider.start_url)
    spider.write_to_file()
    spider.driver.quit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawl())
    loop.close()

