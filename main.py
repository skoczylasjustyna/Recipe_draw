from bs4 import BeautifulSoup as bs
import requests
import re

def getHTMLdoc(url):
    response = requests.get(url)
    return response.text

blog_url = "https://www.kwestiasmaku.com/"
blog_html = getHTMLdoc(blog_url)

soup = bs(blog_html, 'html.parser')

# extracting recipies from main section
main_recipies = []
def getMainLinks():
    for link in soup.find_all('a'):
        main_recipies.append(str(link.get('href')))

getMainLinks()
del main_recipies[0:324]
del main_recipies[131:164]
main_recipies = list(dict.fromkeys(main_recipies))

del main_recipies[46:51]
main_recipies.remove("None")
main_recipies.remove("/user/login")
x = main_recipies[0]

splitting = x.split('/')

rec_name = splitting[2]
rec_name = rec_name.replace("_", " ")
clear_recipies = []

def create_rec_name(rec_list):
    for i in range(len(rec_list)):
        x = rec_list[i]
        splitting = x.split('/')
        rec_name = splitting[2]
        rec_name= rec_name.replace("-", " ")
        rec_name = rec_name.replace("_", " ")
        print(rec_name)

create_rec_name(main_recipies)

###########getting ingredients from single recipe########################

recipe_url = "https://www.kwestiasmaku.com/przepis/pomidorowe-curry-z-kurczakiem"
recipe_html = requests.get(recipe_url).content

data = bs(recipe_html, 'html.parser')
div_data = data.find_all("div", {"class": "field field-name-field-skladniki field-type-text-long field-label-hidden"})

for x in div_data:
    li_tag = x.find_all("li")
    for x in li_tag:
        print(x.text)