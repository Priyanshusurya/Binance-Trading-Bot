import argparse
from setting import API_KEY, API_SECRET
from bot import BasicBot
from logger import setup_logger
from binance.enums import *

def main():
    setup_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", choices=["BUY", "SELL"], required=True)
    parser.add_argument("--type", choices=["MARKET", "LIMIT"], required=True)
    parser.add_argument("--qty", type=float, required=True)
    parser.add_argument("--price", type=float, help="Required for LIMIT orders")

    args = parser.parse_args()

    # ✅ Use the class from bot.py (not redefined here)
    bot = BasicBot(API_KEY, API_SECRET)

    # ✅ This will work only if it's defined in bot.py
    bot.check_balance()

    side = SIDE_BUY if args.side == "BUY" else SIDE_SELL
    order_type = ORDER_TYPE_MARKET if args.type == "MARKET" else ORDER_TYPE_LIMIT

    result = bot.place_order(args.symbol.upper(), side, order_type, args.qty, args.price)

    if result:
        print("✅ Order executed:", result)
    else:
        print("❌ Order failed. Check logs.")

if __name__ == "__main__":
    main()
