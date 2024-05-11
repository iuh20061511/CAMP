# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymongo
import json
import csv
import mysql.connector
from bson.objectid import ObjectId
import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem



class JsonDBUnitopPipeline:
    def process_item(self, item, spider):
        self.file = open('jsondatabooks.json','a',encoding='utf-8')
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        self.file.close()
        return item




import pandas as pd

class CSVDBBookToScrapePipeline:
     def __init__(self):
        self.csv_file = open('output.csv', 'w', newline='', encoding='utf-16')
        self.csv_writer = csv.writer(self.csv_file, delimiter='$')
        header = ['title', 'price', 'instock', 'urlBook', 'categories','star_rating', 'upc','price_exc','price_inc','tax']
        self.csv_writer.writerow(header)

     def process_item(self, item, spider):
        course_data = [
            item.get('title', ' '),
            item.get('price', ' '),
            item.get('instock', ' '),
            item.get('urlBook', ' '),
            item.get('categories', ' '),
            item.get('star_rating', ' '),
            item.get('upc', ' '),
            item.get('price_exc', ' '),
            item.get('price_inc', ' '),
            item.get('tax', ' ')
        ]
        self.csv_writer.writerow(course_data)
        return item

     def close_spider(self, spider):
        self.csv_file.close()



class MongoDBPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')  
        self.db = self.client["dbbook"]

    def process_item(self, item, spider):
        collection = self.db['tbl_book']
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error in Pipeline:{e}")
        

class MySQLPipline:
    # Tham khảo: https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-mysql/
        def __init__(self):
            self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = '123456',
                database = 'dbbook'
            )

        ## Create cursor, used to execute commands
            self.cur = self.conn.cursor()
        ## Create quotes table if none exists
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tbl_book(
                id int NOT NULL auto_increment, 
                title VARCHAR(255),
                price VARCHAR(255),
                star_rating VARCHAR(255),
                instock VARCHAR(255),
                urlBook VARCHAR(2000),
                categories VARCHAR(50),
                upc VARCHAR(50),
                PRIMARY KEY (id)
                            
            )
            """)
 
        def process_item(self, item, spider):
            ## Define insert statement
            self.cur.execute("""  INSERT INTO  tbl_book(title, price, star_rating, instock, urlBook, categories, upc)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
                item['title'],
                item['price'],
                item['star_rating'],
                item['instock'],
                item['urlBook'],
                item['categories'],
                item['upc']

            ))
            ## Execute insert of data into database
            self.conn.commit()
            return item
        
        def close_spider(self, spider):

            ## Close cursor & connection to database 
            self.cur.close()
            self.conn.close()
        pass


class PostgresPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = '123456' 
        database = 'dbbook'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tbl_book (
                id serial PRIMARY KEY,
                title VARCHAR(255),
                price VARCHAR(255),
                star_rating VARCHAR(255),
                instock VARCHAR(255),
                urlBook VARCHAR(2000),
                categories VARCHAR(50),
                upc VARCHAR(50)
            )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        query = """
        INSERT INTO tbl_book (title, price, star_rating, instock, urlBook, categories, upc) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Chuẩn bị các giá trị từ đối tượng item
    
        values = (
        item['title'],
        item['price'],
        item['star_rating'],
        item['instock'],
        item['urlBook'],
        item['categories'],
        item['upc']
    )

# Thực thi lệnh INSERT
        self.cur.execute(query, values)


        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()