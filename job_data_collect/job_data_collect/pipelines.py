# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import MySQLdb

class JobDataCollectPipeline:
    def process_item(self, item, spider):
        # 数据入库
        # 3. 创建SQL
        sql = 'insert into test (job_name) values(%s)'
        # 4. 执行SQL
        self.cursor.execute(sql,(item['job_name'],))
        # 5. 事务提交
        self.conn.commit()

    def open_spider(self,spider): # spider开启的时候回自动执行
        # 1. 创建连接
        self.conn = MySQLdb.Connection(
            host='localhost',  # mysql所在主机的ip
            port=3306,  # mysql的端口号
            user="root",  # mysql 用户名
            password="root",  # mysql 的密码
            db="scrapy",  # 要使用的库名
            charset="utf8"  # 连接中使用的字符集
        )
        # 2. 创建游标
        self.cursor = self.conn.cursor()

    def close_spider(self,spider): # spider 结束的时候会自动调用
        # 6. 关闭资源
        self.cursor.close()
        self.conn.close()
