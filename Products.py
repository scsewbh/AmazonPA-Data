from bs4 import BeautifulSoup as bs
import mysql.connector
from selenium import webdriver


#-----------------------Settings--------------------------

chromedriver = 'C:\\Users\\scsew\\Desktop\\chromedriver.exe'

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1200x600')  # optional

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mydatabase"
)
'''
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE mydatabase")
#mycursor.execute("CREATE TABLE products (ProductName VARCHAR(200) PRIMARY KEY, Link TEXT)")

#mycursor.execute("SHOW TABLES")
#mycursor.execute("DROP TABLE products")

mycursor.execute("SELECT * FROM products")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
'''

#------------------------Initial Variables--------------------------------

amzn_base_url = 'https://www.amazon.com/'
amzn_Elec_url = 'https://www.amazon.com/most-wished-for/zgbs/electronics/'
amzn_VideoGame_url = 'https://www.amazon.com/most-wished-for/zgbs/videogames/'
amzn_CellAccessories_url = 'https://www.amazon.com/most-wished-for/zgbs/wireless/'
amzn_PC_url = 'https://www.amazon.com/most-wished-for/zgbs/pc/'
amzn_HPC_url = 'https://www.amazon.com/most-wished-for/zgbs/hpc/'
amzn_Skincare_url = 'https://www.amazon.com/most-wished-for/zgbs/beauty/11060451/'
amzn_HI_url = 'https://www.amazon.com/most-wished-for/zgbs/hi/'
amzn_Office_url = 'https://www.amazon.com/most-wished-for/zgbs/office-products'

amzn_wishedFor = [amzn_Elec_url, amzn_VideoGame_url, amzn_CellAccessories_url, amzn_PC_url, amzn_HPC_url, amzn_Skincare_url, amzn_HI_url, amzn_Office_url]

#-----------------------AMZN Class ----------------------------

class AMZN:
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=chromedriver, options=options)
        self.data = []

    def passToDatabase(self):
        mycursor = mydb.cursor()
        sql = "INSERT IGNORE INTO products (ProductName, Link) VALUES (%s, %s)" #Insert Ignore allows me to insert products and skip over the duplicates and the error it gives.
        mycursor.executemany(sql, self.data)
        mydb.commit()
        print(mycursor.rowcount, "was inserted to table.")

    def results(self, listUrl):
        self.data = []
        self.browser.get(listUrl)
        listData = self.browser.page_source
        soup = bs(listData, 'html.parser')
        self.browser.quit()
        print(soup)
        a = soup.find_all('a', class_='a-link-normal a-text-normal')

        print(a)
        for parLink in a:
            pHref = parLink['href'].split('?_encoding=')[0]
            if '/ref=' in pHref:
                pHref = pHref.split('/ref=')[0]
            self.data.append((pHref, amzn_base_url + pHref))
        self.passToDatabase()

'''
<span class="p13n-sc-price">$29.99</span>
bestSellers = AMZN()
for x in amzn_bestSellers:
    data = bestSellers.results(x)
    sql = "INSERT INTO products (PartialLink, Link) VALUES (%s, %s)"
    mycursor.executemany(sql, data)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
g = 'https://www.amazon.com//Canon-PG-243-Cartridge-Compatible-iP2820/dp/B01LXJNPZV?_encoding=UTF8&psc=1'
bestSellers = AMZN()
'''
y = AMZN()
y.results('https://www.amazon.com/most-wished-for/zgbs/office-products')

