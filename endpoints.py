ENDPOINTS = {
    "balances": {
        "ep": "/api/v1/users/balances",
        "type": "GET",
        "permission": "Total Funds (Toplam Varlık)"
    },
    "all_orders": {
        "ep": "/api/v1/allOrders",
        "type": "GET",
        "permission": "Trade (Al-Sat)"
    },
    "order": {
        "ep": "/api/v1/order",
        "type": "GET",
        "permission": "Trade (Al-Sat)"
    },
    "cancel_order": {
        "ep": "/api/v1/order",
        "type": "DELETE",
        "permission": "Trade (Al-Sat)"
    },
    "new_order": {
        "ep": "/api/v1/order",
        "type": "POST",
        "permission": "Trade (Al-Sat)"
    },
    "open_orders": {
        "ep": "/api/v1/openOrders",
        "type": "GET",
        "permission": "Trade (Al-Sat)"
    },
    "get_trades": {
        "ep": "/api/v1/users/transactions/trade",
        "type": "GET",
        "permission": "Account (Hesap)"
    },
    "get_fiats": {
        "ep": "/api/v1/users/transactions/fiat",
        "type": "GET",
        "permission": "Account (Hesap)"
    },
    "get_cryptos": {
        "ep": "/api/v1/users/transactions/crypto",
        "type": "GET",
        "permission": "Account (Hesap)"
    },
    "exchange_info": {
        "ep": "/api/v2/server/exchangeinfo",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    "ticker": {
        "ep": "/api/v2/ticker",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    "ticker_currency": {
        "ep": "/api/v2/ticker/currency",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    "orderbook": {
        "ep": "/api/v2/orderbook",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    "trades": {
        "ep": "/api/v2/trades",
        "type": "GET",
        "version": "v2",
        "permission": ""
    },
    "ohlcs": {
        "ep": "/v1/ohlcs",
        "type": "GET",
        "permission": "",
        "base": "https://graph-api.btcturk.com"
    },
    "klines": {
        "ep": "/v1/klines/history",
        "type": "GET",
        "permission": "",
        "base": "https://graph-api.btcturk.com"
    }
}
