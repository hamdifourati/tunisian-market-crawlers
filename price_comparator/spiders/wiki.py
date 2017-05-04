# -*- coding: utf-8 -*-
import scrapy


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["wiki.tn"]

    product = None

    def start_requests(self):
        if self.product is not None:
            url = 'https://www.wiki.tn/recherche?controller=search'
            url += '&orderway=desc&search_query=&orderby=position'
            url += '%s&submit_search=' % self.product.replace(" ", "+")
            yield scrapy.Request(url=url, callback=self.parse)
        else:

            url = 'https://www.wiki.tn/plan-du-site'
            yield scrapy.Request(url=url, callback=self.parse_categories)

    def parse_categories(self, response):
        for category in response.css("div.categTree.box li a"):
            name = category.css("::text").extract()[0]
            url = category.css("::attr(href)").extract()[0]
            yield {
                "category": {
                    "name": name,
                    "url": url
                }
            }

            if url is not None:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for prod in response.css("div.product-container"):
            link = prod.css("h4[itemprop*=name] a::attr('href')")\
                .extract_first()
            name = prod.css("h4[itemprop*=name] ::text").extract_first()
            description = prod.css("div[itemprop*=description] ::text")\
                .extract_first()
            price = prod.css("span[itemprop*=price] ::text")\
                .extract_first()
            available = prod.css("link[itemprop*=availibility] ::text")\
                .extract_first()
            img = prod.css("img[itemprop*=image]::attr(src)").extract_first()

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
