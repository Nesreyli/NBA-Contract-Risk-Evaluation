import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

player = pd.read_csv("data/player_risk.csv")
team   = pd.read_csv("data/team_risk.csv")

player = player.replace([np.inf, -np.inf], np.nan)
player = player.dropna(subset=["ValuePerMillion"])
sns.set_theme(style="whitegrid")

# Player scatter - ValueScore vs ContractSurplus 
fig, ax = plt.subplots(figsize=(12, 7))
scatter = ax.scatter(
    player["ValueScore"],
    player["ContractSurplus"],
    c=player["ProbNegative"],
    cmap="RdYlGn_r",
    s=player["ProbNegative"] * 300 + 40,
    alpha=0.75,
    edgecolors="white",
    linewidths=0.5,
)
plt.colorbar(scatter, ax=ax, label="P(Negative Contract)")
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.set_xlabel("Value Score")
ax.set_ylabel("Contract Surplus ($)")
ax.set_title("Player Value vs Contract Surplus")
plt.tight_layout()
plt.savefig("Images/player_scatter.png", dpi=150)
plt.close()

# Contract Efficiency Bar Chart (top/bottom 20 only) 
n = 20
top = player.nlargest(n, "ContractSurplus")
bottom = player.nsmallest(n, "ContractSurplus")
player_sorted = pd.concat([bottom, top]).drop_duplicates().sort_values("ContractSurplus", ascending=True)

colors = ["#2ecc71" if v > 0 else "#e74c3c" for v in player_sorted["ContractSurplus"]]

fig, ax = plt.subplots(figsize=(10, len(player_sorted) * 0.4 + 2))
ax.barh(player_sorted["Player"], player_sorted["ContractSurplus"], color=colors)
ax.axvline(0, color="gray", linewidth=0.8)
ax.set_xlabel("Contract Surplus ($)")
ax.set_title(f"Top & Bottom {n} Players by Contract Surplus")
plt.tight_layout()
plt.savefig("Images/contract_efficiency.png", dpi=150)
plt.close()

# Surplus distribution with VaR95 & CVaR95 
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(player["ContractSurplus"], bins=40, color="#3498db", alpha=0.7, edgecolor="white")
ax.axvline(player["VaR95"].mean(),  color="#e74c3c", linestyle="--", linewidth=1.5, label=f"Avg VaR95:  ${player['VaR95'].mean():,.0f}")
ax.axvline(player["CVaR95"].mean(), color="#c0392b", linestyle=":",  linewidth=1.5, label=f"Avg CVaR95: ${player['CVaR95'].mean():,.0f}")
ax.axvline(0, color="gray", linewidth=0.8)
ax.set_xlabel("Contract Surplus ($)")
ax.set_ylabel("Player Count")
ax.set_title("Contract Surplus Distribution")
ax.legend()
plt.tight_layout()
plt.savefig("Images/surplus_distribution.png", dpi=150)
plt.close()

# Team heatmap 
heat_cols = ["AvgVaR95", "AvgCVaR95", "AvgProbNegative"]
heat_data = team.set_index("Team")[heat_cols]
heat_data_norm = (heat_data - heat_data.mean()) / heat_data.std()

fig, ax = plt.subplots(figsize=(8, len(team) * 0.45 + 2))
sns.heatmap(
    heat_data_norm,
    annot=heat_data.round(2),
    fmt="g",
    cmap="RdYlGn_r",
    linewidths=0.5,
    ax=ax,
    cbar_kws={"label": "Normalized Risk (z-score)"},
)
ax.set_title("Team Risk Heatmap")
ax.set_xlabel("")
plt.tight_layout()
plt.savefig("Visuals/team_heatmap.png", dpi=150)
plt.close()

# Team surplus bar chart (normalized by player count) 
team["AvgSurplusPerPlayer"] = team["TotalSurplus"] / team["PlayerCount"]
team_sorted = team.sort_values("AvgSurplusPerPlayer", ascending=True)
colors = ["#2ecc71" if v > 0 else "#e74c3c" for v in team_sorted["AvgSurplusPerPlayer"]]

fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(team_sorted["Team"], team_sorted["AvgSurplusPerPlayer"], color=colors)
ax.axvline(0, color="gray", linewidth=0.8)
ax.set_xlabel("Avg Contract Surplus per Player ($)")
ax.set_title("Team Contract Efficiency (Surplus per Player)")
plt.tight_layout()
plt.savefig("Images/team_surplus.png", dpi=150)
plt.close()

# Age vs ProbNegative Scatter 
# Merge Age from model_data since player_risk may not have it
model = pd.read_csv("data/model_data.csv")[["Player", "Age"]]
player_age = player.merge(model, on="Player", how="left")

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(
    player_age["Age"],
    player_age["ProbNegative"],
    c=player_age["ContractSurplus"],
    cmap="RdYlGn",
    alpha=0.65,
    s=60,
    edgecolors="white",
    linewidths=0.4,
)
plt.colorbar(scatter, ax=ax, label="Contract Surplus ($)")

# Trend line
z = np.polyfit(player_age["Age"].dropna(), player_age.loc[player_age["Age"].notna(), "ProbNegative"], 1)
p = np.poly1d(z)
x_line = np.linspace(player_age["Age"].min(), player_age["Age"].max(), 100)
ax.plot(x_line, p(x_line), color="#e74c3c", linewidth=1.5, linestyle="--", label="Trend")

ax.axvline(30, color="gray", linestyle=":", linewidth=1, label="Age 30")
ax.set_xlabel("Player Age")
ax.set_ylabel("P(Negative Contract)")
ax.set_title("Age vs Contract Risk Probability")
ax.legend()
plt.tight_layout()
plt.savefig("Images/age_vs_risk.png", dpi=150)
plt.close()

# VaR95 vs ContractSurplus scatter 
fig, ax = plt.subplots(figsize=(10, 6))

# Quadrant shading
xlim_pad = player["ContractSurplus"].abs().max() * 1.1
ylim_pad = player["VaR95"].abs().max() * 1.1

ax.axhline(0, color="gray", linewidth=0.8)
ax.axvline(0, color="gray", linewidth=0.8)

# Bad Surplus, Low Downside
ax.fill_between([-xlim_pad, 0], 0, ylim_pad,  alpha=0.04, color="#e74c3c")  
# Good Surplus, Low Downside
ax.fill_between([0, xlim_pad],  0, ylim_pad,  alpha=0.04, color="#2ecc71")   
# Bad Surplus, High Downside 
ax.fill_between([-xlim_pad, 0], -ylim_pad, 0, alpha=0.08, color="#e74c3c")   
# Good Surplus, High Downside (risky)
ax.fill_between([0, xlim_pad],  -ylim_pad, 0, alpha=0.04, color="#f39c12")  

scatter = ax.scatter(
    player["ContractSurplus"],
    player["VaR95"],
    c=player["ProbNegative"],
    cmap="RdYlGn_r",
    alpha=0.7,
    s=55,
    edgecolors="white",
    linewidths=0.4,
)
plt.colorbar(scatter, ax=ax, label="P(Negative Contract)")

# Quadrant labels
ax.text( xlim_pad * 0.6,  ylim_pad * 0.85, "Good & Stable",   fontsize=8, color="#27ae60", alpha=0.7)
ax.text(-xlim_pad * 0.95, ylim_pad * 0.85, "Bad & Stable",    fontsize=8, color="#c0392b", alpha=0.7)
ax.text( xlim_pad * 0.6, -ylim_pad * 0.95, "Good but Risky",  fontsize=8, color="#d35400", alpha=0.7)
ax.text(-xlim_pad * 0.95,-ylim_pad * 0.95, "Bad & Risky",     fontsize=8, color="#c0392b", alpha=0.7, fontweight="bold")

ax.set_xlim(-xlim_pad, xlim_pad)
ax.set_ylim(-ylim_pad, ylim_pad)
ax.set_xlabel("Contract Surplus ($)")
ax.set_ylabel("VaR95 ($)")
ax.set_title("Contract Surplus vs Downside Risk (VaR95)")
plt.tight_layout()
plt.savefig("Images/var95_vs_surplus.png", dpi=150)
plt.close()

print("All visuals saved to Images")