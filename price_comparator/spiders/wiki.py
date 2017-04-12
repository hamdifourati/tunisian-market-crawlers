# -*- coding: utf-8 -*-
import scrapy


class MytekSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["wiki.tn"]

    def start_requests(self):
        url = 'https://www.wiki.tn/recherche?controller=search&orderby=position'
        url += '&orderway=desc&search_query='
        url += '%s&submit_search=' % self.product.replace(" ", "+")
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print "[OUTPUT]-[%s] { %s }" % ( response.url, response.text)
        for prod in response.css("div.product-container"):
            link = prod.css("h4  a.product-name::attr('href')").extract_first()
            name = prod.css("h5 a.product-name ::text").extract_first()
            description = prod.css("div.product-desc ::text").extract_first()
            price = prod.css("span.product-price ::text").extract_first()
            available = prod.css("span.availability ::text").extract_first()
            img = prod.css("a.product_img_link::attr('href')").extract_first()

            yield {
                "link": link,
                "name": name,
                "description": description,
                "offers":
                {
                    "price": price,
                    "available": available
                },
                "img": img
                }
            next_page_e = response.css('li#pagination_next a::attr("href")')
            next_page = next_page_e.extract_first()
            if next_page is not None:
                print "[page founded : %s ]" % next_page
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, self.parse)
