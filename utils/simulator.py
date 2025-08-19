from datetime import datetime
from strategies.dca import DCA
from utils.profolio import Profolio
from utils.data import DataCenter


class Simulator:
    def __init__(self):
        self.data_center = DataCenter()
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