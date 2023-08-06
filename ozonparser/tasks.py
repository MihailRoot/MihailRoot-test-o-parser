
from .celery import app 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
from telegram import Bot
import time
from django.apps import apps


def sendtg(msg,id='@TESTBOT_API'):
    bot = Bot('6464088491:AAEPuZNZiDezsGArG8JIJ8EH7X0ekN2L7_E')
    bot.send_message(id, msg, 'MarkdownV2')

@app.task
def process(products_count):
    
    sendtg(f'Parsing task started Products parsing: {products_count}')
    model = apps.get_model(app_label='ozonparser',model_name='Product')

    options = FirefoxOptions()
    options.headless
    options.add_argument('--headless')
    with webdriver.Firefox(options=options,) as wd:
        data = []
        url = "https://www.ozon.ru/seller/1/products/"
        wd.get(url)
        time.sleep(4)
        wd.execute_script("window.scrollTo(0, 2500);")
        time.sleep(4)
        wd.execute_script("window.scrollTo(0, 4000);")
        soup = BeautifulSoup(wd.page_source, 'html.parser')
        divs = soup.find_all("div",class_="i9j ik")
        count = 0
        timestap = int(time.time() * 1000)
        for information in divs:
            if count >= products_count: #Счетчик для товара
                break
            getspan = information.find('span',class_="tsBody500Medium")
            getprice  = information.find('span',class_= 'c3-a1 tsHeadline500Medium c3-b9')
            get_product_url = information.find('a',class_='tile-hover-target yh3 h4y')
            geturl = information.find('img',class_='c9-a')
            getdiscount = information.find('span',class_='tsBodyControl400Small c3-a2 c3-a7 c3-b1')
            price =  int(getprice.text.replace("₽",'').replace(' ',''))
            model.objects.create(name=getspan.text,price=price ,description =getspan.text  ,image_url =geturl['src'] ,discount =getdiscount.text,timeid=timestap,url=get_product_url['href'])
            count += 1
    sendtg(f'Saved {products_count}')


@app.task
def result(id):
    model = apps.get_model(app_label='ozonparser',model_name='Product')
    fs = model.objects.latest("timeid")
    data = []
    fs1 = model.objects.all().filter(timeid = int(fs))
    for i in fs1:
        item = str(i)
        item = item.replace('-','\\-').replace('!','\\!').replace('(','\\(').replace(')','\\)').replace('.','\\.')
        image = 'http://localhost:8000/short/' + str(i.id)
        data.append('*' + item + "*\n" + image  )
    sendtg('\n \\-\\-\\- \n'.join(data),id)
    # print('\n \\-\\-\\- \n'.join(data[10:20]),id)
    # print('\n \\-\\-\\- \n'.join(data[20:30]),id)
