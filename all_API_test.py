import all_API
from time import sleep
import os
###TODO:
#add more documentation on what this file does
#reexamine type list to make it more holistic
#need try except headers and print warning in all_API search, after finished deleting the header information in all_API_test

############################################### below is to make object stockx #################################################################################################

stockx = all_API.StockX()

############################################### below are all the data type needed to segment the APIs  ########################################################################

year_dict = {"0":4374,"1985":3,"1986":2,"1988":1,"1989":5,"1990":2,"1991":5,"1992":5,"1993":8,"1994":10,"1995":8,
"1996":7,"1997":10,"1998":10,"1999":21,"2000":23,"2001":51,"2002":63,"2003":96,"2004":132,"2005":226,
"2006":292,"2007":310,"2008":510,"2009":433,"2010":353,"2011":377,"2012":610,"2013":939,"2014":1177,
"2015":1436,"2016":2575,"2017":4633,"2018":6488,"2019":7112,"2020":6193,"2021":75}
#by brand
brand_dict = {"Nike":21229,"adidas":7955,"Jordan":5735,"Vans":2195,"New Balance":1953,"Converse":1308,
"Reebok":1293,"Puma":1241,"ASICS":884,"Balenciaga":465,"Under Armour":381,"Saucony":360,
"OFF-WHITE":225,"Gucci":217,"Fila":195,"Timberland":193,"Diadora":180,"Dior":156,"Clarks":137,
"BAPE":135,"Yeezy":116,"Louis Vuitton":115,"Ewing Athletics":97,"Li-Ning":94,"K-Swiss":89,
"Alexander McQueen":87,"Dr. Martens":85,"DC Shoes":82,"Mizuno":75,"Crocs":58,"Versace":57,
"Karhu":50,"Salomon":46,"FEAR OF GOD":44,"Hoka One One":38,"Suicoke":38,"John Geiger":37,
"KangaROOS":37,"Common Projects":32,"Burberry":31,"Chanel":29,"Saint Laurent":26,
"Polo Ralph Lauren":25,"Supra":25,"Onitsuka Tiger":24,"Hummel":21,"Le Coq Sportif":21,
"Sonra":20,"The North Face":20,"es":20,"Brooks":19,"Birkenstock":17,"Filling Pieces":17,
"Prada":17,"Rhude":13,"Superga":12,"Mercer":11,"Pro Keds":11,"Hender Scheme":10,"Osiris":10,
"Represent":10,"UGG":10,"Veja":10,"Sandalboyz":9,"Tretorn":9,"And1":8,"Kith":8,"PF Flyers":8,
"Sperry":8,"Cole Haan":7,"Globe":7,"Big Baller Brand":6,"On":6,"Anta":5,"Athletic Propulsion Labs":5,
"Brandblack":5,"CLAE":5,"Ellesse":5,"Lakai":5,"Ubiq":5,"Chalk Line Apparel":4,"Circa":4,"Dsquared2":4,
"Gravis":4,"Ice Cream":4,"Merrell":4,"Moncler":4,"Padmore & Barnes":4,"Starwalk":4,
"Stepney Workers Club":4,"Tommy Hilfiger":4,"Aime Leon Dore":3,"Arc Originals":3,"Boris Bidjan Saberi":3,
"Diemme":3,"Etonic":3,"FTP":3,"GANT":3,"Kickers":3,"Lacoste":3}
#by gender
gender_dict={"men":37067,"women":6200,"child":3243,"preschool":958,"toddler":875,"infant":73,"unisex":4}

year_list = list(year_dict.keys())
print(year_list)
#brand_list = list(brand_dict.keys())
brand_list = ['nike','adidas','jordan','vans','new balance','under armour','converse','reebok','puma','balenciaga','asics',
'saucony','off-white','gucci','fila','other','timberland','diadora','dior','clarks','bape','yeezy','louis vuitton',
'ewing athletics','li-ning','k-swiss','dr. martens','dc shoes','mizuno','crocs','versace','karhu','salomon','fear of god','hoka one one'
'suicoke','john-geiger','kangaroos','common projects','burberry','chanel','saint laurent','polo ralph lauren','supra','onitsuka tiger',
'hummel','le coq sportif','sonra','the north face','es','brooks','birkenstock','filling pieces','prada','rhude','superga','mercer',
'pro keds','hender scheme','osiris','represent','ugg','sandalboyz','tretorn','and1','kith','pf flyers','sperry','cole haan','globe','big baller brand',
'on','anta','athletic propulsion labs','brandblack','clae','ellesse','lakai','ubiq','chalk line apparel','circa','dsquared2','gravis','merrell','moncler','starwalk',
'stepney workers club','tommy hilfiger','aime leon dore','arc originals','boris bidjan saberi','diemme','etonic','ftp','gant','kickers','lacoste']
print(brand_list)   #brand CANNOT have capital letters in!
                    # some brandes' API are catogorized in other, e.g, 
                    #"https://stockx.com/api/browse?_tags=other" 
                    #instead of "https://stockx.com/api/browse?_tags=alexander-mcqueen"
