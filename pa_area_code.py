# 爬虫爬取国家统计局的region_code
import requests
import time
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36',
    'Cookie': 'AD_RS_COOKIE=20080918; _trs_uv=kahvgie3_6_fc6v'
}
# 设置一些全局变量用于使用 city,city_id,country,country_id,town_id,town,village_id,village

province = ""
province_id = ""
city = ""
city_id = ""
country = ""
country_id = ""
town = ""
town_id = ""
village = ""
village_id = ""


def getProvince():  # 获取省级
    response = requests.get('http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/index.html', headers=headers)
    response.encoding = 'utf-8'
    text = response.text
    html = etree.HTML(text)
    trs = html.xpath('//tr[@class="provincetr"]/td')
    for tr in trs[14:31]:  # 最后一个是空值
        global province
        province = tr.xpath('./a/text()')[0]
        page = tr.xpath('./a/@href')[0]
        global province_id
        province_id = page.split('.')[0]
        print(province, province_id)
        province_url = 'http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/' + page
        file_name = province+" region_code"
        dic_name = file_name + '.csv'
        file_path = r'D:\QMDownload\\' + dic_name
        fp = open(file_path,'a')
        fp.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % ('代码', '名称', '代码', '名称', '代码', '名称', '代码', '名称'))
        getCity(province_url,fp)
        fp.close()


def getCity(province_url,fp):
    # province_url = 'http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/35.html'
    response2 = requests.get(province_url, headers=headers)
    response2.encoding = 'utf-8'
    text2 = response2.text
    html2 = etree.HTML(text2)
    trs = html2.xpath('//tr[@class="citytr"]')
    for tr in trs:
        page = tr.xpath('./td[1]/a/@href')[0]
        city_url = 'http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/' + page
        global city_id
        city_id = tr.xpath('./td[1]/a/text()')[0]
        global city
        city = tr.xpath('./td[2]/a/text()')[0]
        print(city, city_id)
        getCountry(city_url,fp)
        # time.sleep(0.5)


def getCountry(city_url,fp):  # 县区级
    response3 = requests.get(city_url, headers=headers)
    response3.encoding = 'utf-8'
    text3 = response3.text
    html3 = etree.HTML(text3)
    trs = html3.xpath('//tr[@class="countytr"]')
    for tr in trs:  # 福建泉州金门县有点问题
        try:
            page = tr.xpath('./td[1]/a/@href')[0]
            country_url = 'http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/' + province_id + '/' + page
            global country_id
            country_id = tr.xpath('./td[1]/a/text()')[0]
            global country
            country = tr.xpath('./td[2]/a/text()')[0]
            print(country, country_id)
            getTown(country_url,fp)
            # time.sleep(0.1)
        except:
            pass


def getTown(country_url,fp):  # 乡镇级别
    response4 = requests.get(country_url, headers=headers)
    response4.encoding = 'utf-8'
    text4 = response4.text
    html4 = etree.HTML(text4)
    trs = html4.xpath('//tr[@class="towntr"]')
    for tr in trs:
        try:
            page = tr.xpath('./td[1]/a/@href')[0]
            substring = country_url.rsplit('/', 1)[0]
            town_url = substring + "/" + page
            global town_id
            town_id = tr.xpath('./td[1]/a/text()')[0]
            global town
            town = tr.xpath('./td[2]/a/text()')[0]
            print(town, town_id)
            getVillage(town_url,fp)
            # time.sleep(0.5)
        except:
            pass


def getVillage(town_url,fp):  # 村级
    response5 = requests.get(town_url, headers=headers)
    response5.encoding = 'utf-8'
    text5 = response5.text
    html5 = etree.HTML(text5)
    trs = html5.xpath('//tr[@class="villagetr"]')
    for tr in trs:
        try:
            global village_id
            village_id = tr.xpath('./td[1]/text()')[0]
            global village
            village = tr.xpath('./td[3]/text()')[0]
            fp.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (
                city_id, city, country_id, country, town_id, town, village_id, village))
            print(village, village_id)

        except:
            pass


# city,city_id,country,country_id,town_id,town,village_id,village

if __name__ == '__main__':

    getProvince()