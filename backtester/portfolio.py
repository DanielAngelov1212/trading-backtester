class Portfolio:

    def __init__(self, initial_capital: float) -> None:
        if initial_capital <= 0:
            raise ValueError("Initial capital must be positive.")

        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.shares = 0
        self.trades = []

    def buy(self, price: float) -> None:
        if price <= 0:
            raise ValueError("Price must be positive.")

        if self.cash < price:
            return

        quantity = int(self.cash // price)

        if quantity == 0:
            return

        cost = quantity * price

        self.cash -= cost
        self.shares += quantity

        self.trades.append(
            {
                "action": "BUY",
                "price": price,
                "quantity": quantity,
            }
        )

    def sell(self, price: float) -> None:
        if price <= 0:
            raise ValueError("Price must be positive.")

        if self.shares == 0:
            return

        quantity = self.shares

        self.cash += quantity * price
        self.shares = 0

        self.trades.append(
            {
                "action": "SELL",
                "price": price,
                "quantity": quantity,
            }
        )

    def get_value(self, current_price: float) -> float:
        if current_price <= 0:
            raise ValueError("Price must be positive.")

        return self.cash + self.shares * current_price