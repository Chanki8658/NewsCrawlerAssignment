from scrapy.spiders import Spider
from dirbot.items import Website


class caissSpider(Spider):
    name = "caissSpider"
    allowed_domains = ["venturebeat.com", "techcrunch.com", "infoworld.com"]
    start_urls = [
        "http://venturebeat.com/category/small-biz/",
        "https://techcrunch.com/mobile/",
        "http://www.infoworld.com/category/application-development/",
    ]


    def parse(self, response):
        #(1)The number of articles we want to grab in each domain
        GRABNO = 3

        items = []

        #(2) For comparing and indicating which start_url that the response scraping from
        xpathSel = [
            # VentureBeat
            '//article',
            # Techcrunch
            '//li[@class="river-block "]//div[@class="block-content"]',
            # InfoWord
            '//div[@class="river-well article"]',
        ]

        compareUrls = [
            "http://venturebeat.com/category/small-biz/",
            "https://techcrunch.com/mobile/",
            "http://www.infoworld.com/category/application-development/"
        ]

        sites = [
            "",
            "",
            "http://www.infoworld.com",
        ]

        domains = [
            "VentureBeat",
            "TechCrunch",
            "Infoworld"
        ]

        #extract the url
        respon = str(response)[5:-1]

        #get the index of the Url
        indexes = [i for i, v in enumerate(compareUrls) if v == respon]
        index = indexes[0]

        #final xpath
        xpathReal = xpathSel[index]

        #(3) Process the response by xpath
        for i, sel in enumerate(response.xpath(xpathReal)):
            
            # print "sel url", sel.xpath('@href').extract       # print "sel desp", sel.xpath('text()').extract        if i < GRABNO:
                #Call the website item model
                item = Website()

                if domains[index] == "VentureBeat":
                    item['domain'] = "VentureBeat"
                    item['domainUrl'] = "http://venturebeat.com/category/small-biz/"
                    nameTmp = sel.xpath('//h2ass="article-title"]/a/text()').extract()[i]
                    item['url'] = str(sel.xpath('//h2ass="article-title"]/a/@href').extract()[i])
                    item['img'] = sel.xpath('//divass="article-media-thumbnail"]/a//img[@class="attachment-river-wide size-river-wide wp-post-image"]/@src').extract()[i]
                    despTmp = ""

                elif domains[index] == "TechCrunch":
                    item['domain'] = "TechCrunch"
                    item['domainUrl'] = "https://techcrunch.com/mobile/"
                    nameTmp = sel.xpath('//h2ass="post-title"]/a/text()').extract()[i]
                    item['url'] = str(sel.xpath('//h2ass="post-title"]/a/@href').extract()[i])
                    item['img'] = sel.xpath('//spantains(@data-omni-sm-delegate, "gbl_river_image")]/a/img/@data-src').extract()[i]
                    despTmp = sel.xpath('//pass="excerpt"]/text()').extract()[i]

                else:
                    item['domain'] = "Infoworld"
                    item['domainUrl'] = "http://www.infoworld.com/category/application-development/"
                    nameTmp = sel.xpath('//divass="post-cont"]//h3/a/text()').extract()[i]
                    item['url'] = sites[index] + str(sel.xpath('//divass="post-cont"]//h3/a/@href').extract()[i])
                    item['img'] = sel.xpath('//figureass="well-img"]/a//img[contains(@class, "lazy carousel.idgeImage")]/@data-original').extract()[i]
                    despTmp = sel.xpath('//h4/text()').extract               #Try to ignore the ASCII if there is any
                try:
                    desp = despTmp.encode('ascii', 'ignore').decode('ascii')
                except:
                    desp = despTmp

                try:
                    name = nameTmp.encode('ascii', 'ignore').decode('ascii')
                except:
                    name = nameTmp

                item['description'] = desp
                item['name'] = name

                items.append(item)
                
        

        return items