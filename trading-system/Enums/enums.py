from enum import Enum


class AssetType(Enum):
    Crypto = 'Crypto'
    Stock = 'Stock'
    Currency = 'Currency'
    
class Side(Enum):
    Buy = 'buy'
    Sell = 'sell'

class PositionType(Enum):
    Long = 'long'
    Short = 'short'
    
class Assets(Enum):
    BTCUSD = 'BTC/USD'