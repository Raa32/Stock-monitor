import yfinance as yf
import datetime
import os

STOCKS = {
    "AAPL": {"name": "Apple",  "threshold": 0.1},
    "MSFT": {"name": "Microsoft", "threshold": 0.1},
    "IBKR": {"name": "Interactive Brokers", "threshold": 0.1},
} 

LOG_FILE = "alert.log"
PRICE_FILE = "prices.log"

def fetch_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")
    if data.empty:
        return None
    return round(data["Close"].iloc[-1], 2)

def log(message, filepath):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    with open(filepath, "a") as f:
        f.write(line)
    print(line.strip())

def check_change(ticker, current, previous):
    if previous is None:
        return
    change_pct = abs((current - previous) / previous) * 100
    if change_pct >= STOCKS[ticker]["threshold"]:
        msg = (f"{STOCKS[ticker]['name']} ({ticker}) moved "
               f"{change_pct:.2f}% — prev: ${previous} now: ${current}")
        send_alert(msg) 

def load_previous_prices():
    prices = {}
    if not os.path.exists(PRICE_FILE):
        return prices
    with open(PRICE_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 2:
                prices[parts[0]] = float(parts[1])
    return prices

def save_prices(prices):
    with open(PRICE_FILE, "w") as f:
        for ticker, price in prices.items():
            f.write(f"{ticker},{price}\n")

def send_alert(message):
    print("\n" + "="*50)
    print("THRESHOLD BREACH DETECTED")
    print(message)
    print("="*50 + "\n")
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ALERT: {message}\n")
def main():
    previous = load_previous_prices()
    current = {}
    for ticker in STOCKS:
        price = fetch_price(ticker)
        if price:
            current[ticker] = price
            log(f"{ticker}: ${price}", PRICE_FILE)
            check_change(ticker, price, previous.get(ticker))
        else:
            log(f"ERROR: Could not fetch price for {ticker}", LOG_FILE)
    save_prices(current)

if __name__ == "__main__":
    main()
