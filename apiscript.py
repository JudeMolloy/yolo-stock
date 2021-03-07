import requests
import json
from config import Config


headers = {
    "X-IG-API-KEY": "apikey",
    "X-SECURITY-TOKEN": "bae8afa438e9b4fa579008823963e15731f7eb7ff00114a30fa9569e96cd33CD01111",
    "CST": "6d7141b70f236e3b8025ba551cad09d90c7cda1c146c1acc9a01293e6e5ffcCU01111",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json; charset=UTF-8",
}

body = {
    "currencyCode": "USD",
    "epic": "IX.D.FTSE.DAILY.IP",
    "expiry": "DFB",
    "direction": "BUY",
    "size":"3",
    "forceOpen": "false",
    "guaranteedStop": "false",
    "orderType": "MARKET"
}

response = requests.get("https://demo-api.ig.com/gateway/deal/markets", params={"searchTerm": "AMD"}, headers=headers)

response = requests.post("https://demo-api.ig.com/gateway/deal/positions/otc", headers=headers, data=json.dumps(body))

#print(response.status_code)

class OrderAPI:
    def __init__(self, apikey, username, password):
        self.apikey = apikey
        self.CST = ""
        self.X_SECURITY_TOKEN = ""
        self.headers = {
            "X-IG-API-KEY": apikey,
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8"
        }
        self.body = {
            "identifier": username,
            "password": password
        }

    def get_tokens(self):
        try:
            response = requests.post("https://demo-api.ig.com/gateway/deal/session", data=json.dumps(self.body), headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        self.CST = response.headers["CST"]
        self.X_SECURITY_TOKEN = response.headers["X-SECURITY-TOKEN"]
        self.headers["CST"] = self.CST
        self.headers["X-SECURITY-TOKEN"] = self.X_SECURITY_TOKEN
        print("Updated security tokens", self.CST, self.X_SECURITY_TOKEN)

    def create_order(self, epic):
        order = {
            "currencyCode": "USD", #Eg USD, GBP
            "epic": epic, #This is meant to tell you what stock is but idk tbh
            "expiry": "DFB", #keep this at DFB probably
            "direction": "BUY", #Keep at buy
            "size": "1", #I think this is amount
            "forceOpen": True, #Enables a second position to be opened
            "guaranteedStop": False, #Stop loss is for losers
            "orderType": "MARKET" #Executed at any price
        }
        return order

    def get_price(self, ticker):
        try:
            response = requests.get("https://demo-api.ig.com/gateway/deal/markets", params={'searchTerm': ticker}, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        response = response.json()
        return response["markets"][0]["offer"]

    def get_epic(self, ticker):
        try:
            response = requests.get("https://demo-api.ig.com/gateway/deal/markets", params={'searchTerm': ticker}, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        response = response.json()
        return response["markets"][0]["epic"]

    def execute_order(self, order):
        executeheaders = self.headers.copy()
        executeheaders["Version"] = "2"
        try:
            response = requests.post("https://demo-api.ig.com/gateway/deal/positions/otc", data=json.dumps(order), headers=executeheaders)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        print("success")

#print(Config.IG_API_KEY)

#test = OrderAPI("apikey", "demoaccount20212", "apipass")
#test.get_tokens()
#testorder = test.create_order("USD", test.get_epic("AMD"))
#test.execute_order(testorder)