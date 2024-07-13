from typing import Literal
from all_weather.market import get_price
from pydantic import BaseModel


class Allocation(BaseModel):
    symbol: str
    percent: float
    description: str


class Position(BaseModel):
    symbol: str
    quantity: int


class Instruction(BaseModel):
    symbol: str
    action: Literal["BUY", "SELL"]
    quantity: int
    price: float
    description: str | None = None

    def __str__(self) -> str:
        return f"{self.symbol:<10} {self.action:<10} {self.quantity:<10} @ ${self.price:<10.2f} | {self.description}"


class Portfolio:
    def __init__(self, value: float, allocations: list[Allocation]):
        self.value = value
        self.cash = value
        self.allocations = allocations
        self.positions = [Position(symbol=allocation.symbol, quantity=0) for allocation in self.allocations]

    def allocate(self, prices: dict[str, float] | None = None) -> list[Instruction]:
        instructions = []
        positions = [position.symbol for position in self.positions]

        for allocation in self.allocations:
            if allocation.symbol in positions:
                # Get the price of the asset, if it is provided
                price = prices.get(allocation.symbol) if prices else None

                # Adjust an existing position
                instruction = self._adjust(allocation.symbol, allocation.percent, price)
                if not instruction:
                    # There is no need to adjust this position
                    continue
                instructions.append(instruction)
            else:
                # Add a new position

                # Get the price of the asset, if it is provided
                price = prices.get(allocation.symbol) if prices else None

                instruction = self._add(allocation.symbol, allocation.percent, price)
                instructions.append(instruction)

        return instructions

    def _add(self, symbol: str, allocation: float, price: float | None = None) -> Instruction:
        "Add a new position"
        assert allocation > 0 and allocation <= 1, "Allocation must be a percentage"

        # Get the price of the asset
        if not price:
            price = get_price(symbol)

        # The part of the portfolio that should be allocated to this asset
        quantity = (allocation * self.value) // price

        return Instruction(
            symbol=symbol,
            action="BUY",
            quantity=int(quantity),
            price=price,
            description="New position",
        )

    def _adjust(self, symbol: str, allocation: float, price: float | None = None) -> Instruction | None:
        """Adjust an existing position"""
        assert allocation > 0 and allocation <= 1, "Allocation must be a percentage"

        # Get the price of the asset
        if not price:
            price = get_price(symbol)

        # Calculate the difference from the current position allocation to the target allocation
        position = next((position for position in self.positions if position.symbol == symbol))
        current_value = price * position.quantity
        target_value = allocation * self.value
        difference = target_value - current_value

        # Calculate the quantity of shares to buy or sell
        quantity = difference // price

        # If the difference is tiny, we don't need to buy or sell anything
        if quantity == 0:
            return None

        return Instruction(
            symbol=symbol,
            action="BUY" if quantity > 0 else "SELL",
            quantity=int(abs(quantity)),
            price=price,
            description=f"Adjust position from {position.quantity} to {int(position.quantity + quantity)}",
        )
