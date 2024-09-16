import scrapy

class CnnbrSpider(scrapy.Spider):
    name = "cnnbr_spider"
    allowed_domains = ["cnnbrasil.com.br"]
    start_urls = ["https://www.cnnbrasil.com.br/"]

    # Limite de páginas que vamos raspar
    max_pages = 5
    page_count = 0

    def parse(self, response):
        # Selecionar links das notícias
        news_links = response.css('li.block__news__item a::attr(href)').getall()

        # Para cada link, segue para a página da notícia e faz o scraping do conteúdo
        for link in news_links:
            yield response.follow(link, self.parse_news)

        # Paginação - segue para a próxima página até o limite definido
        if self.page_count < self.max_pages:
            self.page_count += 1
            next_page = f'https://www.cnnbrasil.com.br/?pagina={self.page_count}'
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_news(self, response):
        # Extrair informações da página da notícia
        yield {
            'title': response.css('h3.block__news__title::text').get(),
            'description': response.css('figcaption h3::text').get(),
            'link': response.url,
        }

