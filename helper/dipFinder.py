from utils.data import DataCenter


class DipFinder:
    def __init__(self, vix_threshold: float = 40, vix_rsi2_threshold: float = 90, sp500_rsi2_threshold: float = 30, sp500_sma200: bool = True):
        self.data_center = DataCenter()
        self.vix_threshold = vix_threshold
        self.vix_rsi2_threshold = vix_rsi2_threshold
        self.sp500_rsi2_threshold = sp500_rsi2_threshold
        self.sp500_sma200 = sp500_sma200

    def find_dips(self, start_date: str, end_date: str) -> list:
        dips = []
        sp500 = self.data_center.data_info.get('SP500', {})
        vix = self.data_center.data_info.get('VIX', {})

        for date in vix:
            if date < start_date or date > end_date:
                continue    
            if date not in sp500:
                continue
            if self.sp500_sma200 and sp500[date].close < sp500[date].sma_200:
                continue
            if vix[date].high >= self.vix_threshold and vix[date].rsi2 >= self.vix_rsi2_threshold and sp500[date].rsi2 <= self.sp500_rsi2_threshold:
                dips.append(date)
                print(f"[{date}] (VIX: {vix[date].high:.2f}) (VIX RSI2: {vix[date].rsi2:.2f}) (SP500 RSI2: {sp500[date].rsi2:.2f}) (SP500: {sp500[date].close:.2f}) (SP500 SMA200: {sp500[date].sma_200:.2f})")
        return dips