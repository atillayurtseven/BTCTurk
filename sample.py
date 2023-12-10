from btcturk import BTCTurk
import json

public_key = "YOUR_PUBLIC_KEY"
private_key = "YOUR_PRIVATE_KEY"
bt = BTCTurk(apiKey=public_key, apiSecret=private_key)
#d = bt.get_open_orders()
d = bt.get_ticker_currency("USDT")
print(json.dumps(d, indent=2))
