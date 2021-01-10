import all_API

stockx = all_API.StockX()

# stockx的使用示例

# search 方程的调用
# search(type, category, size, gender, year, lowest_range, highest_range, page)


type_list = ["adidas","air jordan","nike","other brands","luxury brands","collections"]

def find_id(shoetype,lowest_range, highest_range):
    id_list = []
    for i in range(1, 25):
        data = stockx.search(shoetype, "sneakers", None, None, None, lowest_range, highest_range, i)
        total_no = data["Pagination"]["total"]
        if total_no > 1000:
            highest_range = highest_range - 10
            find_id(shoetype,lowest_range, highest_range)
            for j in range(0, len(data["Products"])):
                id = data["Products"][j]["id"]
                id_list.append(id)
        else:
            for j in range(0, len(data["Products"])):
                id = data["Products"][j]["id"]
                id_list.append(id)
    return id_list, len(id_list)


#a = find_id("adidas", 350, 351)
#print(a)

#最高 90,000
#最低19


def find_url(shoetype, lowest_price, highest_price):
    url_list = []
    if highest_price - lowest_price > 1:
        average_price = (highest_price + lowest_price)/2
        for i in range(1, 25):
            data = stockx.search(shoetype, "sneakers", None, None, None, lowest_price, average_price, i)
            total_no = data["Pagination"]["total"]
            if total_no > 1000:
                find_url(shoetype,lowest_price, average_price)
            else:
                url = find_url(shoetype,lowest_price, average_price)
                url_list.append(url)
                find_url(shoetype, average_price, highest_price)
                #把这个URL存下来，把这个找到的价格作为最低价格，代入原来公式继续
    else:
    #那你就加一些参数（这个参数也是还用类似递归的方法 来切割），再去做原来range的
        for i in range(1,25):
            data = stockx.search(shoetype, "sneakers", None, None, None, lowest_price, highest_price, i)
            total_no = data["Pagination"]["total"]
            # 这边按照1到18 0.5为间隔做切割













##方程一，stockx.search

#data = stockx.search("adidas", "sneakers", "10.5", "women", "2019", "200", "300",1)
#data = stockx.search("alexander mcqueen,luxury brands", "sneakers", None, None, None, None, None,1)
#data = stockx.search("spizike,air jordan", None, None, None, None, None, None,"1")
#print(data)
#data = stockx.search(None, "sneakers", None, None, None, None, None,"1")

##方程二，stockx.extract_ID

#stockx.extract_ID(data)


##方程三，stockx.time_price_dataset
'''
data = stockx.time_price_dataset("7434fd9f-8f45-4beb-9d57-b641d253ff65")
print(data)
'''

##方程四，stockx.time_price
'''
time_price_data = stockx.time_price(data)
print(time_price_data)
'''


##方程五，stockx.item_info
'''
info = stockx.item_info("7434fd9f-8f45-4beb-9d57-b641d253ff65")
print(info)
'''

##方程六，stockx.item_sell
'''
sell = stockx.item_sell("7434fd9f-8f45-4beb-9d57-b641d253ff65")
print(sell)
'''

#stockx.item_info("7434fd9f-8f45-4beb-9d57-b641d253ff65")

#file = open('7434fd9f-8f45-4beb-9d57-b641d253ff65_info.txt', 'r')
#a = file.readlines()["Products"][0]
#print(a)

#stockx.item_info("7434fd9f-8f45-4beb-9d57-b641d253ff65")

#stockx.item_info("91a1cb8abf-13fd-4573-9ee0-f4e20435942c")

#stockx.item_info("a1a900e1-74f7-4039-848b-8e8eed7dbead")

#stockx.item_info("b80ff5b5-98ab-40ff-a58c-83f6962fe8aa")
#stockx.item_info("ca4bdbd5-3ab7-40d1-a1ef-5b9e628328be")
#stockx.item_info("eb10cb6e-2ea7-4dec-8c5e-a60261b36445")
#stockx.item_info("1a8b7d5b-9ed2-40d9-bb0d-7e9261cb97e8")
#stockx.item_info("216c7148-d0dd-4196-ab41-af576e3346f9")
#stockx.item_info("58d5b3ef-b90f-48d3-8d09-883f8a9cb7da")
#stockx.item_info("459e24e1-33a3-44ad-83ea-ab4107801e93")


#所有的鞋子都在这:
airjoranlist = ["one,air jordan","two,air jordan","three,air jordan","four,air jordan", 
                "five,air jordan","six,air jordan","seven,air jordan","eight,air jordan","nine,air jordan",
                "ten,air jordan","eleven,air jordan","twelve,air jordan","thirteen,air jordan","fourteen,air jordan",
                "fifteen,air jordan","sixteen,air jordan","seventeen,air jordan","eighteen,air jordan",
                "nineteen,air jordan","twenty,air jordan","twenty-one,air jordan","twenty-two,air jordan",
                "twenty-three,air jordan","twenty-four,air jordan","twenty-five,air jordan","twenty-six,air jordan",
                "twenty-seven,air jordan","twenty-eight,air jordan","twenty-nine,air jordan","thirty,air jordan",
                "thirty-one,air jordan","thirty-two,air jordan","thirty-three,air jordan","thirty-four,air jordan",
                "packs,air jordan","spizike,air jordan","other,air jordan"]

complexshoe = ["one,air force,nike","90,air max,nike","other,air max,nike","other,other,nike",
               "converse","luxury brands","new balance","puma","other,other brands","other,adidas"]

nike = ["dunk low,nike","dunk high,nike","kobe,nike","lebron,nike","97,air max,nike","1,air max,nike","kd,nike"]
adidaslist = ["yeezy","ultra boost,adidas","nmd,adidas","stan smith,adidas","iniki,adidas","eqt,adidas"]
otherbands = ["asics","diadora","li-ning","reebok","saucony","under armour"]


