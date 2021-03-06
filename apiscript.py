import requests
import json

headers = {
    "X-IG-API-KEY": "f6e357f2b8a0083bd5b89bd188e64ae2e159c1b4",
    "X-SECURITY-TOKEN": "bae8afa438e9b4fa579008823963e15731f7eb7ff00114a30fa9569e96cd33CD01111",
    "CST": "6d7141b70f236e3b8025ba551cad09d90c7cda1c146c1acc9a01293e6e5ffcCU01111",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json; charset=UTF-8",
    "Version": "2"
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

response = requests.post("https://demo-api.ig.com/gateway/deal/positions/otc", headers=headers, data=json.dumps(body))

#print(response.status_code)

class API:
    def __init__(self, apikey, username, password):
        self.apikey = apikey
        self.CST = ""
        self.X_SECURITY_TOKEN = ""
        self.headers = {
            "X-IG-API-KEY": apikey,
            "VERSION": "2",
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
        print("Updated security tokens")

    def create_order(self, currency, epic, expiry, size):
        order = {
            "currencyCode": currency,
            "epic": epic,
            "expiry": expiry,
            "direction": "BUY",
            "size": size,
            "forceOpen": False,
            "guaranteedStop": False,
            "orderType": "MARKET"
        }
        return order

    def execute_order(self, order):
        try:
            response = requests.post("https://demo-api.ig.com/gateway/deal/positions/otc", data=json.dumps(order), headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        print("success")

test = API("f6e357f2b8a0083bd5b89bd188e64ae2e159c1b4", "demoaccount20212", "2JRjuUL7ypv3")
test.get_tokens()
testorder = test.create_order("USD", "IX.D.FTSE.DAILY.IP", "DFB", "3")
test.execute_order(testorder)