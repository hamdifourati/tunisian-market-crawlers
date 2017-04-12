# -*- coding: utf-8 -*-
import scrapy


class ZoomSpider(scrapy.Spider):
    name = "zoom"
    allowed_domains = ["zoom.com.tn"]

    def start_requests(self):
        url = 'http://www.zoom.com.tn/search'
        url += '?orderby=position&orderway=desc&search_query='
        url += '%s&submit_search=' % self.product.replace(" ", "+")
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print "[OUTPUT]-[%s] { %s }" % ( response.url, response.text)

        for prod in response.css("ul.product_list  div.product-container.full"):
            link = prod.css("h5.product-name a::attr('href')").extract_first()
            name = prod.css("h5.product-name a::attr('title')").extract_first()
            description = prod.css("p.product-desc ::text").extract_first()
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
