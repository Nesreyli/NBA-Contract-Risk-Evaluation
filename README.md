# NBA Contract Risk Evaluation

A data-driven system for evaluating NBA player contract risk using statistical modelling, market salary prediction, and Monte Carlo simulation. Built to help quantify whether a player's current contract represents fair value and how much financial risk that contract carries over its remaining term.

---

## Why This Exists

NBA front offices operate in an increasingly complex financial environment. <br>
For the **2025–26 season**, the salary cap sits at **$154.6M**, with the luxury tax threshold at **$187.9M**. The cap is projected to rise to approximately **$165M in 2026–27**, with continued growth expected through the end of the decade as the league's national media deal matures. Under the current CBA, annual cap increases are capped at 10% meaning long-term contracts signed today are being priced against a moving target.

In that environment, overpaying for a declining player isn't just a roster problem it's a compounding financial liability. A $50M/year player delivering $28M of on-court value doesn't just waste money today; it constrains flexibility for 3–5 years. This project attempts to put a number on that risk.

---

## What It Does

The system ingests current NBA player salary and performance data, builds a market salary model based on statistical production, and runs a Monte Carlo simulation to quantify contract risk at both the player and team level.

**Key outputs per player:**
- `ContractSurplus` — difference between predicted market value and actual contract salary
- `VaR95` — the worst-case surplus outcome at the 5th percentile (Value at Risk)
- `CVaR95` — average outcome in the worst 5% of scenarios (Conditional VaR)
- `ProbNegative` — probability the contract is a net negative for the team
- `ValueScore` — composite on-court production score
- `ValuePerMillion` — efficiency of contract relative to salary

**Key outputs per team:**
- Portfolio-level risk aggregates across all rostered players
- Normalized risk heatmap for cross-team comparison

---

## Project Structure

```
NBA-Contract-Risk-Evaluation/
├── main.py                      # Runs the Entire Model
├── README.md
├── requirements.txt 
│
├── data/
│   ├── salaries.csv              # Basketball Reference Data 
│   ├── Stats_NBA.csv             # Pulled Data from API
│   ├── processed_data.csv        # Cleaned & merged output
│   ├── model_data.csv            # Feature-engineered output
│   ├── player_risk.csv           # Monte Carlo results per player
│   └── team_risk.csv             # Aggregated team-level risk
│
├── Data Collection
│   ├── load_salaries.py         # Provide Clean Salary Tables
│   ├── pull_nba_stats.py        # Pull Stats from API 
│   ├── merge_data.py            # Merge Tables into One
│   ├── processing_data.py       # Adjusting Total into Per Game
│
├── Model Building
│   ├── Contract_Surplus.py      # Surplus of 2025-26 Contract
│   ├── Cost_Features.py         # Effiency of Contracts 
│   ├── Market_Value.py          # Fits Model for All Contracts
│   ├── Value_Score.py           # Provides a Total for All Stats
│   ├── Pipeline.py              # Creates a model for testing
│
├── Simulation 
│   ├── Monte Carlo.py           # Engine Simulation
│   ├── Risk_Aggregator.py       # Team level Risk Aggregation
│   ├── Pipeline_2.py            # Slots all Data into One Table
│ 
├── Visualization
│   └── Model_Evaluation         # Chart Outputs of Data 
```

---

## Setup

```bash
pip install pandas numpy matplotlib seaborn nba_api
```

Place your `salaries.csv` file in the `data` folder before running. The file should contain player names, teams, and yearly contract values (2025–26 through 2030–31).

---

## Usage

Run the full pipeline end to end:

```bash
python main.py
```

This will:
1. Pull live player stats from the NBA API
2. Merge with salary data and engineer features
3. Fit a market salary model and calculate contract surplus
4. Run 10,000 Monte Carlo simulations per player
5. Aggregate risk to the team level
6. Generate all visualisations to `Visuals`

---

## Methodology

### Market Salary Model
A regression model is fit on player performance features (points, rebounds, assists, efficiency, minutes) to estimate what each player's production would command on the open market. The difference between this predicted value and their actual contract salary is the **Contract Surplus** positive means the player is a bargain, negative means overpaid.

### Monte Carlo Simulation
For each player, 10,000 salary scenarios are drawn from a normal distribution centred on their Contract Surplus. The uncertainty (standard deviation) is scaled by **age** and **games played**, reflecting that older and less durable players carry more unpredictable outcomes. This produces a full distribution of possible contract outcomes per player rather than a single point estimate.

### Risk Metrics
- **VaR95** — the surplus value at the 5th percentile; the threshold below which outcomes are considered tail risk
- **CVaR95** — the average of all outcomes below VaR95; a more conservative measure of downside exposure
- **ProbNegative** — share of simulated scenarios where the contract is a net loss for the team

### Context: The Cap Growth Factor
Because the salary cap is projected to grow ~7% annually through the late 2020s, a contract that looks expensive today may age differently depending on how quickly a player declines relative to cap inflation. This model evaluates contracts against today's market — future cap growth is not modelled explicitly, but the `YearsRemaining` feature captures duration risk.

---

## Visualisations

| Chart | Description |
|---|---|
| `player_scatter.png` | ValueScore vs ContractSurplus, coloured and sized by risk probability |
| `contract_efficiency.png` | Top & bottom 20 players by contract surplus |
| `surplus_distribution.png` | League-wide surplus histogram with VaR95 / CVaR95 markers |
| `team_heatmap.png` | Normalised team risk across VaR, CVaR, and ProbNegative |
| `team_surplus.png` | Average surplus per player by team |
| `age_vs_risk.png` | Age vs probability of negative contract with trend line |
| `var95_vs_surplus.png` | Quadrant chart separating bad/good and stable/risky contracts |

---

## Limitations

- Performance data reflects the most recent NBA season only; multi-year trends are not incorporated
- Injury history is captured indirectly via games played, not explicitly modelled
- The market salary model assumes a linear relationship between production and salary real contracts involve positional scarcity, team fit, and negotiation dynamics that are not captured
- Cap growth is not projected forward; contracts are evaluated against current market conditions

---