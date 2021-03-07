import requests
import random


def run():
	res = requests.get("https://api.swaggystocks.com/wsb/sentiment/top?limit=500")
	tickers = res.json()[:100]
	stuff = random.choices(tickers, k=50)
	proper_array = [d['ticker'] for d in stuff]
	print(proper_array)
	return proper_array

run()