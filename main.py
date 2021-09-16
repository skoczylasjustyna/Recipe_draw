from bs4 import BeautifulSoup as bs
import requests
import re
import csv
import pandas as pd

def getHTMLdoc(url):
    response = requests.get(url)
    return response.text

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
del main_recipies[0:324]
del main_recipies[131:164]
main_recipies = list(dict.fromkeys(main_recipies))

del main_recipies[46:51]
main_recipies.remove("None")
main_recipies.remove("/user/login")
main_recipies.remove('#navbar')
main_recipies.remove("/regulamin-i-polityka-prywatnosci")

rec_url = []
rec_names = []

#splitting record so that only recipe's name remains, saving pages url
def create_rec_name():
    for i in range(len(main_recipies)):
        x = main_recipies[i]
        rec_url.append(x)
        splitting = x.split('/')
        rec_name = splitting[2]
        rec_name= rec_name.replace("-", " ")
        rec_name = rec_name.replace("_", " ")
        rec_names.append(rec_name)

create_rec_name()

#creating valid url for recipes
full_rec_url = []
def create_url():
    for i in range(len(rec_url)):
        recipe_url = blog_url +  rec_url[i]
        full_rec_url.append(recipe_url)

create_url()
#getting ingredients from single recipe - section in progress - it should take ingredients for each of recipies saved into list, so that they can be added to the csv
ing_list = []
def get_ing():
    for i in range(len(full_rec_url)):
        ing = full_rec_url[i]
        recipe_html = requests.get(ing).content

        data = bs(recipe_html, 'html.parser')
        div_data = data.find_all("div", {"class": "field field-name-field-skladniki field-type-text-long field-label-hidden"})

        for x in div_data:
            li_tag = x.find_all("li")
            for x in li_tag:
                print(x.text)

#saving recipes name and url into csv file
dictionary = {'name' : rec_names, 'url' : full_rec_url}
dataframe = pd.DataFrame(dictionary)
dataframe.to_csv('recipes.csv')

#getting random recipe - in progress