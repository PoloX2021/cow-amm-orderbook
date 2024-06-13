"""Indexing of CoW AMMs"""

import os
from typing import Any

from eth_typing import Address
from hexbytes import HexBytes
from dotenv import load_dotenv
from web3 import Web3
from web3.logs import DISCARD
from web3.types import EventData

from contracts.cowamm import cow_amm_abi, COW_AMM_FACTORY_ADDRESS
from models import CoWAMM

load_dotenv()
config: dict[str, dict[int, Any]] = {
    "node_urls": {
        1: os.getenv("NODE_URL_MAINNET"),
        100: os.getenv("NODE_URL_GNOSIS"),
    },
    "start_blocks": {
        1: 19000000,
        100: 34424133,
    },
}


class OnchainFetcher:
    def __init__(self, nodeurl: str) -> None:
        # get one Web3 object per chain
        self.nodes = {
            chain_id: Web3(Web3.HTTPProvider(node_url))
            for chain_id, node_url in config["node_urls"].items()
        }

        # set up contract for fetching CoW amm creation and
        self.cowamm_contracts = {
            chain_id: node.eth.contract(
                address=Address(HexBytes(COW_AMM_FACTORY_ADDRESS)), abi=cow_amm_abi
            )
            for chain_id, node in self.nodes.items()
        }

        self.last_checked_block: dict[int, int] = config["start_blocks"]

    def get_cow_amms(self) -> list[CoWAMM]:
        """Initialize CoW AMMs from onchain logs"""
        
        #1 update the latest block checked
        self.last_checked_block = {
            chain_id: node.eth.blockNumber
            for chain_id, node in self.nodes.items()
        }

        #2 get all the cow amms from the factory contract which show as internal transactions
            #it seems easier to call etherscan api to get all the cow_amms.
        return []

    def update_cow_amms(self, cow_amms: list[CoWAMM]) -> list[CoWAMM]:
        """Update CoW AMMs from onchain logs
        Already indexed CoW AMMs are updated and new CoW AMMs are added to the list."""

        #1 get new cow_amms : call get_cow_amms
        cow_amms = cow_amms + self.get_cow_amms()

        #2 get the balances for each cow_amms
        for cow_amm in cow_amms:
            token0_contract = self.nodes[cow_amm.chain_id].eth.contract(
                address=Address(HexBytes(cow_amm.token0)), abi=cow_amm_abi
            )
            cow_amm.reserve0 = token0_contract.functions.balanceOf(cow_amm.address).call()
            token1_contract = self.nodes[cow_amm.chain_id].eth.contract(
                address=Address(HexBytes(cow_amm.token1)), abi=cow_amm_abi
            )
            cow_amm.reserve1 = token1_contract.functions.balanceOf(cow_amm.address).call()
        
        return cow_amms


def get_cow_amms(onchain_fetcher: OnchainFetcher) -> list[CoWAMM]:
    return onchain_fetcher.get_cow_amms()


def update_cow_amms(
    cow_amms: list[CoWAMM], onchain_fetcher: OnchainFetcher
) -> list[CoWAMM]:
    return onchain_fetcher.update_cow_amms(cow_amms)


def parse_logs(logs) -> list[CoWAMM]:
    pass
