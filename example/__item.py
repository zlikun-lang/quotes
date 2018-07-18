# https://docs.scrapy.org/en/latest/topics/items.html#working-with-items
import scrapy


class MyItem(scrapy.Item):
    # 未声明的字段，无法使用(赋值等)
    name = scrapy.Field()
    age = scrapy.Field()
    job = scrapy.Field()

    pass


item = MyItem(name='zlikun', age=17)
print(item)

item['job'] = 'Dev'
print(item)

# True
print('job' in item)

# ItemsView({'age': 17, 'job': 'Dev', 'name': 'zlikun'})
print(item.items())
# Dev
print(item.get('job'))
