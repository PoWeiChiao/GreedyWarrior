import datetime
from utils.simulator import Simulator
from utils.vix import VixCenter


def main():
    simulator = Simulator()
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2025, 8, 13)
    interval = 14
    cost = 2000
    simulator.execute_dca('TQQQ', start_date, end_date, interval, cost)
    simulator.execute_dca('QLD', start_date, end_date, interval, cost)
    simulator.execute_dca('QQQ', start_date, end_date, interval, cost)
    simulator.execute_dca('NVDA', start_date, end_date, interval, cost)
    simulator.execute_dca('AAPL', start_date, end_date, interval, cost)
    simulator.execute_dca('MSFT', start_date, end_date, interval, cost)
    simulator.execute_dca('GOOGL', start_date, end_date, interval, cost)
    simulator.execute_dca('AMZN', start_date, end_date, interval, cost)
    # simulator.execute_vix_rsi()

if __name__ == "__main__":
    main()