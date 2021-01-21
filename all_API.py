import requests
import os
from time import sleep
from random import randint
import urllib.request
import shutil
import re
import json

############################################### below are the headers information that we use to avoid getting caught  #########################################################

#different people will have different header files in case of clashing
header_list = []
f = open("headers_new.txt","r")
lines = f.readlines()
for line in lines:
    line = line.strip()
    header_list.append(line)

#print(header_list)

item_info_api = "https://stockx.com/api/products/%s/"
item_info_api_2 = "https://stockx.com/api/products/%s/%s/"

price_info = "chart?start_date=all&end_date=2020-05-03&intervals=100&format=highstock&currency=USD&country=US"
sell_info = "activity?state=480&currency=USD&limit=10000&page=%s&sort=createdAt&order=DESC&country=US"

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

class StockX():

    def __init__(self):
        self.x = 0
        self.y = 0
    
    def change_header(self,url,sent_headers,header_list):
        try:
            r = requests.get(url = url, headers=sent_headers)
            data = r.json()
        except Exception as e:
            caught = True
            print("Damn they caught us!! Switch to the next header. We have "+str(len(header_list))+" headers left")
            sleep(120)
            header_list.remove(header_list[0])
            #print(len(hl))
            send_headers = {
                "User-Agent": header_list[0],
                "Connection": "keep-alive",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8"}
            r = requests.get(url = url, headers=send_headers)
            data = r.json()
        
        return data

    def search(self,type, category, size, gender, year, lowest_range, highest_range, page):
        # 这个方程是一个搜索api，方程里的参数可以汇聚成一个url，注意参数之间不要加不必要的空格
        # 方程结果是导入参数出来符合参数的所有鞋的信息，包括id等等
        root_url = "https://stockx.com/api/browse?%ssort=recent_asks&order=DESC"
        #下面这几行是url拼接参数
        product_type = "_tags=%s&"
        productCategory = "productCategory=%s&"
        shoeSize = "shoeSize=%s&"
        gender_shoe = "gender=%s&"
        year_shoe = "year=%s&"
        market_shoe = "market.lowestAsk=range(%s|%s)&"
        page_shoe = "&page=%s"

        #counter = 0
        #stop_count = len(header_list)-1

        #url = "https://stockx.com/api/browse?_tags=eqt,%s&productCategory=%s&shoeSize=%s&gender=%s&year=%s&market.lowestAsk=range(%s|%s)&sort=recent_asks&order=DESC"
        #https://stockx.com/api/browse?_tags=adidas&productCategory=sneakers&shoeSize=10.5&gender=women&year=2019&market.lowestAsk=range(300|200)&&page=1sort=recent_asks&order=DESC
        temp_url = ""
        if type != None:
            temp_url = temp_url + product_type%type
        if category != None:
            temp_url = temp_url + productCategory%category
        if size != None:
            temp_url = temp_url + shoeSize%size
        if gender != None:
            temp_url = temp_url + gender_shoe%gender
        if year != None:
            temp_url = temp_url + year_shoe%year
        if (lowest_range != None) and (highest_range != None):
            temp_url = temp_url + market_shoe%(highest_range,lowest_range)
        if page != None:
            temp_url = temp_url + page_shoe%page
        URL = root_url%temp_url
        print(URL)
        data = None
        #print(hl)
        send_headers = {
            "User-Agent": header_list[0],
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}
        if len(header_list)!=0:
            while(True):
                if self.change_header(URL,send_headers,header_list):
                    data = self.change_header(URL,send_headers,header_list)
                    break
                else:
                    sleep(15)
                    continue
        else:
            print("We have used all headers!! Save current progress and abort the program!!")
            f = open("all_missing_shoe_list.txt","a")
            f.writelines(str(temp_url))
            f.close()
        return data
    
    




    def extract_ID(self,data):
        # 导入search得出的dataset，这个方程提取出所有符合搜索要求的鞋的id的总数量和具体id
        id_list = []
        #f = open(file_path, 'w')
        #total = data["Pagination"]["total"]
        #f.write(str(total) + "\n")
        for i in range(0, len(data["Products"])):
            #f.write(str(data["Products"][i]["id"])+"\n")
            id = data["Products"][i]["id"]
            id_list.append(id)
        #f.close()
        return data["Pagination"]["total"],id_list

    def time_price_dataset(self,item_id):
        # 方程导入想要搜索的鞋的id，得出Average price over time的rawdata
        URL = item_info_api_2%(item_id,price_info)
        r = requests.get(url = URL,headers=send_headers)
        raw_data = r.json()
        #print(data['series'][0]['data'][0][1])
        #data = raw_data['series'][0]['data']
        return raw_data

    # def price(self, data):
    #    # n = len(data['series'][0]['data'])
    #     n = len(data)
    #     price_list = []
    #     for x in range(n):
    #         i = data[x][1]
    #         price_list.append(i)
    #     return price_list

    def time_price(self, raw_data):
        # 方程导入未处理的Average price over time的rawdata，把表头去了，可利用进行调用处理 e.g.特定时间价格
        data = raw_data['series'][0]['data']
        return data

    def item_info(self,item_id):
        sleep(randint(50,150))
        # 方程导入item_id，得出item的详细信息
        path_info = "%s_info.txt"%item_id
        path_price = "%s_price.txt"%item_id
        path_pic = "%s_pic"%item_id
        if os.path.exists(path_info):
            os.remove(path_info)
            f_info = open(path_info, 'w')
            URL_info = item_info_api%item_id
            r_info = requests.get(url = URL_info,headers=send_headers)
            f_info.write(r_info.text)
        else:
            f_info = open(path_info, 'w')
            URL_info = item_info_api%item_id
            r_info = requests.get(url = URL_info,headers=send_headers)
            f_info.write(r_info.text)
        if os.path.exists(path_price):
                os.remove(path_price)
                f_price = open(path_price, 'w')
                URL_price = item_info_api_2%(item_id,price_info)
                r_price = requests.get(url = URL_price,headers=send_headers)
                price_data = r_price.json()
                f_price.write(str(price_data['series'][0]['data']))
        else:
            f_price = open(path_price, 'w')
            URL_price = item_info_api_2%(item_id,price_info)
            r_price = requests.get(url = URL_price,headers=send_headers)
            price_data = r_price.json()
            f_price.write(str(price_data['series'][0]['data']))
        if os.path.exists(path_pic):
            shutil.rmtree(path_pic)
            os.mkdir(path_pic)
            data = r_info.json()
            extr = re.compile(r'https?://[^\'|\"]*\.(?:jpg|png)[^\'|\"]*')
            result = extr.findall(str(data))
            #print(result)
            for i in range(0, len(result)):
                picture = "%s/pic_%s.png"%(path_pic,i)
                if os.path.exists(picture):
                    os.remove(picture)
                    pic_url = result[i]
                    print(pic_url)
                    f = open(picture,"wb")
                    response = requests.get(pic_url)
                    img = response.content
                    f.write(img)
                else:
                    pic_url = result[i]
                    print(pic_url)
                    f = open(picture,"wb")
                    response = requests.get(pic_url)
                    img = response.content
                    f.write(img)
        else:
            os.mkdir(path_pic)
            data = r_info.json()
            extr = re.compile(r'https?://[^\'|\"]*\.(?:jpg|png)[^\'|\"]*')
            result = extr.findall(str(data))
            for i in range(0, len(result)):
                picture = "%s/pic_%s.png"%(path_pic,i)
                pic_url = result[i]
                print(pic_url)
                f = open(picture,"wb")
                response = requests.get(pic_url)
                img = response.content
                f.write(img)


    def item_sell(self, item_id):
        # 方程导入item_id,得出历史交易信息
        pages = []
        for x in range(1,6):
            URL = item_info_api_2%(item_id, sell_info%str(x))
            print(URL)
            req = requests.get(url = URL,headers=send_headers)
            print(req.json())
        return pages



