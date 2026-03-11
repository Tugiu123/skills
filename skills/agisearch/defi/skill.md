---
name: DeFi
description: The complete operating manual for decentralized finance. Navigate yield farming, liquidity provision, lending protocols, DEX trading, bridges, staking, and governance across every major chain. Evaluate protocols before depositing a single dollar. Calculate real yields after gas, impermanent loss, and token inflation. Detect rug pulls before they happen. Manage positions across multiple chains from one conversation. Built for people who believe in financial sovereignty but refuse to achieve it by losing money to protocols they do not understand.
---

# DeFi

## What Banks Do Not Want You to Understand

For four hundred years, finance has operated on a single architectural principle: trusted intermediaries. You do not lend money directly to the person who wants to borrow it. You deposit your money in a bank, the bank lends it to the borrower, and both of you trust the bank to handle the transaction honestly. The bank takes a margin for this service. A large margin. And in exchange for that margin, you get convenience, insurance, and the comfort of not having to evaluate the creditworthiness of every borrower yourself.

Decentralized finance replaces the bank with math.

A smart contract on a blockchain can do everything the bank does — hold deposits, issue loans, calculate interest, liquidate collateral, distribute returns — without any human making decisions, taking margins, or having the ability to freeze your account because someone in a compliance department decided your transaction looked unusual.

This is either the most important innovation in financial history or the most elaborate mechanism for losing money ever invented. Which one it is for you depends entirely on whether you understand what you are interacting with before you interact with it.

DeFi skill exists to make sure you do.

---

## The Landscape: What Actually Exists

### Decentralized Exchanges

On a traditional exchange, you place an order and a matching engine finds someone willing to take the other side. On a decentralized exchange, there is no matching engine. Instead, there are liquidity pools — reservoirs of paired tokens deposited by other users — and a mathematical formula that determines the price based on the ratio of tokens in the pool.

Uniswap, SushiSwap, Curve, Balancer, Aerodrome, Trader Joe, Raydium — each implements this concept differently. Some optimize for stablecoin swaps with minimal slippage. Some use concentrated liquidity that lets providers target specific price ranges. Some aggregate across multiple pools to find the best execution path.

The skill navigates all of them. When you want to swap one token for another, it identifies the optimal route — which might involve splitting the trade across multiple pools on multiple DEXs to minimize slippage and gas costs. It shows you the expected output, the price impact of your trade size, the gas cost, and the net result compared to a centralized exchange.

When the trade does not make sense — when the slippage would eat your profit, when the gas cost exceeds the value of the transaction, when the token you are trying to buy has liquidity so thin that any significant purchase would move the price against you — the skill tells you before you execute.

### Lending and Borrowing

Aave, Compound, Morpho, Euler, Spark — protocols that create two-sided markets between lenders who want yield and borrowers who need capital.

You deposit ETH. Someone borrows against your deposit and pays interest. You earn that interest minus whatever the protocol takes. The borrower provides collateral worth more than they borrow. If their collateral value drops below a threshold, it is automatically liquidated to repay the loan. No credit checks. No applications. No waiting. Math.

The skill evaluates lending opportunities with precision that goes beyond the advertised APY. What is the real yield after accounting for token rewards that might decline in value, protocol fees, and the opportunity cost of locking your capital? What is the utilization rate of the pool, and what happens to your withdrawal ability if utilization spikes to 100 percent?

### Yield Farming

Yield farming is the practice of depositing tokens into protocols that reward depositors with additional tokens. The rewards are denominated in the protocol own token, which means the real yield depends on the future price of a token that the market has not yet decided how to value.

A farm advertising 200 percent APY is not offering you a guaranteed 200 percent return. It is offering you a specific number of tokens per day. If those tokens drop 90 percent in value — which happens routinely — your 200 percent APY becomes a 20 percent APY on a depreciating asset while your principal may have suffered impermanent loss.

The skill calculates real yield. Not the number displayed on the protocol dashboard. The actual return after token price depreciation based on emission schedules, after impermanent loss based on historical correlation between paired assets, after gas costs for entering, claiming, compounding, and exiting, and after the opportunity cost of simply holding the underlying assets.

### Liquidity Provision

Providing liquidity to a DEX pool means depositing equal values of two tokens so that other traders can swap between them. In return, you earn a share of the trading fees.

Impermanent loss is the phenomenon where providing liquidity can leave you worse off than simply holding the two tokens separately. If Token A goes up 100 percent while Token B stays flat, the pool automatically rebalances by selling your appreciating Token A and buying more of the flat Token B. When you withdraw, you have less Token A than if you had just held it.

The skill models impermanent loss for any token pair based on your entry prices, current prices, and the fee tier. It shows you the exact break-even point — how much fee income you need to earn for the position to be profitable.

### Bridges and Cross-Chain

Bridges move assets between chains. They are also where the largest DeFi exploits in history have occurred. Hundreds of millions of dollars lost because bridge smart contracts had vulnerabilities.

The skill routes cross-chain transfers through the safest path available, considering bridge security history, current liquidity depth, transfer time, and total cost.

### Staking

Proof-of-stake blockchains pay validators for securing the network. Liquid staking protocols like Lido, Rocket Pool, Jito, or Marinade let you stake without running infrastructure and give you a receipt token that can itself be used in DeFi.

This composability is powerful and also introduces layered risk. The skill maps every layer when you are building stacked positions and shows you what happens at each layer during a market drawdown.

---

## Protocol Evaluation: The Survival Framework

Before you deposit a single dollar, the skill runs a comprehensive evaluation.

Smart contract risk — audits, open source status, total value locked, time in production. Battle-tested code with billions locked for years is fundamentally different from freshly deployed code with a single audit.

Economic design risk — is yield from real activity or token emissions? Sustainable yield comes from trading fees and borrowing interest. Unsustainable yield comes from printing tokens and hoping enough new depositors arrive to maintain the price.

Governance risk — who can change parameters? Is there a multisig that could drain funds? Are there timelocks on governance actions?

Oracle risk — price feed source and manipulation history. Oracle failures have caused some of the largest losses in DeFi history.

Liquidity risk — can you exit when you want to? What happens during a bank run on the protocol?

The skill produces a detailed risk map so you can decide which risks you accept.

---

## Tax and Accounting

Every DeFi interaction is a taxable event in most jurisdictions. Every swap, every liquidity provision entry and exit, every yield claim, every bridge transfer. The transaction history is spread across multiple chains, multiple protocols, and multiple wallets.

The skill tracks every position, transaction, and yield accrual across all chains. It calculates cost basis, identifies taxable events, and produces a summary your accountant can work with.

---

## Who This Is For

DeFi beginners who want to understand before they participate. Active users managing positions across multiple chains who want real yield calculations instead of dashboard vanity numbers. Institutional participants who need risk analysis documentation. Anyone who has lost money in DeFi because they did not see the risk clearly enough and refuses to let it happen again.

---

## The Honest Truth

DeFi is real. The ability to lend, borrow, trade, and earn yield without intermediaries is a genuine innovation with profound implications for financial access and sovereignty.

DeFi is also dangerous. Hundreds of billions have been lost to exploits, rug pulls, economic design failures, and simple user error in transactions that cannot be reversed.

The skill exists between these two truths. It helps you access the opportunity while seeing the risk clearly enough to avoid becoming a cautionary tale.

Your money. Your sovereignty. Your responsibility. Your clarity.
