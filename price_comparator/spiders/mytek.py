# -*- coding: utf-8 -*-
import scrapy


class MytekSpider(scrapy.Spider):
    name = "mytek"
    allowed_domains = ["mytek.tn"]

    def start_requests(self):
        url = 'http://www.mytek.tn/recherche?controller=search&orderby=position'
        url += '&orderway=desc&search_query='
        url += '%s&submit_search=&n=999999999' % self.product.replace(" ", "+")
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print "[OUTPUT]-[%s] { %s }" % ( response.url, response.text)

        for prod in response.css("ul.product_list  div.product-container"):
            link = prod.css("h5 a.product-name::attr('href')").extract_first()
            name = prod.css("h5 a.product-name ::text").extract_first()
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
