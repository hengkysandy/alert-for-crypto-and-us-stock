
# Alert for Crypto and US Stock

Create your own crypto and US Stock market alert that will publish message on your telegram channel

## How to Use

1. Clone the repository.
2. Install the dependencies: `pip3 install -r requirements.txt`
3. Create your own telegram channel and Telegram API Key
5. Create your own mongodb atlas account and create collection name with format
```
{"_id":"1234","name":"AMZN","type":"stock-us","price":"84","condition":"below"}
{"_id":"1233","name":"BTCUSDT","type":"crypto","price":"30000","condition":"above"}
```
4. Run the project in cronjob that will run every 5 minutes, by using the following command: 
```
*/5 * * * * /usr/bin/python3.6 main.py crypto
*/5 * * * * /usr/bin/python3.6 main.py stock-us
```
