"""Main function of CoW AMM orderbook"""

import logging
import time

from cowamms import OnchainFetcher, get_cow_amms, update_cow_amms
from liquidity import OffchainFetcher, get_liquidity, update_liquidity
from models import CoWAMM, Liquidity, CoWAMMOrderbook
from orders import update_orderbook, post_orders

logger = logging.getLogger(__name__)


def main():
    cow_amms, orderbook, liquidity, onchain_fetcher, offchain_fetcher = main_setup()
    while True:
        time.sleep(4)
        cow_amms, orders, liquidity = main_loop(
            cow_amms, orderbook, liquidity, onchain_fetcher, offchain_fetcher
        )


def main_setup() -> (
    tuple[list[CoWAMM], CoWAMMOrderbook, Liquidity, OnchainFetcher, OffchainFetcher]
):
    onchain_fetcher = OnchainFetcher()
    cow_amms = get_cow_amms(onchain_fetcher)
    offchain_fetcher = OffchainFetcher()
    liquidity = get_liquidity(cow_amms, offchain_fetcher)
    orderbook = CoWAMMOrderbook([])
    return cow_amms, orderbook, liquidity, onchain_fetcher, offchain_fetcher


def main_loop(
    cow_amms: list[CoWAMM],
    orderbook: CoWAMMOrderbook,
    liquidity: Liquidity,
    onchain_fetcher: OnchainFetcher,
    offchain_fetcher: OffchainFetcher,
) -> tuple[
    list[CoWAMM],
    CoWAMMOrderbook,
    Liquidity,
]:
    cow_amms = update_cow_amms(cow_amms, onchain_fetcher)
    liquidity = update_liquidity(liquidity, offchain_fetcher)
    orderbook = update_orderbook(cow_amms, orderbook, liquidity)
    return cow_amms, orderbook, liquidity


if __name__ == "__main__":
    main()
