from types import Any

import httpx

from models import CoWAMM, Liquidity, Order, CoWAMMOrderbook


def update_orderbook(
    cow_amms: list[CoWAMM], orderbook: CoWAMMOrderbook, liquidity: Liquidity
) -> CoWAMMOrderbook:
    new_orders = [liquidity.propose_order(cow_amm) for cow_amm in cow_amms]

    orders = orderbook.orders + new_orders
    post = [False for order in orderbook.orders] + [True for order in new_orders]
    cancel = [True for order in orderbook.orders] + [False for order in new_orders]

    post_and_cancel_orders(orders, post, cancel)

    orderbook = CoWAMMOrderbook(orders=new_orders)
    return orderbook


def post_and_cancel_orders(orders: CoWAMMOrderbook) -> None:
    pass


def post_order(order: Order) -> None:
    """Post order to CoW orderbook"""
    encoded_order = encode_order(order)
    url = ""
    httpx.post(url, data=encoded_order)  # post to orderbook


def cancel_order(order: Order) -> None:
    """Post order to CoW orderbook"""
    encoded_order = encode_order(order)
    url = ""
    httpx.post(url, data=encoded_order)  # cancel on orderbook


def encode_order(order: Order) -> dict[str, Any]:
    """Encode order including pre- and post-interactions"""
    pass
