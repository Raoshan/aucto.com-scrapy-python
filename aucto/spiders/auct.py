import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.aucto.com/lots?page=1&items_per_page=20&status=active|paused&keyword={}'

class AuctSpider(scrapy.Spider):
    name = 'auct'
    allowed_domains = ['aucto.com']
    def start_requests(self):        
        for index in df:            
            yield scrapy.Request(base_url.format(index),cb_kwargs={'index':index})

    def parse(self, response, index):
        """Pagination"""
        total_pages = response.xpath("//ul[@class='pagination']/li[last()-1]/a/text()").get()
        # print(total_pages)
        current_page = response.xpath("//li[@class='active']/a/text()").get()
        # print(current_page)
        url = response.url  
        # print(url)    
        
        if total_pages and current_page:            
            if int(current_page) ==1:                
                for i in range(2, int(total_pages)+1):                   
                    min = 'page='+str(i-1)
                    max = 'page='+str(i)
                    url = url.replace(min,max) 
                    # print(url)                   
                    yield response.follow(url, cb_kwargs={'index':index})
                    

        links = response.xpath("//div[@class='col-xs-12 col-sm-6']/a")
        for item in links:
            link = "https://www.aucto.com"+item.css('a::attr(href)').get()           
            title = item.css(".lot-title::text").get()          
            item_type = index
            date = item.css("div.timer::text").get()
            date = date.replace("${ getEndIn('","")
            auction_date = date.replace("') }","")          
            image = item.css(".lot-photo::attr(style)").get()              
            image_link = image[22:-1]      
        
            yield{
                'product_url' : link,
                'item_type' : item_type,
                'image_link' : image_link,
                'product_name': title,
                'auction_date' : auction_date,
                'location' : "US",            
                'lot_id' : "",
                'auctioner' : "",
                'website' : "aucto"
            }
            


    