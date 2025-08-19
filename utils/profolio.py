from typing import List, Dict

class HoldingInfo:
    def __init__(self, shares: float, average_price: float):
        self.shares = shares
        self.average_price = average_price

    def __repr__(self):
        return f"HoldingInfo(shares={self.shares}, average_price={self.average_price})"


class Profolio:
    def __init__(self, initial_cash: float):
        self.cash = initial_cash
        self.holdings: Dict[str, List[float]] = {}
        self.holdings_info: Dict[str, HoldingInfo] = {}

    def get_cash(self) -> float:
        return self.cash

    def get_holding_list(self) -> List[str]:
        return list(self.holdings.keys())

    def get_holding_shares(self, code: str) -> float:
        return self.holdings_info.get(code, HoldingInfo(0.0, 0.0)).shares

    def get_holding_average_price(self, code: str) -> float:
        return self.holdings_info.get(code, HoldingInfo(0.0, 0.0)).average_price

    def get_holding_value(self, code: str, current_price: float) -> float:
        shares = self.get_holding_shares(code)
        return shares * current_price

    def add_cash(self, amount: float) -> None:
        self.cash += amount

    def subtract_cash(self, amount: float) -> None:
        if amount > self.cash:
            raise ValueError("Insufficient cash to subtract the specified amount.")
        self.cash -= amount

    def _update_or_create_holding_info(self, code: str, shares: int, price: float) -> None:
        if code in self.holdings_info:
            holding = self.holdings_info[code]
            total_shares = holding.shares + shares
            total_cost = holding.shares * holding.average_price + shares * price
            holding.shares = total_shares
            holding.average_price = total_cost / total_shares
        else:
            self.holdings_info[code] = HoldingInfo(shares=shares, average_price=price)

    def buy_stock(self, code: str, cash_to_invest: float, price: float) -> None:
        """
        Buy stock with a fixed cash amount.
        Updates holdings and holdings_info.
        Only allows buying integer number of shares.
        Records each purchase price in the holdings list.
        """
        if cash_to_invest > self.cash:
            raise ValueError("Not enough cash to buy stock.")
        shares_bought = int(cash_to_invest // price)
        if shares_bought == 0:
            raise ValueError("Not enough cash to buy at least one share.")
        total_cost = shares_bought * price
        self.subtract_cash(total_cost)

        # Manage holdings
        self._update_or_create_holding_info(code, shares_bought, price)
        self.holdings.setdefault(code, []).extend([price] * shares_bought)

    def sell_stock(self, code: str, shares_to_sell: float, price: float) -> None:
        """
        Sell a specified number of shares of a stock.
        Updates holdings and holdings_info.
        """
        if code not in self.holdings_info or shares_to_sell > self.get_holding_shares(code):
            raise ValueError("Not enough shares to sell.")

        holding = self.holdings_info[code]
        total_revenue = shares_to_sell * price
        holding.shares -= shares_to_sell
        self.add_cash(total_revenue)

        for _ in range(int(shares_to_sell)):
            self.holdings[code].pop(0)

        if holding.shares == 0:
            del self.holdings_info[code]
            self.holdings.pop(code, None)
        else:
            holding.average_price = sum(self.holdings[code]) / len(self.holdings[code]) if self.holdings[code] else 0.0

    def buy_stock_by_shares(self, code: str, shares_to_buy: int, price: float) -> None:
        """
        Buy a specific number of shares of a stock.
        Updates holdings and holdings_info.
        Records each purchase price in the holdings list.
        """
        if shares_to_buy <= 0:
            raise ValueError("Number of shares to buy must be positive.")
        total_cost = shares_to_buy * price
        if total_cost > self.cash:
            raise ValueError("Not enough cash to buy the specified number of shares.")
        self.subtract_cash(total_cost)

        # Manage holdings
        self._update_or_create_holding_info(code, shares_to_buy, price)
        self.holdings.setdefault(code, []).extend([price] * shares_to_buy)