from datetime import datetime, timedelta
import time

from Enums.enums import AssetType, Assets
from strategies.TrendFollowingBuyStrategy import TrendFollowingBuyStrategy

# inputs
ticker = Assets.BTCUSD.name
historical_data_ticker = Assets.BTCUSD.value
assetType = AssetType.Crypto
interval = 5
short_period = 12
long_period = 26
trend_period = 200
atr_period = 14
stop_loss_multipler = 10
take_profit_multiplier = 40
trend_ema_offset = 0
investment_amount = 500

def run_strategy():
    strategy = TrendFollowingBuyStrategy(ticker = ticker, historical_data_ticker=historical_data_ticker, assetType = assetType, \
                interval=interval, short_period=short_period, long_period =long_period, trend_period = trend_period, \
                    atr_period=atr_period, stop_loss_multipler=stop_loss_multipler, take_profit_multiplier=take_profit_multiplier, \
                        trend_ema_offset=trend_ema_offset, investment_amount=investment_amount)
    try:
        print("Application started. Press Ctrl+C to stop.")
        while True:
            start = datetime.now() - timedelta(minutes=(2*trend_period)*interval)
            end = datetime.now()
            strategy.apply(start, end)
            time.sleep(interval*60)
    except KeyboardInterrupt:
        print("\nApplication interrupted and stopped by user.")
    
if __name__ == "__main__":
    run_strategy()