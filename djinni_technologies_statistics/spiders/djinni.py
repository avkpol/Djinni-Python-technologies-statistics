import scrapy
import csv
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DjinniSpider(scrapy.Spider):
    name = 'djinni'
    start_urls = ['https://djinni.co/jobs/?primary_keyword=Python']

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.results = []

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "list-jobs__item")))
        html = self.driver.page_source
        selector = Selector(text=html)

        job_items = selector.css('.list-jobs__item')

        for job_item in job_items:
            title = job_item.css('.list-jobs__title > a > span::text').get()
            title = title.strip() if title else ''
            if title:
                print(title)  # Print the title

                description = job_item.css('.list-jobs__description .text-card::text').extract()
                description = ' '.join(description).strip() if description else ''
                print(description)  # Print the description

                self.results.append({
                    'title': title,
                    'description': description
                })

        next_page = response.css(".pagination > li")[-1].css("a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        self.write_to_file()

    def closed(self, reason):
        self.driver.quit()

    def write_to_file(self):
        with open('python_vacancies.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(DjinniSpider)
    process.start()

