import sys

def find_parser_for(url):
    module = sys.modules[__name__]
    for attr in dir(module):
        if not attr.endswith('Parser'):
            continue
        klass = getattr(module, attr)
        if url in klass.supported_urls:
            return klass


class BaseParser(object):
    supported_urls = []

    def __init__(self, response):
        self.response = response

    def extract_content(self):
        raise NotImplementedError('extract_content must be implemented')

    def extract_texts(self, selector):
        texts = self.response.xpath(selector).extract()
        return '\n'.join(self.strip_and_filter_texts(texts))

    def strip_texts(self, texts):
        return [text.strip() for text in texts]

    def strip_and_filter_texts(self, texts):
        return [text for text in self.strip_texts(texts) if text]


class JijiParser(BaseParser):
    supported_urls = ['www.jiji.com']

    def extract_content(self):
        article_block = self.response.xpath('//*[contains(@class, "ArticleBlock")]')
        if not article_block:
            return
        content = article_block[0].xpath('./*[contains(@class, "ArticleText")]/text()').extract()
        return '\n'.join(content)

class OriconParser(BaseParser):
    supported_urls = ['www.oricon.co.jp']

    def extract_content(self):
        selector = '//*[contains(@class, "content")]' + \
                   '//*[contains(@class,"box-a")]' + \
                   '//*[self::p or self::span]//text()'
        return self.extract_texts(selector)


class SanspoParser(BaseParser):
    supported_urls = ['www.sanspo.com']

    def extract_content(self):
        return self.extract_texts('//*[contains(@class, "NewsDetail")]//p/text()')

class ITMediaParser(BaseParser):
    supported_urls = ['nlab.itmedia.co.jp']

    def extract_content(self):
        return self.extract_texts('//*[@id="cmsBody"]//p/text()')

class SponichiParser(BaseParser):
    supported_urls = ['m.sponichi.co.jp']

    def extract_content(self):
        article  = self.extract_texts('//*[contains(@class, "articleBody")]/p/text()')
        readmore = self.extract_texts('//*[contains(@class, "continue")]/text()')
        return article + readmore

# class MatomeNaverParser(BaseParser):
#     supported_urls = ['matome.naver.jp']

#     def extract_content(self):
#         return

class DailyParser(BaseParser):
    supported_urls = ['sp.daily.co.jp']

    def extract_content(self):
        return self.extract_texts('//*[@id="NWrelart:Body"]/text()')

class NatalieParser(BaseParser):
    supported_urls = ['natalie.mu']

    def extract_content(self):
        nl = ''.join(self.response.xpath('//*[contains(@class, "NA_newsLead")]//*/text()').extract())
        nb = ''.join(self.response.xpath('//*[contains(@class, "NA_newsBody")]/p//text()').extract())
        filtered = [text for text in (nl+nb).split('。') if text]
        return [text+'。' for text in filtered]

class MynaviParser(BaseParser):
    supported_urls = ['news.mynavi.jp']

    def extract_content(self):
        return self.extract_texts('//*[contains(@class, "article-content")]/p/text()')


class SankeiParser(BaseParser):
    supported_urls = ['www.sankei.com']

    def extract_content(self):
        return self.extract_texts('//*[contains(@class, "articleText")]//article//p/text()')
#class News47Parser(BaseParser):
#
#    supported_urls = ['www.47news.jp']
#
#    def extract_content(self):
#        return self.extract_texts('')

class CookpadParser(BaseParser):
    supported_urls = ['cookpad.com']

    def extract_content(self):
        if "recipe" in self.response.url:
            return self.extract_texts('//*[@id="recipe"]/div[contains(@class, "description")]/text()')
        elif "articles" in self.response.url:
            return self.extract_texts('//*[@id="main"]//p/text()')
        else:
            return None

class MdprParser(BaseParser):
    supported_urls = ['mdpr.jp']

    def extract_content(self):
        return self.extract_texts('//*[contains(@class, "topic-body")]/div[contains(@class, "m1 cf")]/text()')

class ThisKijiIsParser(BaseParser):
    supported_urls = ['http://this.kiji.is']

    def extract_content(self):
        return self.extract_texts('//*[contains(@class, "main__article")]//p/text()')

class FashionPressParser(BaseParser):
    supported_urls = ["www.fashion-press.net"]

    def extract_content(self):
        return self.extract_texts('//*[@id="entry_article"]//p/text()')
