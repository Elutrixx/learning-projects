---
type: trading_strategy
name: trend_continuation
version: 0.1
created: 2026-11-24
status: frozen_for_initial_testing
instrument: NASDAQ:NVDA
timeframe: 15m
direction: long_only
account_size_eur: 100
max_risk_per_trade_pct: 1
reward_risk_target: 2
---

# Trend Continuation Strategy v0.1

## Intent

Test whether a simple long-only trend-continuation setup on NVIDIA's 15-minute chart has positive expectancy after costs.

This is a learning hypothesis, not a proven trading edge. Rules remain frozen for the initial test so losing examples cannot be explained away afterward.

## Approaches Considered

| Approach | Trade-off | Decision |
|---|---|---|
| Early reversal | Earlier entry and more potential upside, but more false reversals and subjective judgment. | Rejected for the first strategy. |
| Trend continuation | Later entry and some missed movement, but clearer structure and easier rule-following. | Selected. |

## Fixed Context

- **Instrument:** `NASDAQ:NVDA`
- **Chart interval:** 15-minute standard candles
- **Session:** Regular trading hours only
- **Direction:** Long only
- **Leverage:** 1x
- **Account:** EUR 100 paper account
- **Maximum open positions:** 1
- **Maximum entries:** 1 per trading day
- **Overnight holding:** Not allowed
- **Opening restriction:** No entries during the first two 15-minute candles of the regular session

## Definitions

### Swing High

A completed candle whose high is higher than the highs of the immediately preceding and following candles.

### Swing Low

A completed candle whose low is lower than the lows of the immediately preceding and following candles.

### Confirmed Uptrend

The two most recent confirmed swing highs are successively higher, and the two most recent confirmed swing lows are successively higher.

### Pullback

A decline inside a confirmed uptrend that remains above the preceding confirmed swing low.

### Higher Low Setup

The pullback forms a new confirmed swing low above the preceding confirmed swing low. The setup becomes invalid if price reaches or falls below the preceding swing low before entry.

## Entry Rule

Enter long at market only when all conditions are true:

1. The first two regular-session candles have completed.
2. A confirmed uptrend exists.
3. A pullback has formed a confirmed higher low.
4. After that higher low, a complete 15-minute candle closes above the immediately preceding candle's high.
5. No position has already been opened that trading day.

The market order is submitted after the triggering candle closes. The actual fill price becomes the entry price.

## Exit Rules

### Stop Loss

- Initial stop: USD 0.05 below the pullback's confirmed swing low.
- The stop may never be moved farther from the entry.
- Moving the stop closer is not part of v0.1; leave it unchanged for the initial test.

### Take Profit

- Let `risk_per_share = entry_price - stop_price`.
- Set `take_profit = entry_price + (2 * risk_per_share)`.
- This creates a planned reward/risk ratio of 2:1.

### Time Exit

If neither stop nor target executes, close the full position at market before regular trading ends. Do not hold overnight.

## Position Sizing

- Maximum planned account risk is 1%, equal to EUR 1 on the initial paper account.
- TradingView quantity should be based on the entry-to-stop distance using `Risk, % balance = 1%` when available.
- Leverage remains 1x, so position value cannot exceed available cash.
- If the cash cap prevents risking the full EUR 1, accept the smaller actual risk. Never increase leverage to reach the risk target.

Conceptual calculation:

```text
maximum_risk_eur = account_equity_eur * 0.01
quantity = maximum_risk_in_instrument_currency / (entry_price - stop_price)
quantity = min(quantity, maximum_cash_position_quantity)
```

## Trade Management Rules

- Do not add to a losing position.
- Do not open another position after the day's trade closes.
- Do not move the stop farther away.
- Do not remove the stop or target after entry.
- Do not count UI-training trades or accidental orders as strategy trades.
- Do not change these rules during the initial sample.

## Initial Test Plan

- Collect 30 valid strategy trades.
- A strategy trade counts even if it loses.
- Reject and separately record any trade that violated a rule.
- Historical and forward paper trades must be labelled separately.
- The current random bracket-order exercise is excluded from the sample.

### Metrics

- Net PnL after modelled costs
- Result in R for every trade
- Win rate
- Average R per trade (expectancy)
- Maximum drawdown in R
- Rule-adherence rate
- Number of valid setups skipped
- Historical versus forward-test results

The theoretical break-even win rate for +2R winners and -1R losers is 33.3% before costs. A positive initial result means only that the strategy deserves more testing.

## Trade Journal Template

```markdown
### Trade YYYY-MM-DD

- Test type: historical | forward paper
- Uptrend confirmed: yes | no
- First 30 minutes complete: yes | no
- Previous swing high:
- Latest swing high:
- Previous swing low:
- Higher-low setup:
- Trigger candle close:
- Entry price:
- Stop price:
- Target price:
- Quantity:
- Planned risk EUR:
- Result EUR:
- Result R:
- Exit reason: stop | target | session close | manual/error
- Rules followed: yes | no
- Screenshot before entry:
- Screenshot after exit:
- Notes:
```

## Known Limitations

- Swing identification reacts after a following candle completes and therefore enters late by design.
- Backtests approximate fills and can understate spread, slippage, and gaps.
- NVIDIA alone is not evidence that the rules generalize to other stocks or market conditions.
- Thirty trades are a preliminary filter, not statistical proof.
- Exact commission, spread, slippage, and EUR/USD conversion assumptions remain to be added before judging net profitability.

## Versioning Rule

Do not edit v0.1 after testing begins. Proposed changes become a new file and version, with the reason for each change recorded.

> Educational experiment only. Do not treat this document as individualized investment advice or evidence of future returns.
