import requests
from lxml import etree


for page in range(1, 3):
    url = f'https://cn.58.com/ershoufang/p{page}/?PGTID=0d100000-008d-2ff4-aa07-121f52dd52f4&ClickID=6'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }

    # 详情页的页面源码
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    # 房子的名称列表
    name_list = tree.xpath('//div[@class="property-content-title"]/h3/@title')

    # 房子详情页的url
    next_page_url = tree.xpath('//div[@class="property"]/a/@href')

    name_url_dict = dict(zip(name_list, next_page_url))

    for (name, next_page) in name_url_dict.items():
        # 房子详情的页面源码
        next_page_text = requests.get(url=next_page, headers=headers).text
        next_page_tree = etree.HTML(next_page_text)

        # 图片的url列表
        img_url = next_page_tree.xpath('//div[@class="gallery-image-wrap"]/img/@src')
        # 图片的数据,取第二张图片
        img_data = requests.get(url=img_url[0], headers=headers).content
        with open(f'./fang/{name}.jpg', 'wb') as f:
            f.write(img_data)