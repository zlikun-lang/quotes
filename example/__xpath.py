# xpath selector
# https://docs.scrapy.org/en/latest/topics/selectors.html
# https://www.w3.org/TR/xpath/all/
# https://www.w3.org/TR/2017/REC-xpath-31-20170321/


from scrapy.selector import Selector
from scrapy.http import HtmlResponse

body = '<html><body><span>good</span></body></html>'
# ['good']，取span标签的内容
print(Selector(text=body).xpath('//span/text()').extract())

# 下面是scrapy封装的等价写法
response = HtmlResponse(url='http://example.com', body=body.encode('utf-8'))
# ['good']
print(Selector(response=response).xpath('//span/text()').extract())

# ['good']
print(response.selector.xpath('//span/text()').extract())

html = """
<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
   <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
   <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
   <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
  </div>
 </body>
</html>
"""

response = HtmlResponse(url='http://example.com', body=html.encode('utf-8'))

# 返回选择器对象
# [<Selector xpath='//title/text()' data='Example website'>]
print(response.selector.xpath('//title/text()'))
# ['Example website']，提取内容列表
print(response.selector.xpath('//title/text()').extract())
# Example website，提取列表第一条
print(response.selector.xpath('//title/text()').extract_first())
# Example website，提取列表第一条，只是换种写法，不知道上面的写法会不会效率更高一些
print(response.selector.xpath('//title/text()').extract()[0])

# css选择器和xpath选择器混用，选择img标签，提取src属性
# ['image1_thumb.jpg', 'image2_thumb.jpg', 'image3_thumb.jpg', 'image4_thumb.jpg', 'image5_thumb.jpg']
print(response.css('img').xpath('@src').extract())
# 等价写法
# ['image1_thumb.jpg', 'image2_thumb.jpg', 'image3_thumb.jpg', 'image4_thumb.jpg', 'image5_thumb.jpg']
print(response.css('img::attr(src)').extract())
# ['image1_thumb.jpg', 'image2_thumb.jpg', 'image3_thumb.jpg', 'image4_thumb.jpg', 'image5_thumb.jpg']
print(response.xpath('//img/@src').extract())

# Name: My image 1 ，取id为images的div下的第一个a标签内容
print(response.xpath('//div[@id="images"]/a/text()').extract_first())
# 取id为images的div下的所有a标签内容
print(response.xpath('//div[@id="images"]/a/text()').extract())

# image1.html，提取属性值
print(response.xpath('//div[@id="images"]/a/@href').extract_first())
# 如果属性值没有，返回：None
print(response.xpath('//div[@id="images"]/a/@class').extract_first())
# 如果内容为空，也返回：None
print(response.xpath('//div[@id="images"]/img/text()').extract_first())
# 查找的标签不存在，返回：None
print(response.xpath('//div[@id="not-exists"]/text()').extract_first())
# 当查找的元素不存在时，返回：默认值
print(response.xpath('//div[@id="not-exists"]/text()').extract_first(default='not-found'))
# 父级元素不存在时，也返回：None
print(response.xpath('//div[class="main"]/div[@id="not-exists"]/text()').extract_first())

# Name: My image 1 ，如果单独取内容或属性时，不需要/开头
print(response.xpath('//div[@id="images"]/a')[0].xpath('text()').extract_first())
# image1.html
print(response.xpath('//div[@id="images"]/a')[0].xpath('@href').extract_first())

# 查询包含href属性且该属性值包含image2关键字的a标签
# <a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>
print(response.xpath('//a[contains(@href, "image2")]').extract_first())
# Name: My image 2 ,只取文本内容，子标签被忽略
print(response.xpath('//a[contains(@href, "image2")]/text()').extract_first())

# 除了使用contains还可以使用正则表达式
# Name: My image 1
print(response.xpath('//a[re:test(@href, "image\d")]/text()').extract_first())

# images，表示有$cnt个a标签为子标签的div元素的属性id值
print(response.xpath('//div[count(a)=$cnt]/@id', cnt=5).extract_first())

# 按索引定位元素(索引从1开始，且不能为0和负数，否则返回None)
# Name: My image 1
print(response.xpath('//div[@id="images"]/a[1]/text()').extract_first())
# Name: My image 2
print(response.xpath('//div[@id="images"]/a[2]/text()').extract_first())
# Name: My image 5 ，取最后的元素，使用last()函数
print(response.xpath('//div[@id="images"]/a[last()]/text()').extract_first())
# Name: My image 4 ，还可以通过last()-1倒推
print(response.xpath('//div[@id="images"]/a[last()-1]/text()').extract_first())
