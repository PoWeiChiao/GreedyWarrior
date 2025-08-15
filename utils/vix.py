import os
from typing import Dict, List, Optional
import pandas as pd


class VixInfo:
    """
    Represents a single day's vix data.
    """
    def __init__(self, date: str, open: float, close: float, high: float, low: float):
        self.date = date
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.rsi2 = -1
        self.rsi14 = -1

    def set_rsi(self, rsi2: float, rsi14: float) -> None:
        """
        Sets the RSI values for this VIX info.
        """
        self.rsi2 = rsi2
        self.rsi14 = rsi14

    def __repr__(self) -> str:
        return (f"VixInfo(date={self.date}, open={self.open}, close={self.close}, "
                f"high={self.high}, low={self.low}, rsi2={self.rsi2:2f}, rsi14={self.rsi14:2f})")
    
class VixCenter:
    """
    Loads and provides access to VIX data from a CSV file.
    Implements the singleton pattern.
    """
    _instance = None

    def __new__(cls, data_file: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(VixCenter, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, data_file: Optional[str] = None, is_all: bool = False):
        if self._initialized:
            return
        if data_file is None:
            data_file = os.path.join(os.path.dirname(__file__), '../data/vix/max/VIX_MAX_FROM_PERPLEXITY.csv' if is_all else '../data/vix/5y/VIX_5Y_FROM_PERPLEXITY.csv')
        self.data_file = data_file
        self.vix_data: Dict[str, VixInfo] = {}
        self._load_vix_data()
        self._initialized = True

    def _load_vix_data(self) -> None:
        """
        Loads VIX data from the specified CSV file.
        """
        print(f"[VixCenter] Loading VIX data from: {self.data_file}")
        df = pd.read_csv(self.data_file, parse_dates=['date'])
        date_list = []
        for _, row in df.iterrows():
            date_key = row['date'].strftime('%Y-%m-%d')
            vix_info = VixInfo(
                date=date_key,
                open=row['open'],
                close=row['close'],
                high=row['high'],
                low=row['low'],
            )
            self.vix_data[date_key] = vix_info
            date_list.append(date_key)
            rsi_2 = self._get_rsi(date_list, 2)
            rsi_14 = self._get_rsi(date_list, 14)
            self.vix_data[date_key].set_rsi(rsi_2, rsi_14)
        print(f"[VixCenter] Loaded {len(self.vix_data)} VIX records.")

    def _get_rsi(self, date_list: List[str], rsi_period: int) -> float:
        """
        Calculates RSI for the given date list and period.
        """
        if len(date_list) < rsi_period + 1:
            return -1

        gains = []
        losses = []
        for i in range(1, len(date_list)):
            change = self.vix_data[date_list[i]].close - self.vix_data[date_list[i-1]].close
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(-change)

        avg_gain = sum(gains[-rsi_period:]) / rsi_period
        avg_loss = sum(losses[-rsi_period:]) / rsi_period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi