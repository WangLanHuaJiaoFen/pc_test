import requests
from lxml import etree


for index in range(1, 11):
    if index == 1:
        url = 'https://pic.netbian.com/4kdongman/'
    else:
        url = 'https://pic.netbian.com/4kdongman/' + f'index_{index}.html'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }

    # 在页面源码出现文字乱码时转换编码
    page = requests.get(url=url, headers=headers)
    page.encoding = 'GBK'
    # 或者采用通用的解决乱码的方案
    # page_text.encode("iso-8859-1").decode('gbk')
    page_text = page.text

    tree = etree.HTML(page_text)
    img_src = tree.xpath('//div[@class="slist"]/ul[@class="clearfix"]/li/a/img/@src')
    img_name_list = tree.xpath('//div[@class="slist"]/ul[@class="clearfix"]/li/a/img/@alt')

    img_url_list = []
    for img in img_src:
        img_url = "https://pic.netbian.com" + img
        img_url_list.append(img_url)

    img_dict = dict(zip(img_url_list, img_name_list))

    for img_url, img_name in img_dict.items():
        img_data = requests.get(url=img_url).content
        with open(f'./acg_img/{img_name}.jpg', 'wb') as f:
            f.write(img_data)
