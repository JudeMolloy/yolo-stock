import random
from apiscript import OrderAPI

test = OrderAPI("f6e357f2b8a0083bd5b89bd188e64ae2e159c1b4", "demoaccount20212", "2JRjuUL7ypv3")

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
    
def yolo(ticker_prices, order):
    tickers = [d["ticker"] for d in ticker_prices]
    stock = random.choice(tickers)
    print(stock)
    stock_order = order.create_order(order.get_epic(stock))
    reference = order.execute_order(stock_order)

demo_tickers = ["TSLA", "AMD", "AAPL", "PLTR", "SHOP", "BB", "UBER"]
amount = 10000000

test.get_tokens()
yolo(get_ticket_array(demo_tickers, amount, test), test)