import requests
from bs4 import BeautifulSoup
from time import sleep

#定义下载网页函数,返回html文本
def down_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    data = requests.get(url, headers=headers)
    data.encoding = 'utf-8'
    return data.text
#定义目录页函数,返回小说名字和每个章节的页面编码列表
def page_list(html):
    soup = BeautifulSoup(html,'lxml')
    title = soup.find('h1').text
    all_page= soup.find_all('dd')
    page_li = []
    for one_page in all_page:
        page = one_page.find('a')['href']
        page_li.append(page)
    return title,page_li
#抓取单章内容函数,返回章节名称,章节内容
def chapter(html):
    soup = BeautifulSoup(html,'lxml')
    title = soup.find('h1').text
    content = soup.find('div',id="content").get_text('\n')
    return title,content


# 写入文件
for i in range(10,11):
    book_num = '1_%s'%i
    print('正在下载第%s本小说'%book_num)
    first_url = 'http://www.biquge.tw/%s/'%book_num
    first_html = down_url(first_url)
    book_name,page_list = page_list(first_html)
    with open('%s.txt'%book_name,'a',encoding='utf-8') as f:
        for page in page_list:
            full_url = first_url[:21]+page
            new_html = down_url(full_url)
            title,content = chapter(new_html)
            print('正在下载:%s'%title)
            f.write('%s\n%s\n'%(title,content))
            sleep(1)