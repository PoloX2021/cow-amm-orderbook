"""Models for CoW AMMs"""

from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class CoWAMM:
    chain_id: int
    address: str
    token0: str
    token1: str
    reserve0: int
    reserve1: int


@dataclass
class Order:
    sell_token: str
    buy_token: str
    limit_sell_amount: str
    limit_buy_amount: str
    cow_amm: str


@dataclass
class CoWAMMOrderbook:
    orders: list[Order]
    # post: list[bool]
    # cancel: list[bool]


@dataclass
class Liquidity:
    prices: dict[str, float]

    def propose_order(self, cow_amm: CoWAMM) -> Order:
        price0 = self.prices[cow_amm.token0]
        price1 = self.prices[cow_amm.token1]
        p = price0 / price1

        return Order()
