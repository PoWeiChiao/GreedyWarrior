from utils.profolio import Profolio
from utils.data import DataCenter


class BuyDip:
    def __init__(self, profolio: Profolio):
        self.profolio = profolio
        self.data_center = DataCenter()

    def get_dip(self, start_date: str, end_date: str, vix_threshold: float = 30, vix_rsi2_threshold: float = 90, sp500_rsi2_threshold: float = 30, sp500_sma200: bool = True) -> None:
        """
        Executes a Buy Dip strategy:
        - Buys when RSI2 is above the threshold.
        - Prints log for each action: date, action, price, and RSI values.
        """
        print("="*60)
        print(f"Buy Dip Execution from {start_date} to {end_date}")
        print(f"VIX Threshold: {vix_threshold}")
        print(f"VIX RSI2 Threshold: {vix_rsi2_threshold}")
        print(f"S&P 500 RSI2 Threshold: {sp500_rsi2_threshold}")
        print(f"S&P 500 SMA200: {'Enabled' if sp500_sma200 else 'Disabled'}")
        print("="*60)

        sp500 = self.data_center.data_info.get('SP500', {})
        vix = self.data_center.data_info.get('VIX', {})

        for date in vix:
            if date < start_date or date > end_date:
                continue    
            if date not in sp500:
                continue
            if vix[date].high >= vix_threshold:
                print(f"[{date}] (VIX: {vix[date].high:.2f}) (VIX RSI2: {vix[date].rsi2:.2f}) (SP500 RSI2: {sp500[date].rsi2:.2f}) (SP500: {sp500[date].close:.2f}) (SP500 SMA200: {sp500[date].sma_200:.2f})")

    def get_high(self, start_date: str, end_date: str, vix_threshold: float = 20, vix_rsi2_threshold: float = 10, sp500_rsi2_threshold: float = 65, sp500_sma200: bool = True) -> None:
        """ Executes a Buy Dip strategy to find high points."""
        print("="*60)
        print(f"Buy Dip Execution from {start_date} to {end_date}")
        print(f"VIX Threshold: {vix_threshold}")
        print(f"VIX RSI2 Threshold: {vix_rsi2_threshold}")
        print(f"S&P 500 RSI2 Threshold: {sp500_rsi2_threshold}")
        print(f"S&P 500 SMA200: {'Enabled' if sp500_sma200 else 'Disabled'}")
        print("="*60)

        sp500 = self.data_center.data_info.get('SP500', {})
        vix = self.data_center.data_info.get('VIX', {})

        for date in vix:
            if date < start_date or date > end_date:
                continue    
            if date not in sp500:
                continue
            if vix[date].close <= vix_threshold and vix[date].rsi2 <= vix_rsi2_threshold and sp500[date].rsi2 >= sp500_rsi2_threshold and sp500[date].close > sp500_sma200:
                print(f"[{date}] (VIX: {vix[date].high:.2f}) (VIX RSI2: {vix[date].rsi2:.2f}) (SP500 RSI2: {sp500[date].rsi2:.2f}) (SP500: {sp500[date].close:.2f}) (SP500 SMA200: {sp500[date].sma_200:.2f})")

    def execute(self, code: str, start_date: str, end_date: str, rsi2_threshold: float = 90) -> None:
        return
