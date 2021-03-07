import random
from apiscript import OrderAPI

test = OrderAPI("apikey", "demoaccount20212", "apipass")

def get_ticket_array(tickers, amount, order):
    ticker_prices = []
    for ticker in tickers:
        temp_price = order.get_price(ticker)
        if temp_price < amount:
            temp = {
                "ticker": ticker,
                "price": temp_price
            }
            ticker_prices.append(temp)
    return ticker_prices
    
def get_stock(ticker_prices):
    stock = random.choice(ticker_prices)
    return stock

def yolo(order, stock):
    stock_order = order.create_order(order.get_epic(stock["ticker"]))
    reference = order.execute_order(stock_order)

demo_tickers = ["TSLA", "AMD", "AAPL", "PLTR", "SHOP", "BB", "UBER"]
amount = 10000000

test.get_tokens()
ticker_prices = get_ticket_array(demo_tickers, amount, test)
print(get_stock(ticker_prices))