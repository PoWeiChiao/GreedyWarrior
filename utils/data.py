import os
from typing import List, Dict, Optional
import pandas as pd
import talib as ta


class DataInfo:
    """Represents a single day's data."""

    def __init__(
        self, symbol: str, date: str, open: float, close: float, high: float,
        low: float, volume: float, rsi2: float, rsi14: float, sma_50: float, sma_200: float
    ):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.rsi2 = rsi2
        self.rsi14 = rsi14
        self.sma_50 = sma_50
        self.sma_200 = sma_200

    def __repr__(self) -> str:
        return (f"DataInfo(symbol={self.symbol}, date={self.date}, open={self.open}, "
                f"close={self.close}, high={self.high}, low={self.low}, volume={self.volume})")


class DataCenter:
    """Loads and provides access to data from CSV files in a data folder.
    Implements the singleton pattern.
    """
    _instance = None

    def __new__(cls, data_folder: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, data_folder: Optional[str] = None, is_all: bool = False):
        if self._initialized:
            return
        self.data_folder = data_folder or os.path.join(
            os.path.dirname(__file__), '../data/max' if is_all else '../data/5y'
        )
        self.data_info: Dict[str, Dict[str, DataInfo]] = {}
        self.symbols: List[str] = []
        self.dates_by_symbol: Dict[str, List[str]] = {}
        self._load_data()
        self._initialized = True

    def _load_data(self) -> None:
        """Loads all CSV files in the data folder and populates internal dictionaries for fast lookup."""
        print(f"[DataCenter] Loading data data from: {self.data_folder}")
        symbols_set = set()
        for filename in os.listdir(self.data_folder):
            if filename.endswith('.csv'):
                self._process_file(filename, symbols_set)
        self.symbols = sorted(symbols_set)
        print(f"[DataCenter] Loaded symbols: {self.symbols}")

    def _process_file(self, filename: str, symbols_set: set) -> None:
        """Helper function to process each CSV file."""
        print(f"[DataCenter] Loading file: {filename}")
        symbol = filename.split('_')[0]
        symbols_set.add(symbol)
        df = pd.read_csv(os.path.join(self.data_folder, filename), parse_dates=['date'])
        
        indicators = self._calculate_indicators(df)
        date_list, info_dict = [], {}

        for i, row in df.iterrows():
            date_key = row['date'].strftime('%Y-%m-%d')
            data_info = DataInfo(
                symbol=symbol,
                date=date_key,
                open=row['open'],
                close=row['close'],
                high=row['high'],
                low=row['low'],
                volume=row['volume'],
                rsi2=indicators.get('rsi_2', pd.Series([-1]))[i],
                rsi14=indicators.get('rsi_14', pd.Series([-1]))[i],
                sma_50=indicators.get('sma_50', pd.Series([-1]))[i],
                sma_200=indicators.get('sma_200', pd.Series([-1]))[i]
            )
            info_dict[date_key] = data_info
            date_list.append(date_key)

        self.dates_by_symbol[symbol] = sorted(date_list)
        self.data_info[symbol] = info_dict

    def _calculate_indicators(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculates needed indicators (RSI and SMA)."""
        indicators = {}
        if 'close' in df:
            indicators['rsi_2'] = ta.RSI(df['close'], timeperiod=2).fillna(-1)
            indicators['rsi_14'] = ta.RSI(df['close'], timeperiod=14).fillna(-1)
            indicators['sma_50'] = df['close'].rolling(window=50).mean().fillna(-1)
            indicators['sma_200'] = df['close'].rolling(window=200).mean().fillna(-1)
        return indicators

    def get_symbols(self) -> List[str]:
        """Returns a sorted list of all data symbols loaded."""
        return self.symbols

    def get_dates(self, code: str) -> List[str]:
        """Returns a sorted list of all available dates for a given data symbol."""
        if code not in self.dates_by_symbol:
            raise KeyError(f"No dates found for symbol: {code}")
        return self.dates_by_symbol[code]

    def get_latest_date(self, code: str) -> str:
        """Returns the latest available date for a given data symbol."""
        dates = self.get_dates(code)
        if not dates:
            raise KeyError(f"No dates found for symbol: {code}")
        return dates[-1]

    def get_data_info(self, code: str, date: str) -> DataInfo:
        """Returns DataInfo for the given code and date."""
        if code not in self.data_info:
            raise KeyError(f"No data for symbol: {code}")
        if date not in self.data_info[code]:
            raise KeyError(f"No data for {code} on {date}")
        return self.data_info[code][date]

    def is_valid_date(self, code: str, date: str) -> bool:
        """Checks if the given date is valid for the specified data symbol."""
        return code in self.dates_by_symbol and date in self.dates_by_symbol[code]