#clean brand_list
gender_list = list(gender_dict.keys())
print(gender_list)
#release_time_list = list(release_time_dict.keys())
#print(release_time_list)
#I highly doubt if we need to examin the brand list and compare it with the type list over here
type_list = ["adidas","air-jordan","nike","other-brands","luxury-brands","collections"]  
shoeSize_list = [1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16]

############################################## below is the function that calls search to segment APIs and extract IDs ########################################################

def find_id(shoeType, year, gender,shoeSize):
    '''
    takes in these variables: shoeType -> brand_list -> all the brands for the shoes
                               year    -> year_list -> all release years for the shoes
                               gender  -> gender_list -> all genders for the shoes
                               shoeSize -> shoeSize_list -> all shoe sizes for the shoes
                               missing -> all_missing_shoe_list.txt -> txt file used to save shoes that cannot be segmented to under 1000
    '''                          
    #with the cleaned data sets try to have all combinations of api that limit return results to <1000
    #start from root url
    #if >1000, add year
    #if >1000, add gender
    #if >1000, add shoeSize
    #if >1000, add the link to missing and we can print it out and see for ourselves
    id_list = []
    f_missing = open("all_missing_shoe_list.txt","a")
    f_no_id = open("no_id_file.txt","a")
    root_url = "https://stockx.com/api/browse?_tags="
    for i in range(len(shoeType)):
        #first go through the type list and see if request by brand will limit the number of results under 1000
        data = stockx.search(shoeType[i], "sneakers", None, None, None, None, None, None)
        total_no = data["Pagination"]["total"]
        sleep(5) #after every api call, sleep for 15 secs
        if total_no > 1000:
            print("Oops! Too many shoes for "+str(shoeType[i]))
            print("Narrow search with year")
            for j in range(len(year)):
                #if not, add another limit year and see if that will limit the number of results under 1000
                print("The count for year is "+str(j))
                print(type(j))
                data = stockx.search(shoeType[i], "sneakers", None, None, year[j], None, None, None)
                total_no = data["Pagination"]["total"]
                sleep(5) #after every api call, sleep for 15 secs
                if total_no >1000:
                    print("Oops! Too many shoes for "+str(shoeType[i])+ " in " + str(year[j]))
                    print("Narrow search with gender")
                    for k in range(len(gender)):
                        #if not, add another limit gender and see if that will limit the number of results under 1000
                        data = stockx.search(shoeType[i], "sneakers", None, gender[k], year[j], None, None, None)
                        total_no = data["Pagination"]["total"]
                        sleep(5) #after every api call, sleep for 15 secs
                        if total_no>1000:
                            #if not, add another limit shoe size and see if that will limit the number of results under 1000
                            print("Oops! Too many shoes for "+str(shoeType[i])+ " in " + str(year[j])+ " for "+str(gender[k]))
                            print("Narrow search with shoe size")
                            for n in range(len(shoeSize)):
                                data = stockx.search(shoeType[i], "sneakers", shoeSize[n], gender[k], year[j], None, None, None)
                                total_no = data["Pagination"]["total"]
                                sleep(5) #after every api call, sleep for 15 secs
                                if total_no>1000:
                                    #at this point we should cover most shoes, but if not, write the url into file all_missing_shoe_list.txt for further examination
                                    print("Oops! Too many shoes for "+str(shoeType[i])+ " in " + str(year[j])+ " for"+ str(gender[k])+" in size "+
                                    shoeSize[n] +". Put in file and check out later with more detailed segmentation")
                                    f_missing.writelines(root_url+str(shoeType[i])+"&productCategory=sneakers&shoeSize="+shoeSize[n]+"&gender="+gender[k]+"&year="+year[j]+
                                        "&market.lowestAsk=range(300|200)&&page=1sort=recent_asks&order=DESC")
                                    f_missing.close()
                                else:
                                    print("Yeah! Extracting ID for "+ str(shoeType[i])+ " in " + str(year[j])+ " for "+ str(gender[k])+" in size "+shoeSize[n])
                                    for d in range(0, len(data["Products"])):
                                        print(d)
                                        try:
                                            id = data["Products"][d]["id"]
                                            if id not in id_list:
                                                id_list.append(id)
                                        except IndexError:
                                            print("Ouch there's no id for this shoe, something might be wrong......")
                                            f_no_id.writelines(str(shoeType[i])+" in "+str(year[j])+" for "+str(gender[k])+" in size "+str(shoeSize[n])+" has no id.")
                                    print("Total id number is : "+ str(len(id_list)))
                                    path_id = "%s_%s_%s_%s_id.txt" %(shoeType[i],year[j],gender[k],shoeSize[n])
                                    if os.path.exists(path_id):
                                        os.remove(path_id)
                                        f = open(path_id, 'w')
                                        for i in id_list:
                                            f.write(i + "\n")
                                    else:
                                        f = open(path_id, 'w')
                                        for i in id_list:
                                            f.write(i + "\n")
                        else:
                            print("Yeah! Extracting ID for "+ str(shoeType[i])+ "in " + str(year[j])+ " for "+ str(gender[k]))
                            for d in range(0, len(data["Products"])):
                                print(d)
                                try: 
                                    id = data["Products"][d]["id"]
                                    if id not in id_list:
                                        id_list.append(id)
                                except IndexError:
                                    print("Ouch there's no id for this shoe, something might be wrong......")
                                    f_no_id.writelines(str(shoeType[i])+" in "+str(year[j])+" for "+str(gender[k])+" has no id.")
                            print("Total id number is : "+ str(len(id_list)))
                            path_id = "%s_%s_%s_id.txt" %(shoeType[i],year[j],gender[k])
                            if os.path.exists(path_id):
                                os.remove(path_id)
                                f = open(path_id, 'w')
                                for i in id_list:
                                    f.write(i + "\n")
                            else:
                                f = open(path_id, 'w')
                                for i in id_list:
                                    f.write(i + "\n")
                else:
                    print("Yeah! Extracting ID for "+ str(shoeType[i])+ "in " + str(year[j]))
                    for d in range(0, len(data["Products"])):
                        print(d)
                        try: 
                            id = data["Products"][d]["id"]
                            if id not in id_list:
                                id_list.append(id)
                        except IndexError:
                            print("Ouch there's no id for this shoe, something might be wrong......")
                            f_no_id.writelines(str(shoeType[i])+" in "+str(year[j])+" for "+" has no id.")
                    print("Total id number is : "+ str(len(id_list)))
                    path_id = "%s_%s_id.txt" %(shoeType[i],year[j])
                    if os.path.exists(path_id):
                        os.remove(path_id)
                        f = open(path_id, 'w')
                        for i in id_list:
                            f.write(i + "\n")
                    else:
                        f = open(path_id, 'w')
                        for i in id_list:
                            f.write(i + "\n")
        else:
            print("Yeah! Extracting ID for "+ str(shoeType[i]))
            for d in range(0, len(data["Products"])):
                print(d)
                try: 
                    id = data["Products"][d]["id"]
                    if id not in id_list:
                        id_list.append(id)
                except IndexError:
                    print("Ouch there's no id for this shoe, something might be wrong......")
                    f_no_id.writelines(str(shoeType[i])+" has no id.")
            print("Total id number is : "+ str(len(id_list)))
            path_id = "%s_id.txt" %(shoeType[i])
            if os.path.exists(path_id):
                os.remove(path_id)
                f = open(path_id, 'w')
                for i in id_list:
                    f.write(i + "\n")
            else:
                f = open(path_id, 'w')
                for i in id_list:
                    f.write(i + "\n")
    return id_list

<<<<<<< HEAD
print(find_id(["adidas"],[2010],["women"],[10.5]))
=======

#print(find_id(["adidas"],[2010],["women"],[10.5]))

#print(find_id(["adidas"],[2020],["women"],[1]))

print(find_id(["new balance"],year_list,gender_list,shoeSize_list))
>>>>>>> 30f4240558f47ab4b6ebf0241f19afe06fec08db


'''def find_id(shoetype,lowest_range, highest_range):
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

data = stockx.time_price_dataset("7434fd9f-8f45-4beb-9d57-b641d253ff65")
print(data)


##方程四，stockx.time_price
time_price_data = stockx.time_price(data)
print(time_price_data)


##方程五，stockx.item_info
info = stockx.item_info("7434fd9f-8f45-4beb-9d57-b641d253ff65")
print(info)
##方程六，stockx.item_sell
sell = stockx.item_sell("7434fd9f-8f45-4beb-9d57-b641d253ff65")
print(sell)
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
otherbands = ["asics","diadora","li-ning","reebok","saucony","under armour"]'''


