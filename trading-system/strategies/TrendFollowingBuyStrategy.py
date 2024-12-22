from typing import Any
from Enums.enums import AssetType, Side
from market_connectors.alpaca import AlpacaAPI
from datetime import datetime, timedelta
import talib as ta

class TrendFollowingBuyStrategy:
    def __init__(self, ticker, historical_data_ticker, assetType, interval, short_period, long_period, trend_period, \
        atr_period, stop_loss_multipler, take_profit_multiplier, trend_ema_offset, investment_amount):
        self.ticker = ticker
        self.historical_data_ticker = historical_data_ticker,
        self.assetType = assetType
        self.interval = interval
        self.short_period = short_period
        self.long_period = long_period
        self.trend_period = trend_period
        self.atr_period = atr_period
        self.stop_loss_multiplier = stop_loss_multipler
        self.take_profit_multiplier = take_profit_multiplier
        self.trend_ema_offset = trend_ema_offset
        self.investment_amount = investment_amount
        self.alpacaAPI = AlpacaAPI(ticker=ticker, historical_data_ticker=historical_data_ticker, interval=interval)
        self.short_ema = 0
        self.long_ema = 0
        self.atr = 0
        self.trend_ema = 0
        self.close = 0
        self.stop_loss = None
        self.take_profit = None
        self.side = ''
        
    def apply(self, start, end):
        data = self.get_historical_data(start, end)
        data = self.get_indicators(data)
        position_checker = self.alpacaAPI.has_position()
        if position_checker == False:
            if (self.close >= self.trend_ema):
                if (self.short_ema > self.long_ema):
                    self.stop_loss = self.close - (self.stop_loss_multiplier * self.atr)
                    self.take_profit = self.close + (self.take_profit_multiplier * self.atr)
                    self.alpacaAPI.create_order(amount=self.investment_amount, time_in_force='gtc', side=Side.Buy.value)
                    # self.side = 'buy'
                    print(f'Buy order placed with close price: {self.close}, stop loss: {self.stop_loss}, take profit: {self.take_profit} at {end}')
                    print(f'Indicators- shortEMA: {self.short_ema}, longEMA: {self.long_ema}, trendEMA: {self.trend_ema}') 
            # else:
            #     if (self.short_ema < self.long_ema):
            #         self.stop_loss = self.close + (self.stop_loss_multiplier * self.atr)
            #         self.take_profit = self.close - (self.take_profit_multiplier * self.atr)
            #         self.alpacaAPI.create_order(amount=self.investment_amount, time_in_force='gtc', side=Side.Sell.value)
            #         self.side = 'sell'
            #         print(f'Sell order placed with close price: {self.close}, stop loss: {self.stop_loss}, take profit: {self.take_profit} at {end}')
            #         print(f'Indicators- shortEMA: {self.short_ema}, longEMA: {self.long_ema}, trendEMA: {self.trend_ema}')       
        else:
            if ((self.close <= self.stop_loss) | (self.close >= self.take_profit)):
                self.alpacaAPI.close_position()
                # self.side = ''
                print(f'Position closed with close price: {self.close} at {self.close}')

    def get_indicators(self, data):
        self.close = data.iloc[-1]['Close']
        self.short_ema = ta.EMA(data['Close'], self.short_period).iloc[-1]
        self.long_ema = ta.EMA(data['Close'], self.long_period).iloc[-1]
        self.previous_short_ema = ta.EMA(data['Close'], self.short_period).iloc[-2]
        self.previous_long_ema = ta.EMA(data['Close'], self.long_period).iloc[-2]
        self.atr = ta.ATR(data['High'], data['Low'], data['Close'], self.atr_period).iloc[-1]
        self.trend_ema = ta.SMA(data['Close'], self.trend_period).iloc[-1] + (self.trend_ema_offset * self.atr)

    def get_historical_data(self, start, end):
        if self.assetType == AssetType.Stock:
            return self.alpacaAPI.get_stock_data(start, end)
        elif self.assetType == AssetType.Crypto:
            return self.alpacaAPI.get_crypto_data(start, end)    