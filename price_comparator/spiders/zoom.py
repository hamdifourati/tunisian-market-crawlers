# -*- coding: utf-8 -*-
import scrapy
from price_comparator.items import Product
from price_comparator.items import Category


class ZoomSpider(scrapy.Spider):
    name = "zoom"
    allowed_domains = ["zoom.com.tn"]

    product = None

    def start_requests(self):
        if self.product is not None:
            url = 'http://www.zoom.com.tn/search'
            url += '?orderby=position&orderway=desc&search_query='
            url += '%s&submit_search=' % self.product.replace(" ", "+")
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            # parse categories
            url = 'http://www.zoom.com.tn/'
            yield scrapy.Request(url=url, callback=self.parse_categories)

    def parse_categories(self, response):
        for category in response.css("#content li a"):
            name = category.css("::text").extract()[0]
            link = category.css("::attr(href)").extract()[0]
            category = Category()
            category['name'] = name
            category['link'] = link
            yield category

            if link is not None:
                yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        for prod in response.css("ul.product_list  div.product-container.full"):
            link = prod.css("h5.product-name a::attr('href')").extract_first()
            name = prod.css("h5.product-name a::attr('title')").extract_first()
            description = prod.css("p.product-desc ::text").extract_first()
            price = prod.css("span.product-price ::text").extract_first()
            # available = prod.css("span.availability ::text").extract_first()
            img = prod.css("a.product_img_link::attr('href')").extract_first()

            product = Product()
            product['name'] = name
            product['price'] = price
            product['description'] = description
            product['link'] = link
            product['img'] = img
            yield product

            next_page_e = response.css('li#pagination_next a::attr("href")')
            next_page = next_page_e.extract_first()
            if next_page is not None:
                print "[page founded : %s ]" % next_page
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, self.parse)
