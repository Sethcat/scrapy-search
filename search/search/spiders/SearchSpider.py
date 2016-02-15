# -*- coding=utf-8 -*-
# scrapy crawl sbaidu -a key="关键字"
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy.http import Request, FormRequest
from search.items import SearchItem
import logging,sys#,urllib
import requests,string,re

reload(sys)
sys.setdefaultencoding('utf-8')

class SearchSpider(CrawlSpider):
    name = "sbaidu"
    allowed_domains = ["baidu.com"]

    def __init__(self, key='奥巴马 夏威夷', *args, **kwargs):
        self.domain = "http://www.baidu.com"
        self.start_urls = ['http://www.baidu.com/s?wd=%s'%key]
        self.pages=1;
        super(SearchSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        sel = Selector(response)
        items=[]
        for i in range((self.pages-1)*10, self.pages*10):
            i+=1
            item = SearchItem()
            url = sel.xpath('//div[@id="%d"]/h3/a/@href'%(i)).extract()
            title = sel.xpath('//div[@id="%d"]/h3/a//text()'%(i)).extract()
            desc = sel.xpath('//div[@id="%d"]//div[@class="c-abstract"]//text()'%(i)).extract()
            item['num'] = str(i)
            item['title'] = title if title else '未爬取到标题'
            item['url'] = url if url else 'www.example.com'
            item['desc'] = desc if desc else '未爬取到内容'            
            print str(i)+' '+''.join(item['title'])+'\n'
            yield item 
        next_page = sel.xpath('//div[@id="page"]/a[@class="n"]/@href').extract()
        self.pages+=1
        if len(next_page)==2:
            yield Request(self.domain+next_page[1])
        elif ((len(next_page)==1) and (re.match(r'.*rsv_page=1$',next_page[0]))):
            yield Request(self.domain+next_page[0])
        else:
            print "Congratulations! All results has crawled!"
            raise CloseSpider('Happy Ending')




                                