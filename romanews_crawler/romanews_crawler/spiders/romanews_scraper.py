import scrapy

class RomanewsSpider(scrapy.Spider):
    name = "romanews_scraper_v2"
    allowed_domains = ["romanews.com.br"]
    start_urls = ["https://www.romanews.com.br/page/1/"]

    def parse(self, response):
        # Seleciona os links de cada notícia na página
        news_links = response.css('a::attr(href)').getall()
        
        # Segue cada link encontrado para fazer scraping do conteúdo
        for link in news_links:
            if "romanews.com.br" in link:
                yield response.follow(link, self.parse_news)
        
        # Paginação - segue para a próxima página
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_news(self, response):
        # Extrai informações da página da notícia
        yield {
            'title': response.css('h2::text').get(),
            'category': response.css('p.font-bold::text').get(),
            'description': response.css('h3::text').get(),
            'author': response.css('p.hidden::text').get(),
            'published_time': response.css('time::attr(datetime)').get(),
            'link': response.url,
        }
