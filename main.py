"""All-weather portfolio allocation calculator"""

from all_weather.portfolio import Portfolio, Allocation

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

for instruction in instructions:
    print(instruction)
