from datetime import datetime, timedelta
from utils.profolio import Profolio
from utils.stock import StockCenter

class DCA:
    def __init__(self, profolio: Profolio):
        self.profolio = profolio
        self.stockCenter = StockCenter()

    def execute(self, code: str, start_time: str, end_time: str, interval: int = 30, cost: float = 3000) -> None:
        """
        Executes a Dollar-Cost Averaging (DCA) strategy:
        - Buys stock at regular intervals (in days) between start_time and end_time.
        - Only buys on valid trading days.
        - Adds cash to the portfolio if needed.
        - Prints log for each buy: date, shares, price, and return rate.
        """
        print("="*60)
        print(f"DCA Execution for {code}")
        print(f"Start date: {start_time.strftime('%Y-%m-%d')}")
        print(f"End date:   {end_time.strftime('%Y-%m-%d')}")
        print(f"Interval:   {interval} days")
        print(f"Amount per buy: {cost:.2f}")
        print("="*60)

        current_time = start_time

        while current_time <= end_time:
            # Find the next valid trading day on or after current_time
            while current_time <= end_time and not self.stockCenter.is_valid_date(code, current_time.strftime('%Y-%m-%d')):
                current_time += timedelta(days=1)
            if current_time > end_time:
                break

            stock_info = self.stockCenter.get_stock_info(code, current_time.strftime('%Y-%m-%d'))
            # Ensure enough cash is available
            if self.profolio.get_cash() < cost:
                self.profolio.add_cash(cost)
            shares_to_buy = int(cost // stock_info.close)
            if shares_to_buy == 0:
                print(f"[{current_time.strftime('%Y-%m-%d')}] Not enough cash to buy at least one share at price {stock_info.close:.2f}")
                current_time += timedelta(days=interval)
                continue
            self.profolio.buy_stock(code, cost, stock_info.close)
            # Calculate return after buying
            return_rate = self.get_return(code, current_time) * 100
            print(f"[{current_time.strftime('%Y-%m-%d')}] Bought {shares_to_buy} shares at {stock_info.close:.2f} per share.")
            print(f"[{current_time.strftime('%Y-%m-%d')}] Holding {self.profolio.get_holding_shares(code)} shares at average price {self.profolio.get_holding_average_price(code):.2f}.")
            print(f"Average price {self.profolio.get_holding_average_price(code):.2f} Current price: {stock_info.close:.2f} Return: {return_rate:.2f}%")
            current_time += timedelta(days=interval)

    def get_return(self, code: str, current_date: datetime) -> float:
        """
        Calculates the total return of the portfolio for the given stock code as of current_date.
        Return is (current_value + cash - total_invested) / total_invested.
        """
        # Get current price
        if not self.stockCenter.is_valid_date(code, current_date.strftime('%Y-%m-%d')):
            raise ValueError("Invalid date for the given stock code.")
        stock_info = self.stockCenter.get_stock_info(code, current_date.strftime('%Y-%m-%d'))
        current_price = stock_info.close

        # Get holding value and cash
        holding_shares = self.profolio.get_holding_shares(code)
        holding_value = holding_shares * current_price
        cash = self.profolio.get_cash()

        # Calculate total invested
        # Sum up all purchase prices for this code
        if code in self.profolio.holdings:
            total_invested = sum(self.profolio.holdings[code])
        else:
            total_invested = 0.0

        if total_invested == 0:
            return 0.0

        total_value = holding_value + cash
        return (total_value - total_invested) / total_invested