---
type: project_roadmap
topic: trading_automation
created: 2026-11-24
status: active
current_phase: foundations_and_first_strategy
---

# Trading Research and Automation Roadmap

## Intent

Learn trading mechanics, develop and test strategies, and eventually automate a strategy through a broker's official API if the evidence supports doing so.

The project is successful if it produces useful knowledge and sound testing habits. Finding no durable profitable strategy is an acceptable result. Bad ideas should lose simulated money before they are allowed near real money.

## Guiding Constraints

- Initial EUR 100 is a learning and strategy-research budget, not the final bot bankroll.
- Begin with paper trading and historical simulations.
- Use 1x leverage and long-only stock strategies initially.
- Do not use CFDs, options, futures, turbos, crypto perpetuals, or borrowed money during the beginner phase.
- Do not automate real orders using TradingView data, alerts, or webhooks.
- A future live bot must use a broker's officially supported API and appropriately licensed broker data.
- Trade only personal funds. Do not manage accounts, execute trades, or provide individualized signals for other people.
- Re-check broker terms, data licences, German law, and EU rules before live deployment.
- Treat costs, spread, slippage, FX conversion, taxes, and operational failures as part of the strategy.

## System Boundary

```text
Research and strategy discovery
TradingView + Pine Script
        |
        | Reimplement frozen, validated rules
        v
Live-capable automation
Broker market data -> Local strategy bot -> Risk controls -> Broker API
```

TradingView is the research environment. The broker API is the eventual execution environment. They remain separate.

## Phase 1: Foundations

### Work

- Learn candles, timeframes, volume, sessions, gaps, and basic market structure.
- Learn market, limit, stop-loss, and take-profit orders.
- Learn bid/ask spread, fractional positions, and realized/unrealized PnL.
- Learn risk units, reward/risk, expectancy, drawdown, and transaction costs.
- Practice reading charts without predicting individual candles.

### Exit Gate

- Explain the completed topics in `learning_baseline.md` without relying on button memorization.
- Place, inspect, modify, cancel, and close paper orders safely.
- Calculate the intended loss and target before entering a trade.

## Phase 2: Strategy Research

### Work

- Turn each idea into explicit, falsifiable rules.
- Give each strategy a versioned Markdown specification.
- Freeze the version before viewing its backtest result.
- Translate the frozen rules into Pine Script.
- Backtest on standard candles with realistic capital and costs.
- Inspect individual signals for coding errors and hindsight leakage.
- Record rejected strategies and why they failed.

### Current Candidate

- `trend_continuation_v0.1.md`
- Instrument: NVIDIA
- Interval: 15 minutes
- Direction: long only
- Planned reward/risk: 2:1
- Maximum planned account risk: 1% per trade

### Exit Gate

- Rules produce repeatable signals without subjective reinterpretation.
- Backtest contains enough trades to expose obvious failure modes.
- Average result remains positive after realistic costs in the tested data.
- Results are not dependent on one unusually profitable trade or brief market period.

Passing this gate means only that the strategy deserves further testing.

## Phase 3: Validation

### Work

- Test data not used while designing the strategy.
- Test different market conditions: rising, falling, ranging, calm, and volatile.
- Compare results across historical and forward paper trades.
- Keep strategy parameters frozen during each test batch.
- Record skipped signals and rule violations.
- Compare active results with a simple buy-and-hold benchmark where appropriate.

### Minimum Evidence to Review

- At least 30 valid trades as an initial filter.
- Expectancy in R after modelled costs.
- Maximum drawdown in R.
- Rule-adherence rate.
- Distribution of winners and losers.
- Historical versus forward-test differences.

Thirty trades are not proof. The sample expands if the strategy remains interesting.

### Exit Gate

- Forward results are directionally consistent with historical results.
- Drawdown and losing streaks are tolerable for the intended bankroll.
- The strategy survives reasonable parameter changes instead of requiring one magical setting.
- There is a clear explanation of when the strategy should not trade.

## Phase 4: Broker and API Selection

### Selection Criteria

- Available to German residents.
- Official API permits personal automated trading.
- Separate paper and live environments.
- Stable market-data access for the chosen instruments.
- Fractional shares if required.
- Required order types, including protective stops and bracket orders.
- Transparent commissions, spread, FX, data, and custody costs.
- Reliable account, position, order, and execution reporting.
- Sensible rate limits and authentication.
- German tax handling and usable annual documentation.

