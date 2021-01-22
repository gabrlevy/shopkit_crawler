import requests
from bs4 import BeautifulSoup
import pandas
import re
import os
import csv
# from googletrans import Translator
# translator = Translator()
#
# #Translating the text to specified target language
# def translate(word):
#     # Target language
#     target_language = 'en' #Add here the target language that you want to translate to
#     # Translates some text into Russian
#     translation = translator.translate(
#         word,
#         dest=target_language)
#
#     return translation.text


from google.cloud import translate
all_products = {"handle":[], "title":[], "keywords":[]}



def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target, source_language="pt")


    return result["translatedText"]


directory = "./htmls/"

for filename in os.listdir(directory):
    if filename.endswith(".htm"):
        products_file = open(os.path.join(directory, filename), "r")
        if products_file.mode == "r":
            contents = products_file.read()

        soup = BeautifulSoup(contents, 'html.parser')


        for link in soup.find_all(href=re.compile("it/product/")):
            product_url = link.get('href')
            print(product_url)

            html_text = requests.get(product_url).text
            product_soup = BeautifulSoup(html_text, 'html.parser')
            product_keywords = product_soup.find(name="meta", attrs={"name": "keywords"})
            product_title = product_soup.find(name="h1")
            if product_title is not None:
                product_title = product_title.contents[0]
                translated_title_en = translate_text(target="en", text=product_title)
                translated_title_fr = translate_text(target="fr", text=product_title)

            else:
                product_title = " "
            if product_keywords is not None:
                if product_title is not None:
                    product_keywords = product_keywords.attrs["content"] + ", " + translated_title_en + ", " + \
                                       translated_title_fr
            else:
                product_keywords = " "
            product_handle = product_url[34:]
            all_products["handle"].append(product_handle)
            all_products["keywords"].append(product_keywords)
            all_products["title"].append(product_title)


    df = pandas.DataFrame.from_dict(all_products)
    df.to_csv("all_products.csv")