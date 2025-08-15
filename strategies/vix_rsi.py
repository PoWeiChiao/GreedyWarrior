from utils.profolio import Profolio
from utils.vix import VixCenter
from utils.stock import StockCenter


class VixRSI:
    def __init__(self, profolio: Profolio):
        self.profolio = profolio
        self.vix_center = VixCenter()
        self.stock_center = StockCenter()

    def execute(self, code: str, start_date: str, end_date: str, vix_threshold: float, rsi2_threshold: float = -1, rsi14_threshold: float = -1) -> None:
        """
        Executes a VIX RSI strategy:
        - Buys when VIX is above vix_threshold.
        - Sells when VIX is below vix_threshold.
        - Prints log for each action: date, action, price, and RSI values.
        """
        print("="*60)
        print(f"VIX RSI Execution from {start_date} to {end_date}")
        print(f"RSI2 Threshold: {rsi2_threshold}, RSI14 Threshold: {rsi14_threshold}")
        print("="*60)

        for date, vix_info in self.vix_center.vix_data.items():
            if date < start_date or date > end_date:
                continue

            if vix_info.high > vix_threshold:
                price = 0
                if rsi2_threshold != -1 and vix_info.rsi2 > rsi2_threshold:
                    price = self.stock_center.get_stock_info(code, date).close
                elif rsi14_threshold != -1 and vix_info.rsi14 > rsi14_threshold:
                    price = self.stock_center.get_stock_info(code, date).close
                else:
                    price = self.stock_center.get_stock_info(code, date).close
                print(f"[{date}] Buy {code} at {price:.2f} (VIX: {vix_info.high:.2f}) (RSI2: {vix_info.rsi2:.2f}) (RSI14: {vix_info.rsi14:.2f})")