import datetime
from utils.simulator import Simulator
from utils.data import DataCenter


def main():
    simulator = Simulator()
    # start_date = datetime.datetime(2023, 1, 1)
    # end_date = datetime.datetime(2025, 8, 13)
    # interval = 14
    # cost = 2000
    # simulator.execute_dca('TQQQ', start_date, end_date, interval, cost)
    # simulator.execute_buy_dip(
    #     start_date='2022-01-01',
    #     end_date='2025-08-13',
    #     vix_threshold=30,
    #     vix_rsi2_threshold=90,
    #     sp500_rsi2_threshold=30,
    #     sp500_sma200=True
    # )
    simulator.execute_sell_high(
        start_date='2022-01-01',
        end_date='2025-08-13',
        vix_threshold=20,
        vix_rsi2_threshold=10,
        sp500_rsi2_threshold=65,
        sp500_sma200=True)
    # simulator.execute_dca('QLD', start_date, end_date, interval, cost)
    # simulator.execute_dca('QQQ', start_date, end_date, interval, cost)
    # simulator.execute_dca('NVDA', start_date, end_date, interval, cost)
    # simulator.execute_dca('AAPL', start_date, end_date, interval, cost)
    # simulator.execute_dca('MSFT', start_date, end_date, interval, cost)
    # simulator.execute_dca('GOOGL', start_date, end_date, interval, cost)
    # simulator.execute_dca('AMZN', start_date, end_date, interval, cost)
    
if __name__ == "__main__":
    main()