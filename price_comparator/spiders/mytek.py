# -*- coding: utf-8 -*-
import scrapy


class MytekSpider(scrapy.Spider):
    name = "mytek"
    allowed_domains = ["mytek.tn"]

    product = None

    def start_requests(self):
        if self.product is not None:
            url = 'http://www.mytek.tn/recherche'
            url += '?controller=search&orderby=position'
            url += '&orderway=desc&search_query='
            url += '%s&submit_search=' % self.product.replace(" ", "+")
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            # parse categories
            url = 'http://www.mytek.tn/'
            yield scrapy.Request(url=url, callback=self.parse_categories)

    def parse_categories(self, response):
        for category in response.css("#menu li a"):
            name = category.css("::text").extract_first()
            url = category.css("::attr(href)").extract_first()
            yield {
                    "category": {
                        "name": name,
                        "url": url
                    }
            }
            if url is not None:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for prod in response.css("ul.product_list  div.product-container"):
            link = prod.css("h5 a.product-name::attr('href')").extract_first()
            name = prod.css("h5 a.product-name ::text").extract_first()
            description = prod.css("p.product-desc ::text").extract_first()
            price = prod.css("span.product-price ::text").extract_first()
            available = prod.css("span.availability ::text").extract_first()
            img = prod.css("a.product_img_link img::attr('src')")\
                .extract_first()

            yield {
                "product": {
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
            }
            next_page_e = response.css('li#pagination_next a::attr("href")')
            next_page = next_page_e.extract_first()
            if next_page is not None:
                print "[page founded : %s ]" % next_page
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, self.parse)
