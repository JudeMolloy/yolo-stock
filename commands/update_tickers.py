from app import db
from flask_script import Command
import requests
import random


class UpdateTickersCommand(Command):
	def run(self):
		res = requests.get("https://api.swaggystocks.com/wsb/sentiment/top?limit=500")
		tickers = res.json()[:100]

		print(random.choices(tickers, k=3))