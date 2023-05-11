import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            link = book.css("h3 a").attrib["href"]

            if "catalogue" in link:
                book_page = "https://books.toscrape.com/" + link
            else:
                book_page = "https://books.toscrape.com/catalogue/" + link

            yield response.follow(book_page, callback=self.parse_book)

        next = response.css("li.next a").attrib["href"]
        if next is not None:
            if "catalogue/" in next:
                next_url = "https://books.toscrape.com/" + next
            else:
                next_url = "https://books.toscrape.com/catalogue/" + next
            yield response.follow(next_url, callback=self.parse)

    def parse_book(self, response):
        yield {
            "name": response.css("div.col-sm-6.product_main h1 ::text").get(),
            "category": response.xpath("//div//div//ul//li[3]//text()").extract()[1],
            "price": response.css("p.price_color ::text").get(),
            "Description": response.xpath(
                "(//div//div//div//div//article//p)[4]//text()"
            ).extract()[0],
        }
