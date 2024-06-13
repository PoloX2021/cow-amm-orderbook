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
        slippage = 0.005
        price0 = self.prices[cow_amm.token0]
        price1 = self.prices[cow_amm.token1]
        p = price1 / price0
        order = Order()
        #Goal : (X+x)/(Y-y) = p = x/y -> x = (p*Y-X)/2 & y = (Y-p*X)/2
        #if x>0: buy x token0, sell y token1
        #if x<0: sell x token0, buy y token1
        if p*cow_amm.reserve1>cow_amm.reserve0:
            p = (1-slippage)*p
            order.buy_token = cow_amm.token0
            order.limit_buy_amount = (p*cow_amm.reserve1-cow_amm.reserve0)/2
            order.sell_token = cow_amm.token1
            order.limit_sell_amount = (cow_amm.reserve1-p*cow_amm.reserve0)/2
            order.cow_amm = cow_amm.address

        
        p = (1+slippage)*p
        order.sell_token = cow_amm.token0
        order.limit_sell_amount = -(p*cow_amm.reserve1-cow_amm.reserve0)/2
        order.buy_token = cow_amm.token1
        order.limit_buy_amount = -(cow_amm.reserve1-p*cow_amm.reserve0)/2
        order.cow_amm = cow_amm.address

        return Order()
