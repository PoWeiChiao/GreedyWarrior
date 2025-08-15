from datetime import datetime
from strategies.dca import DCA
from strategies.vix_rsi import VixRSI
from utils.profolio import Profolio
from utils.stock import StockCenter


class Simulator:
    def __init__(self):
        self.profolio = Profolio(initial_cash=0.0)

    def execute_dca(self):
        dca = DCA(self.profolio)
        dca.execute(
            code='NVDA',
            start_time=datetime(2025, 4, 1),
            end_time=datetime(2025, 8, 13),
            interval=14,
            cost=1000
        )

    def execute_vix_rsi(self):
        vix_rsi = VixRSI(self.profolio)
        vix_rsi.execute(
            code='TQQQ',
            start_date='2021-01-01',
            end_date='2025-08-13',
            vix_threshold=30.0,
            rsi2_threshold=-1,
            rsi14_threshold=-1
        )