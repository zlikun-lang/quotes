# 实现一个代理IP池爬虫，数据来源：http://www.xicidaili.com/nn ，目前只取第一页
import requests
from pyquery import PyQuery as pq

DEFAULT_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'


# 后期将整个逻辑做成一个定时任务，比如每分钟检测一次，将有效结果更新到缓存或数据库中

def get_proxies():
    try:
        # 下载代理列表页
        response = requests.get('http://www.xicidaili.com/nn',
                                headers={
                                    'User-Agent': DEFAULT_UA,
                                    'Host': 'www.xicidaili.com',
                                })
        response.raise_for_status()
        html = response.text
        # 解析该页，获取全部代理IP及协议
        for tr in pq(html).find('tr:gt(0)'):
            tds = pq(tr).find('td')
            yield (tds[5].text.strip(), tds[1].text.strip(), tds[2].text.strip())


    except Exception as e:
        print(e)


def validate():
    lst = []
    count = 1
    for protocol, ip, port in get_proxies():
        try:
            if requests.get('https://baidu.com/',
                            headers={'User-Agent': DEFAULT_UA},
                            proxies={
                                protocol: ':'.join([ip, port])
                            }, timeout=0.3).status_code == 200:
                lst.append('{}://{}:{}'.format(protocol, ip, port))
        except Exception as e:
            print(e)
        count += 1

    # 有效代理列表, 检查代理总数, 失败代理总数
    return lst, count, count - len(lst)


if __name__ == '__main__':
    # print(requests.get('https://baidu.com/').text)

    lst, count, failures = validate()
    print('一共检测 {} 个代理IP，其中 {} 个有效!'.format(count, len(lst)))
    print('输出有效代理IP:')
    [print(proxy) for proxy in lst]
