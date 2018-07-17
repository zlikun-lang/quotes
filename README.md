# Scrapy 学习工程

- https://scrapy.org/
- https://docs.scrapy.org/en/latest/

#### 创建工程
```
# 使用默认模板创建工程
$ scrapy startproject quotes
New Scrapy project 'quotes', using template directory 'd:\\program\\python\\python37\\lib\\site-packages\\scrapy\\templates\\project', created in:
    ...

$ cd quotes

# 生成爬虫，注意爬虫名称不能与工程名称相同
$ scrapy genspider quote quotes.toscrape.com
Created spider 'quote' using template 'basic' in module:
  quotes.spiders.quote
```

#### 目标网站
- http://quotes.toscrape.com/

爬虫任务
- 获取网页中的名言、作者、标签信息
```
# 运行爬虫
$ scrapy crawl quote
```
- 将爬取的数据生成json/xml/csv等格式文件保存
```
# 运行爬虫，将结果保存成一个JSON文件(组织为一个数组)
$ scrapy crawl quote -o .data/quotes.json
# 运行爬虫，将结果保存成一个JSON文件(一条记录一行) 
$ scrapy crawl quote -o .data/quotes.jl
# 运行爬虫，将结果保存成一个XML文件
$ scrapy crawl quote -o .data/quotes.xml
# 运行爬虫，将结果保存成一个CSV文件
$ scrapy crawl quote -o .data/quotes.csv
```
- 将爬取的数据写入MongoDB
```
# 运行爬虫
$ scrapy crawl quote
```
