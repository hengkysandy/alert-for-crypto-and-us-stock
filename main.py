import sys
import os
import pymongo
import telebot
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from binance.client import Client
client = Client()

API_KEY = '<TELEGRAM_API_KEY>'
bot = telebot.TeleBot(API_KEY)
message_id = '<YOUR_TELEGRAM_CHANNEL_ID>'

cluster = MongoClient('mongodb+srv://<USERNAME>:<PASSWORD>@<MONGODB_HOST>/<MONGODB_DB>?retryWrites=true&w=majority')
db = cluster['<MONGODB_DB>']
collection = db['<MONGODB_COLLECTION>']

if len(sys.argv) == 2:
    asset_type = sys.argv[1]
    is_crypto_type = False
    url = ""
    html_tag = ""
    attribute = ""
    attribute_value = ""
    
    if asset_type == "stock-us":
        url = "https://finance.yahoo.com/quote/"
        html_tag = "fin-streamer"
        attribute = "class"
        attribute_value = "Fw(b) Fz(36px) Mb(-4px) D(ib)"
    else:
        is_crypto_type = True
    
    col = collection.find({"type": asset_type})
    for data in col:
        try:
            is_triggered = False
            if is_crypto_type == True:
                current_asset_price = client.get_symbol_ticker(symbol=data['name'])['price']
            else:
                response = requests.get(url+data['name'])
                soup = BeautifulSoup(response.text, "html.parser")
                current_asset_price = soup.find(html_tag, {attribute: attribute_value}).text
                current_asset_price = current_asset_price.replace(',','')
            
            if data['condition'] == "above" and float(current_asset_price) > float(data['price']):
                is_triggered = True
            elif data['condition'] == "below" and float(current_asset_price) < float(data['price']):
                is_triggered = True

            if is_triggered == True:
                msg = 'TRIGGERED: ' + data['name'] + ' ' + data['condition'] + ' ' + data['price'] + ' (' + data['type'] + ')'
                bot.send_message(message_id, msg)
                collection.delete_one({"_id": data['_id']})
            
        except:
            print("Caught Error on get current asset price")