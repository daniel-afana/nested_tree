from lxml import html, etree
import grequests

urls = ['https://yandex.ru/referats/?t=gyroscope&s=',]

# Create a set of unsent Requests:
rqs = (grequests.get(u) for u in urls)


# Send them all at the same time:

resps = grequests.map(rqs)
# [<Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, None, <Response [200]>]

# parser = etree.HTMLParser(encoding='utf-8')
# htmltext = r.content.decode('utf-8')
# tree = etree.HTML(htmltext, parser)
#
#
#

tree = html.fromstring(resps[0].content)
description = tree.xpath('//div[@class="referats__text"]//text()')
print (description)


url1 = 'https://yandex.ru/referats/?t=gyroscope&s='
resp = requests.get(url1)
tree = html.fromstring(resp.content)
description = tree.xpath('//div[@class="referats__text"]//text()')