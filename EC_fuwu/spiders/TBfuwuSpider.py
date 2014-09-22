import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from tutorial.items import FuwuPurchaseItem,FuwuISVItem
from scrapy.http import Request
#import json
import jsondatetime as json
import re
import pprint 

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class TBfuwuSpider(CrawlSpider):
    name = "TBfuwu"
    allowed_domains = ["fuwu.taobao.com"]
    start_urls = [
                  "http://fuwu.taobao.com",
                 ]
    
    rules = [
             Rule(LxmlLinkExtractor(allow=['/ser/list\.htm\?.+&tracelog=category.*'], restrict_xpaths=['//*[@id="J_Menu"]/ul[1]/li[7]'])),
             Rule(LxmlLinkExtractor(allow=['/ser/detail\.htm?.+&tracelog=category.*']), 'requestBuyer',{"pageNo": 1, "pageCount":1})
             ]     
   
    def requestBuyer(self, response, **kwargs):
        #pprint.pprint(locals())
        #get reuqest URL
        urlRequestRaw = response.xpath('//div[@id="J_TradeLog"]/@data-action').extract()[0]
        self.log("TradeLog request: %s" % urlRequestRaw, level=log.INFO)
        # print urlRequestRaw        
        #parseBuyer(self, response, urlRequestRaw, 1, 1)

        urlRequestBuyer = urlRequestRaw.format(page = kwargs['pageNo'], count=kwargs['pageCount'])
        request = scrapy.Request('http://fuwu.taobao.com' + urlRequestBuyer,
                             callback=self.parseBuyer)       
        request.meta['urlRequestRaw'] = urlRequestRaw
        
        #decode fuwuISV
        item = FuwuISVItem()
        item['name']=response.xpath('//*[@id="J_SKUForm"]/div[1]/h2/text()').extract()[0].strip()
        item['category']=response.xpath('//*[@id="apc-detail"]/div[1]/a[3]').extract()[0].strip()
        item['link']=response.url.strip()
        
       # request.meta['fuwuISV.name'] = item['name']
       # request.meta['fuwuISV.category'] = item['category']
        request.meta['fuwuISV'] = item
        yield item
        yield request
        
    #recursively parse buyers while yield request & items 
    def parseBuyer(self, response):
        #pprint.pprint(locals())             
        urlRequestRaw = response.meta['urlRequestRaw']
        fuwuISV = response.meta['fuwuISV']
        #fuwuISV['name'] = response.meta['fuwuISV.name']
        #fuwuISV['category'] = response.meta['fuwuISV.category']
        
        self.log(response.body,level = log.DEBUG)
        
        #format return format from puedo json to formal json 
        j=re.sub(r"(,|{)(\w+):", r"\1'\2':", response.body);
        j = re.sub(r"'", r'"', j)
        decodedResponse = json.loads(striphtml(j),datetime_format="%Y-%m-%d %H:%M:%S")
        
        currentPage = decodedResponse['currentPage']
        pageCount = decodedResponse['pageCount']
        
        if currentPage == pageCount:
            return 
        else:
           #form request, maybe try to use str.format
            urlRequestBuyer = urlRequestRaw.format(page = currentPage+1, count=pageCount)
            
            request = Request('http://fuwu.taobao.com' + urlRequestBuyer,
                         callback=self.parseBuyer) 
            request.meta['urlRequestRaw'] = urlRequestRaw
            yield request
            
            #extract buyer's data
            #items = []
            for buyer in decodedResponse['data']:
                item = FuwuPurchaseItem()                
                item['buyerNameMasked']=buyer['nick'].strip()
                item['buyerRank']=buyer['rateSum'].strip()
                item['purchaseTime'] = buyer['payTime']
                item['licLength'] = buyer['deadline'].strip()
                item['licVersion'] = buyer['version'].strip()
                item['fuwuISV']=fuwuISV
                yield item     
            
 

            
          
        

        
        
        
        

