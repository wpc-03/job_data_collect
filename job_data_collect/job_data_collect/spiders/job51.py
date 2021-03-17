import scrapy,re,json
from ..items import JobDataCollectItem

#  爬虫代码
class Job51Spider(scrapy.Spider):
    # 必须有
    name = 'job51'
    # 必须有
    allowed_domains = ['hhhhh.com']
    # start_urls = ['http://hhhhh.com/']

    # 如果 start_urls 不存在，必须写start_requests
    def start_requests(self): # 用于访问列表页---有多个目标数据（详情页链接）
        url = 'https://search.51job.com/list/210200,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25BC%2580%25E5%258F%2591,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    # 解析方法  用于解析列表页
    def parse(self, response):
        # print('我进入到了解析方法')
        # 解析操作
        detail_urls=re.findall('__SEARCH_RESULT__ = (.*?)</script>',response.text)[0]
        detail_urls = json.loads(detail_urls)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            # 'referer':''
        }
        for outline_data in detail_urls['engine_search_result']:
            # 获取到详情页的链接
            url2 = outline_data['job_href']
            yield scrapy.Request(url=url2,callback=self.details_parse,dont_filter=True,headers=self.headers)

    # 解析详情页
    def details_parse(self,response):  # scrapy 中的xpath预热默认打包成 Selector  需要进行序列化
        # 创建Item对象
        item = JobDataCollectItem()
        try:  # 如果出现异常
            # 工作名称，职位名称
            item['job_name'] = response.xpath('//h1/@title').extract()[0] # 序列化
            # 公司名称
            item['company_name'] = response.xpath('//a[@class="catn"]/@title')[0].extract()
            # 基本信息     需要清洗
            item['base_message'] = response.xpath('//p[@class="msg ltype"]/@title')[0].extract()
            # 公司地址
            item['company_address'] = response.xpath('//p[@class="fp"]/text()')[0].extract()
            # 公司详情
            item['company_details_message'] = response.xpath('string(//div[@class="tmsg inbox"])')[0].extract()
            # 职位信息  需要清洗
            item['job_message'] = response.xpath('string(//div[@class="bmsg job_msg inbox"])').extract()
            # 薪资范围  数据格式化
            item['salary'] = response.xpath('//div[@class="cn"]/strong/text()')[0].extract()
            yield  item # 符合规范  引擎通过检测，发现数据是字典类型，将数据自动转发给Pipeline
        except Exception as e:  # 不要了
            print('有错误', e)