### Legal and Contract Check

- Confirm the bot trades only the owner's account and funds.
- Confirm API and market-data licences permit the planned use.
- Confirm no TradingView data is used for live algorithmic decisions.
- Re-check current German and EU requirements.
- Stop for professional advice if the scope expands to client money, public signals, direct exchange access, market making, or high-frequency trading.

### Exit Gate

- Broker, API, data source, fees, and legal boundary are documented.
- The chosen paper API supports every required order and account operation.

## Phase 5: Local Shadow Bot

### Behaviour

The bot reads broker data and records what it would do, but cannot transmit orders.

### Required Components

- Market-session and candle-close handling.
- Strategy signal engine matching the frozen rules.
- Position-sizing calculation.
- Stale or missing data detection.
- Duplicate-signal and duplicate-order prevention.
- Persistent state and restart recovery.
- Structured decision logs.
- Notifications for signals, errors, and state disagreements.

### Exit Gate

- Shadow decisions match expected manual decisions.
- Restarting the computer does not create duplicate or missing trades.
- The bot safely does nothing when data or state is uncertain.

## Phase 6: Automated Broker Paper Trading

### Work

- Enable order submission only in the broker's paper environment.
- Reconcile local state with broker positions and orders on every startup.
- Test entry, stop, target, session close, cancellation, and rejection paths.
- Test disconnects, stale prices, partial fills, rejected orders, and restarts.
- Compare API-paper results with the earlier backtest assumptions.

### Mandatory Safety Controls

- Maximum order value.
- Maximum position value.
- Maximum daily loss.
- Maximum number of entries per day.
- One-position limit unless a later strategy explicitly changes it.
- No new orders outside the approved session.
- Emergency kill switch.
- Default state of no action.

### Exit Gate

- Paper bot runs reliably for a meaningful period without manual rescue.
- Every order is explainable from logs.
- No duplicate, oversized, unprotected, or out-of-session positions occur.
- Actual paper executions remain acceptably close to modelled results.

## Phase 7: Capped Live Pilot

### Work

- Start on the local computer with a deliberately small bankroll and hard notional limits.
- Keep the same strategy version used in the final paper test.
- Monitor every order and reconcile daily.
- Compare live spread, slippage, fees, FX, and fills with paper assumptions.
- Increase size only after a separate review; never automatically compound during the pilot.

### Stop Conditions

- Broker state and bot state disagree.
- Protective orders are absent or rejected.
- Data becomes stale or unavailable.
- Daily loss limit is reached.
- Live behaviour differs materially from the validated model.
- Strategy drawdown exceeds its predefined tolerance.

### Exit Gate

- Live behaviour and costs are sufficiently close to validated expectations.
- Operational failures are rare, visible, and safely handled.
- The strategy remains positive after actual costs over a meaningful sample.

## Phase 8: Optional Cloud Deployment

Move the proven local bot to a small EU cloud server only when improved uptime is valuable.

Expected cost categories:

| Category | Rough planning range |
|---|---:|
| Local research and backtesting | EUR 0/month |
| Local automated paper bot | Approximately EUR 0-5/month plus electricity |
| Small cloud server | Approximately EUR 5-10/month |
| Basic broker market data | Approximately EUR 0-15/month |
| Simple live bot fixed costs | Approximately EUR 10-30/month |
| Trading costs | Variable by broker, instrument, size, and frequency |

Re-check prices before choosing infrastructure. Hosting is a fixed cost; spread, slippage, commissions, and FX scale with trading activity.

## Ongoing Strategy Lifecycle

```text
Idea
  -> explicit rules
  -> frozen version
  -> historical test
  -> untouched-data test
  -> forward paper test
  -> shadow bot
  -> automated paper bot
  -> capped live pilot
  -> continue, revise as a new version, or retire
```

Never rewrite an old strategy version to make its previous results look better. Every material rule change creates a new version and restarts the relevant validation gates.

## Immediate Next Actions

1. Finish the TradingView mechanics lessons.
2. Clarify and freeze any remaining ambiguities in Trend Continuation v0.1.
3. Build a Pine Script backtester for the frozen strategy.
4. Review its signals and results before discussing broker automation code.

> Educational project only. A positive backtest is not evidence of future returns, and automation makes bad rules fail faster as efficiently as it executes good ones.
