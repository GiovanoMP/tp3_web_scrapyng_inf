import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"  # Nome do Spider
    allowed_domains = ["books.toscrape.com"]  # Domínio permitido
    start_urls = ["http://books.toscrape.com/"]  # URL inicial

    def parse(self, response):
        # Para cada livro na página
        for book in response.css('article.product_pod'):
            # Extraímos o título, o preço e a disponibilidade do livro
            yield {
                'title': book.css('h3 a::attr(title)').get(),  # Título do livro
                'price': book.css('div.product_price p.price_color::text').get(),  # Preço do livro
                'availability': book.css('p.instock.availability::text').re_first('\S+'),  # Disponibilidade do livro
            }

        # Verifica se há um link para a próxima página
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            # Faz a requisição da próxima página e chama novamente o método 'parse'
            yield response.follow(next_page, self.parse)
