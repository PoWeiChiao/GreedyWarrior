from datetime import datetime
from strategies.dca import DCA
from strategies.vix_rsi import VixRSI
from utils.profolio import Profolio
from utils.stock import StockCenter


class Simulator:
    def __init__(self):
        self.stock_center = StockCenter()
        self.profolio = Profolio(initial_cash=0.0)

    def execute_dca(self, code: str = 'TQQQ', start_date: datetime = datetime(2025, 1, 1), end_date: datetime = datetime(2025, 8, 13), interval: int = 14, cost: float = 2000):
        """ Executes a Dollar-Cost Averaging (DCA) strategy. """
        print("Executing DCA strategy...")
        dca = DCA(Profolio(initial_cash=0.0))
        dca.execute(
            code=code,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            cost=cost
        )

    def execute_vix_rsi(self, code: str = 'TQQQ', start_date: str = '2021-01-01', end_date: str = '2025-08-13', vix_threshold: float = 30.0, rsi2_threshold: float = -1, rsi14_threshold: float = -1):
        vix_rsi = VixRSI(Profolio(initial_cash=0.0))
        vix_rsi.execute(
            code=code,
            start_date=start_date,
            end_date=end_date,
            vix_threshold= vix_threshold,
            rsi2_threshold=rsi2_threshold,
            rsi14_threshold=rsi14_threshold
        )