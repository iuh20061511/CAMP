import scrapy
from booksc.items import BooksItem

class MycraperSpider(scrapy.Spider):
    name = "mycraper"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # Extract data from current page
        yield from self.parse_page(response)

        # Check for next page link and follow it
        #next_page = response.css('li.next a::attr(href)').get()
        #if next_page and self.page_count < 2:  # Check if there is a next page and if the page count is less than 5
           # self.page_count += 1  # Increment page count
           # yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
    def parse_page(self, response):
        # Extract data from the current page
        courseList = response.xpath('//div[@class="row"]/descendant::ol/li/article/h3/a/@href').getall()
        for courseItem in courseList:
            item = BooksItem()
            item['urlBook'] = response.urljoin(courseItem)
            request = scrapy.Request(url=response.urljoin(courseItem), callback=self.parseCourseDetailPage)
            request.meta['dataBook'] = item
            yield request 
    def parseCourseDetailPage(self, response):
        item = response.meta['dataBook']
        item['title'] = response.xpath('normalize-space(string(//div[@class="col-sm-6 product_main"]/h1))').get()
        #item['price'] = response.xpath('normalize-space(string(//div[@class="col-sm-6 product_main"]/p[@class="price_color"]))').get()
        price_text = response.xpath('normalize-space(string(//div[@class="col-sm-6 product_main"]/p[@class="price_color"]))').get()
        item['price'] = float(price_text.replace('£', '')) if price_text else None

        item['instock'] = response.xpath('normalize-space(string(//div[@class="col-sm-6 product_main"]/p[@class="instock availability"]))').get()
        item['product_description'] = response.xpath('normalize-space(string(//article[@class="product_page"]/p))').get()
        item['categories'] = response.xpath('normalize-space(string(//ul[@class="breadcrumb"]/li[3]/a/text()))').get()
       
        #item['star_rating'] = response.xpath("substring-after(//div[contains(@class, 'product_main')]/p[contains(@class, 'star-rating')]/@class, 'star-rating ')").extract_first() 
        star_mapping = { "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5 }
        star_class = response.xpath("//div[contains(@class, 'product_main')]/p[contains(@class, 'star-rating')]/@class").extract_first()
        item['star_rating'] = star_mapping.get(star_class.split(' ')[1].capitalize(), None) if star_class else None


        item['upc'] = response.xpath('normalize-space(string(//th[text()="UPC"]/following-sibling::td))').get()
        item['price_exc'] = response.xpath('normalize-space(string(//th[text()="Price (excl. tax)"]/following-sibling::td))').get()
        item['price_inc'] = response.xpath('normalize-space(string(//th[text()="Price (incl. tax)"]/following-sibling::td))').get()
        item['tax'] = response.xpath('normalize-space(string(//th[text()="Tax"]/following-sibling::td))').get()
        item['number_review'] = response.xpath('normalize-space(string(//th[text()="Number of reviews"]/following-sibling::td))').get()
        item['image_url'] = response.xpath('normalize-space(string(//div[@class="item active"]/img/@src))').get()
      



        yield item
