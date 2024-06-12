# CoW AMM orderbook

The purpose of the software is to continuously add executable orders for CoW AMMs the the CoW Protocol orderbook. Those orders can then be picked up by other solvers who do not natively support CoW AMMs yet.

This is done by

- indexing the state of CoW AMMs,
- computing reasonable trades for CoW AMMs,
- creating order with suitable pre- and post-interactions, and
- submitting those orders to the orderbook.

These four parts of the code can also be used independently.

## Install

The easiest way to install the code is using `rye`:

```bash
git clone git@github.com:fhenneke/cow-amm-orderbook.git
cd cow-amm-orderbook
rye sync
```

This should automatically install python dependencies.
