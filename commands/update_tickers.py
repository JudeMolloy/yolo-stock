from app import db
from flask_script import Command
from bs4 import BeautifulSoup
import requests


class UpdateTickersCommand(Command):
	def run(self):
		res = requests.get(TICKER_URL)

		html_raw = res.content.decode("utf-8")
		html = BeautifulSoup(html_raw, 'html.parser')

		containers = html.body.find_all("div", class_="volume-ticker-entry")
		if len(containers) == 0:
			print("Can't find root element")
			return

		tickers = []

		for container in containers:
			names = html.body.find_all("div", class_="volume-ticker-name")
			
			if len(names) == 0: continue

			tickers.append(names[0])

		print(tickers)