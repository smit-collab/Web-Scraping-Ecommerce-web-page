import bs4
import requests
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup 
import csv

 

#to get the website url
def get_page(url):
    #response var will contain the response from the website server. 
    response = requests.get(url)#instance of response class
    
    #sometimes server can give error 404 or etc. below code is used to check if requested resource exists or not.
    # print(response.ok) 
    # print(response.status_code)#200 means server responded properly.

    #if server does not respond.print error
    if not response.ok:
        print("Server responded : " , response.status_code)
    else: 
        #need to convert html page to python object tree using bs4 for efficient search.
        soup  = BeautifulSoup(response.text , 'lxml')#first arg is html code.2nd arg is parser .most efficient is lxml
        return soup



#to scrap the data like title,price,items sold on url page.
def get_detail_data(soup):
    #getting title with h1 tag
    #find_all is used to find more than one element.
    #find is used to find first found element
    #text.strip() to only get the text. 
    # alternative is soup.select('h1.listing-name')[0].text.strip() for many h1 tags.
    
    try:
        title = soup.find('h1' , id = 'itemTitle').text.strip()
    except:
        title = ''

    try:
        p = soup.find('span' , id = 'prcIsum').text.strip()#strip will remove spaces and split to put it in list with space seperator
        currency, price = p.split(' ') 
    except:
        currency =''
        price = ''  

    try:
        available = soup.find('span' , class_= "").text
    except:
        available=''    

    # creating dictionary
    data = {
        'title':title,
        'price':price,
        'currency':currency,
        'available':available
    }

    return data


    # print("Title is : " , title)
    # print("")
    # print("Price is " , price)
    # print("")
    # print("Currency is " , currency , "$")
    # print("")
    # print("Avaialable items are : " , available)



# getting all the link associated with class s-item__link from ebay page
def get_index_data(soup):
    try:
        links = soup.find_all('a' , class_= 's-item__link')#will give output as list of all a tags objs
    except:
        links = []    
    urls = [item.get('href') for item in links] #get all href from a tag objects and store it in urls list.
    # now urls var contian all the products from the url and its link.

    # now to crawl urls list
    # print(urls)
    return urls


def write_csv(data,url):
    with open('output.csv' , 'a') as csv_file:#a will append new data to the file
        writer = csv.writer(csv_file)

        row = [data['title'],data['price'],data['currency'],data['available'],url]#storing all the keys from data dict in row

        writer.writerow(row)#to write to the file








def main():
    # main url of the page.
    
    #below url is for just getting specific info on a watch 
    # url = 'https://www.ebay.com/itm/24-Carats-White-Diamond-Rolex-41-MM-Date-Just-II-2-Watch-BEST-PRICE-EBAY-ASAAR/400907784114?hash=item5d57f74fb2:g:TFkAAOSwBahVObAb'

    # below url is to get info from many pages using main url
    url  = 'https://www.ebay.com/sch/i.html?_nkw=ebay+watches&_pgn=1'
    
    # get_detail_data(get_page(url))
    # get_index_data(get_page(url))

    # storing all the product links in a var
    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail_data(get_page(link))    
        write_csv(data,link)
        # print(data)


if __name__ == "__main__":
    main()
