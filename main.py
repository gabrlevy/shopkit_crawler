import requests
from bs4 import BeautifulSoup
import pandas
import re
import csv

# html_text = requests.get().text
# <a href="https://zaytouna.shopk.it/product/labneh-gulcan-regular" target="_blank" class="text-light-gray datagrid-show-onhover" title="Ver produto na loja" data-toggle="tooltip">
# Parse the html file
products_file = open("htmls/products_1.htm", "r")
if products_file.mode == "r":
    contents = products_file.read()


# Format the parsed html file
# strhtm = soup.prettify()
soup = BeautifulSoup(contents, 'html.parser')

all_products = {"handle":[], "keywords":[]}

for link in soup.find_all(href=re.compile("it/product/")):
    product_url = link.get('href')
    print(product_url)

    html_text = requests.get(product_url).text
    product_soup = BeautifulSoup(html_text, 'html.parser')
    product_keywords = product_soup.find(name="meta", attrs={"name": "keywords"})
    if product_keywords is not None:
        product_keywords = product_keywords.attrs["content"]
    else:
        product_keywords = " "
    product_handle = product_url[34:]
    all_products["handle"].append(product_handle)
    all_products["keywords"].append(product_keywords)

df = pandas.DataFrame.from_dict(all_products)
df.to_csv("all_prodcuts.csv")



        # for key in ficha_produto:
        #     writer.writerow({'handle': key, 'keywords': ficha_produto[key]})

    # with open(r'test.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(fieldnames)
    #     for key in ficha_produto.keys():
    #         f.write("%s,%s\n" % (key, ficha_produto[key]))






