import time
from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
from logger import setup_logger  # ✅ Assuming this sets up and returns a logger


class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)

        # Time sync fix
        server_time = self.client.futures_time()
        local_time = int(time.time() * 1000)
        self.client.TIME_OFFSET = server_time["serverTime"] - local_time

        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        self.logger = setup_logger()

    def check_balance(self):
        try:
            balance = self.client.futures_account_balance()
            for asset in balance:
                if asset["asset"] == "USDT":
                    print("USDT Balance:", asset["balance"])
        except Exception as e:
            self.logger.error(f"Balance check failed: {e}")
            print(f"DEBUG ERROR: {e}")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == ORDER_TYPE_MARKET:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            elif order_type == ORDER_TYPE_LIMIT and price:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                raise ValueError("Invalid order type or missing price for LIMIT")

            self.logger.info(f"Order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Order failed: {e}")
            print(f"DEBUG ERROR: {e}")
            return None
