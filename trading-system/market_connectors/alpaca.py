from matplotlib import pyplot as plt
from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import requests

paper_api_key = 'PKHW6Z8TUF1VVA39U26G'
paper_api_secret = 'tKsOZxbzGTvTCgYZxPjf7nYpeJ09lbFzSX8InA4T'
paper_endpoint = 'https://paper-api.alpaca.markets/v2'

live_api_key = 'AKWS3QANE3F9QUM7UD0H'
live_api_secret = 'ZMtjbWs0RzEQjvCof4AQdxNRmZP6CHcZH21uLj8v'
live_endpoint = 'https://api.alpaca.markets'

stock_client = StockHistoricalDataClient(api_key=paper_api_key, secret_key=paper_api_secret)
crypto_client = CryptoHistoricalDataClient(api_key=paper_api_key, secret_key=paper_api_secret)

class AlpacaAPI:
    def __init__(self, ticker, historical_data_ticker, interval, environment = 'paper'):
        self.ticker = ticker
        self.historical_data_ticker = historical_data_ticker
        self.interval = interval
        if environment == 'paper':
            self.api_key = paper_api_key
            self.api_secret = paper_api_secret
            self.endpoint = paper_endpoint
        else:
            self.api_key = live_api_key
            self.api_secret = live_api_secret
            self.endpoint = live_endpoint
            
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }
        
    def get_stock_data(self, start, end):
        request_params = StockBarsRequest(
            symbol_or_symbols=[self.historical_data_ticker],
            timeframe= TimeFrame(self.interval, TimeFrameUnit.Minute),
            start=start,
            end=end
        )

        bars = stock_client.get_stock_bars(request_params)
        data = bars.df
        data.rename(columns = {'close':'Close', 'high':'High', 'low':'Low', 'open':'Open'}, inplace = True)
        return data.reset_index(['symbol']).drop(['symbol'], axis=1)


    def get_crypto_data(self, start, end):
        request_params = CryptoBarsRequest(
            symbol_or_symbols=[self.historical_data_ticker],
            timeframe= TimeFrame(self.interval, TimeFrameUnit.Minute),
            start=start,
            end=end
        )

        bars = crypto_client.get_crypto_bars(request_params)
        data = bars.df
        data.rename(columns = {'close':'Close', 'high':'High', 'low':'Low', 'open':'Open'}, inplace = True)
        return data.reset_index(['symbol']).drop(['symbol'], axis=1)
    
    
    def has_position(self):
        url = f'{self.endpoint}/positions/{self.ticker}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return True
        return False
    
    
    def close_position(self):
        url = f'{paper_endpoint}/positions/{self.ticker}'
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 200:
            print(f'Successfully closed position for {self.ticker}')
        else:
            print(f'Error occured when closing position for {self.ticker}')
    
    
    def create_order(self, amount, time_in_force, side, stop_loss_price = None, take_profit_price = None):
        url = f"{self.endpoint}/orders"
        payload = {
            "side": side,
            "type": 'market',
            "time_in_force": time_in_force,
            "notional": str(amount),
            "symbol": self.ticker,
        }
        
        if stop_loss_price is not None:
            payload["stop_loss"] = {"stop_price": str(stop_loss_price)}
        
        if take_profit_price is not None:
            payload["take_profit"] = {"limit_price": str(take_profit_price)}
        
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            print(f'Order created successfully for {self.ticker}')
        else:
            print(f'Error occured when creating order for {self.ticker}: {response.status_code}, {response.reason}')
        