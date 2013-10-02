#scrapy crawl tutorial  -o companies.json -t json

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from technopark.items import CompanyProp
import re


class TechnoparkSpider(BaseSpider):
    name = "technopark"
    allowed_domains = ["technopark.org"]

    start_urls = [
        "http://www.technopark.org/companies/a-z-listing?limit=0&limitstart=0&option=com_jobgroklist&view=companies&Itemid=111&filter_order111=postings_job_title&filter_order_Dir111="
    ]

    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        companies = hxs.select('//span[@class="companyName"]/a/text()').extract()
        companyraw = hxs.select('//div[@class="contents"]').extract()
        companydetails =[]
        #Email Regex
        reg_email = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')
        reg_link = re.compile (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        reg_phone = r'(phone)(?i)'
        reg_phoneno = re.compile(r'(\(?\+?(\d+)\)?-?(\d+)?-?(\d+)?\s?)')
        items =[]

        for idx,companydetail in enumerate(companyraw):
            ## Remove Span
            companydetail = re.sub('<span.*?</span>', '', unicode(companydetail))
            ## Remove HTML Tags 
            companydetail= re.sub(r'<[^>]*?>', '', unicode(companydetail))
            ## Remove Extra Spaces 
            companydetails.append(re.sub("[ \t]+"," ", unicode(companydetail)))

        for idx, company in enumerate(companies):
            item = CompanyProp()
            item['name'] = unicode(company).strip()
            item['desc'] = companydetails[idx]
            try:
                item['email'] = reg_email.findall(companydetails[idx])[0]
            except:
                item['email'] = ""
            try:
                item['link'] = reg_link.findall(companyraw[idx])[0]
            except:
                item['link'] = ""
            try:
                item['address'] = re.split(reg_phone,companydetails[idx])[0]
            except:
                item['address'] =""
            try:
                item['phone'] = re.split(reg_phone,companydetails[idx])[2].split('\n')[0]
            except:                
                item['phone'] =""
            items.append(item)
        
        return items 
        


# hxs.select('//div[@class="contents"]/text() and descendant::span[@class="companyName"]').extract()


# f=open('j.txt','w')
# f.write(', '.join([x.strip() for x in ' '.join(companydetails[0].split(' ')).replace('\t', '').split(',')]))
# f.close()
# f=open('j.txt','w')
# f.write(companydetail[0])
# f.close()
