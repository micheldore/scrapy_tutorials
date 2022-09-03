import scrapy


class ChocolatespiderSpider(scrapy.Spider):
    name = 'chocolatespider'
    allowed_domains = ['chocolate.co.uk']
    start_urls = ['https://www.chocolate.co.uk/collections/all']

    def parse(self, response):
        # here we are looping through the products and extracting the name, price & url
        products = response.css('product-item')
        for product in products:
            # here we put the data returned into the format we want to output for our csv or json file
            yield {
                'name': product.css('a.product-item-meta__title::text').get(),
                'price': product.css(".price").get().split('£')[-1].split('<')[0].strip(),
                'url': product.css('div.product-item-meta a').attrib['href'],
            }

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = ('https://%s' %
                             self.allowed_domains[0]) + next_page
            yield response.follow(next_page_url, callback=self.parse)
