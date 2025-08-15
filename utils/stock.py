import pandas as pd
import os
from typing import List, Dict, Optional


class StockInfo:
    """
    Represents a single day's stock data.
    """
    def __init__(self, symbol: str, date: str, open: float, close: float, high: float, low: float, volume: float):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume

    def __repr__(self) -> str:
        return (f"StockInfo(symbol={self.symbol}, date={self.date}, open={self.open}, "
                f"close={self.close}, high={self.high}, low={self.low}, volume={self.volume})")


class StockCenter:
    """
    Loads and provides access to stock data from CSV files in a data folder.
    Implements the singleton pattern.
    """
    _instance = None

    def __new__(cls, data_folder: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(StockCenter, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, data_folder: Optional[str] = None, is_all: bool = False):
        if self._initialized:
            return
        if data_folder is None:
            data_folder = os.path.join(os.path.dirname(__file__), '../data/stock/max' if is_all else '../data/stock/5y')
        self.data_folder = data_folder
        self.stock_info: Dict[str, Dict[str, StockInfo]] = {}
        self.symbols: List[str] = []
        self.dates_by_symbol: Dict[str, List[str]] = {}
        self._load_stock_data()
        self._initialized = True

    def _load_stock_data(self) -> None:
        """
        Loads all CSV files in the data folder and populates internal dictionaries for fast lookup.
        """
        print(f"[StockCenter] Loading stock data from: {self.data_folder}")
        symbols_set = set()
        for filename in os.listdir(self.data_folder):
            if filename.endswith('.csv'):
                print(f"[StockCenter] Loading file: {filename}")
                symbol = filename.split('_')[0]
                if symbol == 'VIX':
                    continue
                symbols_set.add(symbol)
                df = pd.read_csv(
                    os.path.join(self.data_folder, filename),
                    parse_dates=['date']
                )
                date_list = []
                info_dict = {}
                for _, row in df.iterrows():
                    date_key = row['date'].strftime('%Y-%m-%d')
                    stock_info = StockInfo(
                        symbol=symbol,
                        date=date_key,
                        open=row['open'],
                        close=row['close'],
                        high=row['high'],
                        low=row['low'],
                        volume=row['volume']
                    )
                    info_dict[date_key] = stock_info
                    date_list.append(date_key)
                self.dates_by_symbol[symbol] = sorted(date_list)
                self.stock_info[symbol] = info_dict
        self.symbols = sorted(symbols_set)
        print(f"[StockCenter] Loaded symbols: {self.symbols}")

    def get_symbols(self) -> List[str]:
        """
        Returns a sorted list of all stock symbols loaded.
        """
        return self.symbols

    def get_dates(self, code: str) -> List[str]:
        """
        Returns a sorted list of all available dates (as datetime) for a given stock symbol.
        """
        if code not in self.dates_by_symbol:
            raise KeyError(f"No dates found for symbol: {code}")
        return self.dates_by_symbol[code]

    def get_latest_date(self, code: str) -> str:
        """
        Returns the latest available date (as datetime) for a given stock symbol.
        """
        dates = self.get_dates(code)
        if not dates:
            raise KeyError(f"No dates found for symbol: {code}")
        return dates[-1]

    def get_stock_info(self, code: str, date: str) -> StockInfo:
        """
        Returns StockInfo for the given code and date.
        Accepts date as a string ('yyyy-mm-dd').
        Raises KeyError if not found.
        """
        if code not in self.stock_info:
            raise KeyError(f"No data for symbol: {code}")
        if date not in self.stock_info[code]:
            raise KeyError(f"No data for {code} on {date}")
        return self.stock_info[code][date]

    def is_valid_date(self, code: str, date: str) -> bool:
        """
        Checks if the given date is valid (exists in the data) for the specified stock symbol.
        Accepts date as a string ('yyyy-mm-dd').
        Returns True if valid, False otherwise.
        """
        if code not in self.dates_by_symbol:
            return False
        return date in self.dates_by_symbol[code]
