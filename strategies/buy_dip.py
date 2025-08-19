from utils.profolio import Profolio
from utils.data import StockCenter
from utils.vix import VixCenter


class BuyDip:
    def __init__(self, profolio: Profolio):
        self.profolio = profolio
        self.vix_center = VixCenter()
        self.stock_center = StockCenter()

    def get_dip(self, start_date: str, end_date: str, rsi2_threshold: float = 90) -> None:
        """
        Executes a Buy Dip strategy:
        - Buys when RSI2 is above the threshold.
        - Prints log for each action: date, action, price, and RSI values.
        """
        print("="*60)
        print(f"Buy Dip Execution from {start_date} to {end_date}")
        print(f"RSI2 Threshold: {rsi2_threshold}")
        print("="*60)

        for date, vix_info in self.vix_center.vix_data.items():
            if date < start_date or date > end_date:
                continue

            if vix_info.rsi2 >= rsi2_threshold:
                print(f"[{date}] (VIX: {vix_info.high:.2f}) (RSI2: {vix_info.rsi2:.2f}) (RSI14: {vix_info.rsi14:.2f})")

    def execute(self, code: str, start_date: str, end_date: str, rsi2_threshold: float = 90) -> None:
        return
