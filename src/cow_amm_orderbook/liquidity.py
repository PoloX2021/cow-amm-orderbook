import httpx

from models import CoWAMM, Liquidity


class OffchainFetcher:
    def __init__(self):
        pass

    def get_liquidity(self, cow_amms: dict[str, CoWAMM]) -> Liquidity:
        tokens: list[str] = []
        for cow_amm in cow_amms:
            tokens += [cow_amm.token0, cow_amm.token1]
        prices = self.get_prices(tokens)
        return Liquidity(prices)

    def update_liquidity(
        self, cow_amms: dict[str, CoWAMM], liquidity: Liquidity
    ) -> Liquidity:
        return self.get_liquidity(cow_amms)

    def get_price(self, address: str) -> float:
        url = (
            "https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses="
            + address
            + "&vs_currencies=usd"
        )
        response = httpx.get(url, timeout=5)  # do this async
        return float(response.json()[address]["usd"])

    def get_prices(self, addresses: list[str]) -> list[float]:
        prices = {address: self.get_price(address) for address in addresses}
        return prices


def get_liquidity(cow_amms: dict[str, CoWAMM], offchain_fetcher: OffchainFetcher):
    return offchain_fetcher.get_liquidity(cow_amms)


def update_liquidity(
    cow_amms: dict[str, CoWAMM], liquidity: Liquidity, offchain_fetcher: OffchainFetcher
):
    return offchain_fetcher.update_liquidity(cow_amms, liquidity)
