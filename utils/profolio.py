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
        return self.holdings_info[code].shares if code in self.holdings_info else 0.0

    def get_holding_average_price(self, code: str) -> float:
        return self.holdings_info[code].average_price if code in self.holdings_info else 0.0
    
    def get_holding_value(self, code: str, current_price: float) -> float:
        if code in self.holdings_info:
            shares = self.holdings_info[code].shares
            return shares * current_price
        return 0.0
    
    def add_cash(self, amount: float) -> None:
        self.cash += amount

    def subtract_cash(self, amount: float) -> None:
        if amount <= self.cash:
            self.cash -= amount
        else:
            raise ValueError("Insufficient cash to subtract the specified amount.")
        
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
        total_cost = shares_bought * price
        if shares_bought == 0:
            raise ValueError("Not enough cash to buy at least one share.")
        self.cash -= total_cost

        # Update or create HoldingInfo
        if code in self.holdings_info:
            holding = self.holdings_info[code]
            total_shares = holding.shares + shares_bought
            total_cost_accum = holding.shares * holding.average_price + total_cost
            new_avg_price = total_cost_accum / total_shares
            holding.shares = total_shares
            holding.average_price = new_avg_price
        else:
            self.holdings_info[code] = HoldingInfo(shares=shares_bought, average_price=price)

        # Update holdings list: append the purchase price for each share bought
        if code not in self.holdings:
            self.holdings[code] = []
        self.holdings[code].extend([price] * shares_bought)
    
    def sell_stock(self, code: str, shares_to_sell: float, price: float) -> None:
        """
        Sell a specified number of shares of a stock.
        Updates holdings and holdings_info.
        """
        if code not in self.holdings_info:
            raise KeyError(f"No holdings for stock: {code}")
        
        holding = self.holdings_info[code]
        if shares_to_sell > holding.shares:
            raise ValueError("Not enough shares to sell.")
        
        total_revenue = shares_to_sell * price
        holding.shares -= shares_to_sell
        self.cash += total_revenue
        
        # Remove the sold shares from the holdings list
        for _ in range(int(shares_to_sell)):
            if self.holdings[code]:
                self.holdings[code].pop(0)
        
        # Update average price if shares remain, else remove holding info
        if holding.shares == 0:
            del self.holdings_info[code]
            self.holdings.pop(code, None)
        else:
            # Recalculate average price based on remaining purchase prices
            if self.holdings[code]:
                holding.average_price = sum(self.holdings[code]) / len(self.holdings[code])
            else:
                holding.average_price = 0.0
    
    def buy_stock_by_shares(self, code: str, shares_to_buy: int, price: float) -> None:
        """
        Buy a specific number of shares of a stock.
        Updates holdings and holdings_info.
        Records each purchase price in the holdings list.
        """
        total_cost = shares_to_buy * price
        if total_cost > self.cash:
            raise ValueError("Not enough cash to buy the specified number of shares.")
        if shares_to_buy <= 0:
            raise ValueError("Number of shares to buy must be positive.")
        self.cash -= total_cost

        # Update or create HoldingInfo
        if code in self.holdings_info:
            holding = self.holdings_info[code]
            total_shares = holding.shares + shares_to_buy
            total_cost_accum = holding.shares * holding.average_price + total_cost
            new_avg_price = total_cost_accum / total_shares
            holding.shares = total_shares
            holding.average_price = new_avg_price
        else:
            self.holdings_info[code] = HoldingInfo(shares=shares_to_buy, average_price=price)

        # Update holdings list: append the purchase price for each share bought
        if code not in self.holdings:
            self.holdings[code] = []
        self.holdings[code].extend([price] * shares_to_buy)