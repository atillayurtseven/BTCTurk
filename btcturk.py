# ---------------------------------------------------------------------------------
# BTCTurk API Python Wrapper
# Author: Atilla Yurtseven
# License: MIT License
#
# Bu dosya, BTCTurk API'sini kullanarak çeşitli kripto para işlemleri ve sorgulamalarını
# yapmak için yazılmış bir Python wrapper'ıdır. Tüm hakları saklıdır.
# ---------------------------------------------------------------------------------
# https://docs.btcturk.com/

import requests, base64, time, hashlib, hmac
from endpoints import ENDPOINTS

base = "https://api.btcturk.com"
base_ws = "wss://ws-feed-pro.btcturk.com"

class BTCTurk:
    def __init__(self, apiKey: str, apiSecret: str):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.apiSecret = base64.b64decode(apiSecret)
        self.symbols = {}
        self.exchange_info = self.get_exchange_info()["data"]
        for e in self.exchange_info["symbols"]:
            digit = e["denominatorScale"]
            e["price"] = self.round_pair(pair="", val=e["minimumLimitOrderPrice"] * 10, digit=digit)
            self.symbols[e["name"]] = e

    def qty_check(self, pair: str, qty: float) -> bool:
        min_val = float(self.symbols[pair]["filters"][0]["minExchangeValue"])
        last_price = float(self.symbols[pair]["price"])
        val = qty * last_price
        return val >= min_val

    def round_pair(self, pair: str, val: float, digit: int = 0) -> float:
        if pair == "":
            numeratorScale = digit
        else:
            numeratorScale = self.symbols[pair]["numeratorScale"]
        dgt = 10 ** numeratorScale
        return int(val * dgt) / dgt

    def numerator_scale(self, pair: str, val: float) -> float:
        numeratorScale = self.symbols[pair]["numeratorScale"]
        dgt = 10 ** numeratorScale
        return int(val * dgt) / dgt

    def denominator_scale(self, pair: str, val: float) -> float:
        denominatorScale = self.symbols[pair]["denominatorScale"]
        dgt = 10 ** denominatorScale
        return int(val * dgt) / dgt

    def send(self, cmd: str, act: str = "", payload: dict = None, order_id: int = 0) -> dict:
        stamp = str(int(time.time()) * 1000)
        data = "{}{}".format(self.apiKey, stamp).encode('utf-8')
        signature = hmac.new(self.apiSecret, data, hashlib.sha256).digest()
        signature = base64.b64encode(signature)

        headers = {
            "X-PCK": self.apiKey,
            "X-Stamp": stamp,
            "X-Signature": signature,
            "Content-Type": "application/json"
        }

        e = ENDPOINTS[cmd]
        ep = e["ep"]
        t = e["type"]
        if "base" in e:
            host = e["base"]
        else:
            host = base
        url = f"{host}{ep}"
        if act != "":
            if cmd == "order" and t == "GET":
                url += "/" + act
            else:
                url += "?" + act
        if t == "GET":
            r = requests.get(url, headers=headers)
        elif t == "POST":
            r = requests.post(url, headers=headers, json=payload)
        elif t == "DELETE":
            r = requests.delete(url, headers=headers)
        else:
            r = {}
        return r.json()

    def get_balances(self, nonzero: bool = True) -> list:
        r = self.send("balances")
        b = r["data"]
        a = []
        if nonzero:
            for s in b:
                if float(s["balance"]) > 0.0:
                    a.append(s)
            return a
        else:
            return b

    def get_fiat_balances(self) -> list:
        a = []
        b = self.get_balances()
        for s in b:
            if s["asset"] == "TRY" or s["asset"] == "USDT":
                a.append(s)
        return a

    def get_crypto_balances(self) -> list:
        a = []
        b = self.get_balances()
        for s in b:
            if s["asset"] != "TRY" and s["asset"] != "USDT":
                if float(s["balance"]) > 0.0:
                    a.append(s)
        return a

    def get_all_orders(self, pair: str) -> dict:
        act = ""
        if pair != "":
            act = f"pairSymbol={pair}"
        return self.send("all_orders", act)

    def get_filtered_orders(self, pair: str, filter: str) -> list:
        o = self.get_all_orders(pair)
        orders = []
        for s in o:
            if s["status"].lower() == filter:
                orders.append(s)
        return orders

    def get_canceled_orders(self, pair: str) -> list:
        return self.get_filtered_orders(pair, "canceled")

    def get_filled_orders(self, pair: str) -> list:
        return self.get_filtered_orders(pair, "closed")

    def get_untouched_orders(self, pair: str) -> list:
        return self.get_filtered_orders(pair, "untouched")

    def get_single_order(self, order_id: int):
        return self.send("order", act=str(order_id))

    def cancel_order(self, order_id: int) -> dict:
        act = f"id={order_id}"
        return self.send("cancel_order", act)

    def get_ticker(self, pair: str = "") -> dict:
        act = ""
        if pair != "":
            act = f"pairSymbol={pair}"
        return self.send("ticker", act)

    def get_ticker_currency(self, pair: str = "") -> dict:
        act = ""
        if pair != "":
            act = f"symbol={pair}"
        return self.send("ticker_currency", act)

    def get_orderbook(self, pair: str, limit: int = 0) -> dict:
        act = ""
        if pair != "":
            act = f"pairSymbol={pair}"
        if limit > 0:
            act += f"&limit={limit}"
        return self.send("orderbook", act)

    def get_fiat_transactions(self) -> dict:
        act = "type=deposit&type=withdrawal&symbol=try"
        return self.send(cmd="get_fiats", act=act)

    def get_fiat_deposits(self) -> dict:
        act = "type=deposit&symbol=try"
        return self.send(cmd="get_fiats", act=act)

    def get_fiat_withdrawals(self) -> dict:
        act = "type=withdrawal&symbol=try"
        return self.send(cmd="get_fiats", act=act)

    def get_crypto_transactions(self, symbol: list = None) -> dict:
        act = "type=deposit&type=withdrawal"
        if not symbol is None:
            for s in symbol:
                act += f"&symbol={s}"
        return self.send(cmd="get_cryptos", act=act)

    def get_crypto_deposits(self, symbol: list = None) -> dict:
        act = "type=deposit"
        if not symbol is None:
            for s in symbol:
                act += f"&symbol={s}"
        return self.send(cmd="get_cryptos", act=act)

    def get_crypto_withdrawals(self, symbol: list = None) -> dict:
        act = "type=withdrawal"
        if not symbol is None:
            for s in symbol:
                act += f"&symbol={s}"
        return self.send(cmd="get_cryptos", act=act)

    def get_user_trades(self, pair: str = "", start_date: int = 0, end_date: int = 0, symbol: list = None, typ: list = None) -> dict:
        act = ""
        if pair != "":
            act = f"pairSymbol={pair}&"
        if not typ is None:
            for t in typ:
                act += f"type={t}&"
        if not symbol is None:
            for s in symbol:
                act += f"symbol={s}&"
        if start_date > 0:
            act += f"startDate={start_date}&"
        if end_date > 0:
            act += f"endDate={end_date}&"
        if len(act) > 0 and act[-1] == "&":
            act = act[:-1]
        return self.send("get_trades", act)

    def get_public_trades(self, pair: str, last: int = 0) -> dict:
        act = ""
        if pair != "":
            act = f"pairSymbol={pair}"
        if last > 0:
            act += f"&last={last}"
        return self.send("trades", act)

    def get_open_orders(self, pair: str = "") -> dict:
        act = ""
        if pair != "":
            act = f"pairSymbol={pair}"
        return self.send("open_orders", act)

    def get_ohlcs(self, pair: str, from_time: int = 0, to_time: int = 0) -> dict:
        # daily
        act = ""
        if pair != "":
            act = f"pair={pair}"
        if from_time > 0:
            act += f"&from={from_time}"
        if to_time > 0:
            act += f"&to={to_time}"
        return self.send("ohlcs", act)

    def get_klines(self, pair: str, resolution: int = 60, from_time: int = 0, to_time: int = 0) -> dict:
        # daily
        act = ""
        if pair != "":
            act = f"symbol={pair}"
        if resolution > 0:
            act += f"&resolution={resolution}"
        if from_time > 0:
            act += f"&from={from_time}"
        if to_time > 0:
            act += f"&to={to_time}"
        return self.send("klines", act)

    def get_exchange_info(self) -> dict:
        return self.send("exchange_info")

    def submit_order(self, pair: str, price: float, qty: float, orderType: str, orderMethod: str, stopPrice: float = 0.0) -> dict:
        if orderMethod == "market" and orderType == "buy":
            val = self.denominator_scale(pair, qty)
        else:
            val = self.numerator_scale(pair, qty)
        payload = {
            "quantity": val,
            "newOrderClientId": "BtcTurk API Connection by Atilla Yurtseven",
            "orderMethod": orderMethod,
            "orderType": orderType,
            "pairSymbol": pair
        }
        if price > 0.0:
            payload["price"] = price
        if stopPrice > 0.0:
            payload["stopPrice"] = stopPrice
        r = self.send("new_order", payload=payload)
        return r

    def limit_buy(self, pair: str, price: float, qty: float) -> dict:
        return self.submit_order(pair, price, qty, orderMethod="limit", orderType="buy")

    def limit_sell(self, pair: str, price: float, qty: float) -> dict:
        return self.submit_order(pair, price, qty, orderMethod="limit", orderType="sell")

    def market_buy(self, pair: str, amount: float) -> dict:
        return self.submit_order(pair, price=0.0, qty=amount, orderMethod="market", orderType="buy")

    def market_sell(self, pair: str, qty: float) -> dict:
        return self.submit_order(pair, price=0.0, qty=qty, orderMethod="market", orderType="sell")
