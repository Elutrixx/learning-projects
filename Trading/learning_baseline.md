---
type: learning_baseline
topic: trading
learner: elu
updated: 2026-11-24
status: active
---

# Trading Learning Baseline

This document records what the learner has already encountered and should be able to explain. It is a checkpoint, not a claim of mastery.

## Project Boundaries

| Area | Current understanding |
|---|---|
| Purpose | Learn how trading works and test ideas; not job replacement or a get-rich-quick plan. |
| Money | Eventual live-training budget is EUR 100 of disposable fun money. |
| Current environment | TradingView Paper Trading on desktop with simulated money. |
| Risk boundary | Cash-sized positions only, leverage set to 1x, and no CFDs, options, futures, turbos, or crypto perpetuals. |
| Initial direction | Long-only training. Short-selling is understood conceptually but excluded for now. |

## Knowledge Checklist

| Topic | What the learner should already know | Status |
|---|---|---|
| Paper trading | Uses simulated money with market-price data. It teaches the interface and strategy testing without real financial loss. | Introduced and used |
| TradingView cost | A free Basic account is sufficient for the current exercises. Paid market data and subscriptions are not currently needed. | Introduced |
| Account setup | Paper account is EUR 100. All asset-class leverage settings are 1x. Margin control and simulated commissions are currently disabled. | Configured |
| Leverage | 1x means EUR 100 controls at most roughly EUR 100 of assets. Higher leverage amplifies gains, losses, and costs. | Explained |
| Timeframes | On a 15-minute chart, each candle summarizes one 15-minute period. Zoom changes how many candles are visible, not the candle duration. | Demonstrated |
| Candles | A candle contains open, high, low, and close. Its body shows open-to-close movement; its wicks show the period's extremes. | Introduced |
| Volume | Each volume bar aligns with a price candle and shows how much trading activity occurred during that period. High volume is activity, not automatically a buy signal. | Identified correctly |
| Market sessions | RTH means regular trading hours. Closed periods may be compressed or hidden. A price difference between one session's close and the next session's open is a gap. | Introduced |
| Indicative data | Free US-stock charts use real-time indicative Cboe data and may differ slightly from the primary NASDAQ feed. This is sufficient for training. | Introduced |
| Bid and ask | A market buy normally fills near the ask; a market sell normally fills near the bid. The difference is the bid-ask spread. | Demonstrated |
| Market order | Requests immediate execution at the best available price. Execution is likely, but the exact price is not guaranteed. | Used |
| Limit order | A buy limit executes only at the selected price or lower. It can remain unfilled. | Created and cancelled |
| Order vs position | A working order is an instruction waiting for execution. A position is an asset already bought or sold. | Demonstrated |
| Fractional position | A fraction of a share allows a small cash amount to track the percentage movement of a more expensive whole share. | Used |
| Equity | Account value including current unrealized profit or loss. | Introduced |
| Unrealized PnL | Profit or loss on an open position. It changes with the market and is not final. | Observed |
| Realized PnL | Profit or loss after a position is closed. | Observed |
| Display rounding | Per-share movement must be multiplied by quantity. A USD 0.003 loss can display as USD 0.00 when rounded to cents. | Calculated correctly |
| Bracket order | A position can have a take-profit and stop-loss attached. When one exit fills, the other is intended to cancel. | Created |
| Stop loss | Defines where the trade thesis is invalidated and limits intended loss. Real execution can be worse than the stop price during fast moves or gaps. | Introduced |
| Take profit | Defines an automatic profitable exit at a planned target. | Introduced |
| Long position | Profits when price rises and loses when price falls. | Demonstrated |
| Short position | Profits when price falls by selling borrowed stock and buying it back lower. It adds borrowing, margin, fee, and potentially unlimited-loss risks. | Concept only; excluded |
| Trend types | Price can form an uptrend, downtrend, or range. | Identified on chart |
| Market structure | Uptrends generally form higher highs and higher lows. Downtrends generally form lower highs and lower lows. | Introduced |
| Trend as evidence | A visible trend provides context but does not prove what the next candle will do. | Understood |
| No-trade decision | Waiting is a valid decision when a long-only setup conflicts with a downtrend or unclear range. | Introduced |
| Risk unit | 1R is the planned loss between entry and stop. A 2R target is twice that distance. | Introduced |
| Win rate | Win rate alone does not determine profitability. With +2R winners and -1R losers, theoretical break-even is about 33.3% before costs. | Explained |
| Expectancy | Strategy quality depends on average outcome after wins, losses, and costs, not merely how often it wins. | Introduced |

## Completed Exercises

| Exercise | Result | Lesson |
|---|---|---|
| First market round trip | Bought 0.06 NVDA at USD 151.08 and sold at USD 151.03. Gross result: about -USD 0.003, displayed as 0.00 after rounding. | Market execution, spread, fractional quantity, realized vs unrealized PnL, and rounding. |
| Pending limit order | Placed a buy limit for 0.07 NVDA at USD 150.49, observed `Working` status, then cancelled it. | A limit order controls price but may never fill. |
| Bracket-order exercise | Opened approximately EUR 10 of NVDA with a +2% take-profit and -1% stop-loss. | Attached exits and 2:1 reward/risk mechanics. Outcome not yet recorded in this document. |
| Chart classification | Identified a declining session, a gap up into a range, and a later gap down followed by short-term downward structure. | Trend, range, session gaps, and volume context. |

## Not Yet Covered

- Consistent identification and marking of swing highs and swing lows.
- Position sizing from a fixed EUR risk amount.
- Commission, spread, slippage, and currency-conversion modelling.
- Backtesting and forward-testing workflow.
- Trading journal maintenance and performance statistics.
- Pine Script strategy automation.
- Broker selection and live-account execution.
- Taxes beyond the fact that they must be considered before live trading.

## Current Next Step

1. Finish or close the bracket-order exercise and record its outcome.
2. Practice identifying confirmed swing highs and swing lows.
3. Apply the frozen Trend Continuation v0.1 rules.
4. Test historical examples before accumulating forward paper trades.

## Reference Material

- [TradingView paper trading](https://www.tradingview.com/support/solutions/43000516466-paper-trading-main-functionality/)
- [TradingView order ticket](https://www.tradingview.com/support/solutions/43000784804-what-is-an-order-ticket/)
- [TradingView leverage settings](https://www.tradingview.com/support/solutions/43000742700-how-to-trade-with-leverage-in-paper-trading/)
- [TradingView US indicative market data](https://www.tradingview.com/support/solutions/43000473924-is-us-stock-market-data-free-by-default/)
- [Investor.gov short-selling overview](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-51)

> Educational notes only. No strategy in this repository is assumed profitable or suitable for live trading.
