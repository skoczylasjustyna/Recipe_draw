from bs4 import BeautifulSoup as bs
import requests
import re
import csv
import pandas as pd

#saving recipies
def getHTMLdoc(url):
    response = requests.get(url)
    return response.text

#getting main page
blog_url = "https://www.kwestiasmaku.com"
blog_html = getHTMLdoc(blog_url)
soup = bs(blog_html, 'html.parser')

# extracting recipies from main section
main_recipies = []
def getMainLinks():
    for link in soup.find_all('a'):
        main_recipies.append(str(link.get('href')))

getMainLinks()

#getting rid of items which are not recipies
main_recipies = list(dict.fromkeys(main_recipies))
main_recipies.remove("None")
main_recipies.remove("/user/login")
main_recipies.remove('#navbar')

del main_recipies[0:290]
del main_recipies[47:72]
del main_recipies[-1]

#lists to store recipes name and url
full_rec_url = []
rec_names = []
rec_urls = []

#splitting record so that only recipe's name remains
def create_rec_name():
    for i in range(len(main_recipies)):
        x = main_recipies[i]
        rec_urls.append(x)
        splitting = x.split('/')
        if len(splitting) >2:
            name = splitting[2]
            name= name.replace("-", " ")
            name = name.replace("_", " ")
            rec_names.append(name)
        else:
            pass

create_rec_name()

#creating valid url for recipes

def create_url():
    for i in range(len(rec_urls)):
        url = blog_url + rec_urls[i]
        full_rec_url.append(url)

create_url()
full_rec_url.remove('https://www.kwestiasmaku.com/home-przepisy?page=1')

#saving recipes name and url into csv file

dictionary = {'name' : rec_names, 'url' : full_rec_url}
dataframe = pd.DataFrame(dictionary)
dataframe.to_csv('recipes.csv')

