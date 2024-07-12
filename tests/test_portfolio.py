import pytest
from all_weather.portfolio import Instruction, Portfolio, Allocation, Position


@pytest.mark.usefixtures("setup")
def test_portfolio_allocate_first_allocation():
    portfolio = Portfolio(
        value=10000.00,
        allocations=[
            Allocation(percent=0.30, symbol="VOO", description="S&P 500"),
            Allocation(percent=0.40, symbol="VGLT", description="Long-Term Treasury"),
            Allocation(percent=0.15, symbol="VGIT", description="Intermediate-Term Treasury"),
            Allocation(percent=0.075, symbol="GLD", description="Gold"),
            Allocation(percent=0.075, symbol="GSG", description="Commodities"),
        ],
        positions=[],
    )

    instructions = portfolio.allocate()

    expected = [
        Instruction(symbol="VOO", action="BUY", quantity=30, price=100.0, description="New position"),
        Instruction(symbol="VGLT", action="BUY", quantity=40, price=100.0, description="New position"),
        Instruction(symbol="VGIT", action="BUY", quantity=15, price=100.0, description="New position"),
        Instruction(symbol="GLD", action="BUY", quantity=7, price=100.0, description="New position"),
        Instruction(symbol="GSG", action="BUY", quantity=7, price=100.0, description="New position"),
    ]

    assert instructions == expected


@pytest.mark.usefixtures("setup")
def test_portfolio_allocate_second_allocation():
    portfolio = Portfolio(
        value=10000.00,
        allocations=[
            Allocation(percent=0.30, symbol="VOO", description="S&P 500"),
            Allocation(percent=0.40, symbol="VGLT", description="Long-Term Treasury"),
            Allocation(percent=0.15, symbol="VGIT", description="Intermediate-Term Treasury"),
            Allocation(percent=0.075, symbol="GLD", description="Gold"),
            Allocation(percent=0.075, symbol="GSG", description="Commodities"),
        ],
        positions=[
            Position(symbol="VOO", quantity=1),
            Position(symbol="VGLT", quantity=6),
            Position(symbol="VGIT", quantity=1),
            Position(symbol="GLD", quantity=10),
            Position(symbol="GSG", quantity=7),
        ],
    )

    instructions = portfolio.allocate()

    expected = [
        Instruction(symbol="VOO", action="BUY", quantity=29, price=100.0, description="Adjust position from 1 to 30"),
        Instruction(symbol="VGLT", action="BUY", quantity=34, price=100.0, description="Adjust position from 6 to 40"),
        Instruction(symbol="VGIT", action="BUY", quantity=14, price=100.0, description="Adjust position from 1 to 15"),
        Instruction(symbol="GLD", action="SELL", quantity=3, price=100.0, description="Adjust position from 10 to 7"),
    ]

    assert instructions == expected
