import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_risk_distribution(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['Risk Score'], bins=20, edgecolor='black', alpha=0.7, color='steelblue')
    ax.set_title('Distribution of Risk Scores', fontsize=14, fontweight='bold')
    ax.set_xlabel('Risk Score (0-100)')
    ax.set_ylabel('Number of Assets')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=70, color='red', linestyle='--', alpha=0.7, label='Alert Threshold')
    ax.legend()
    return fig

def plot_risk_by_platform(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {'TradFi': '#2ecc71', 'DeFi': '#e74c3c', 'FinTech': '#f39c12'}
    platforms = df['Platform'].unique()
    for i, platform in enumerate(platforms):
        data = df[df['Platform'] == platform]['Risk Score']
        bp = ax.boxplot(data, positions=[i], widths=0.6, patch_artist=True)
        bp['boxes'][0].set_facecolor(colors.get(platform, '#95a5a6'))
    ax.set_xticks(range(len(platforms)))
    ax.set_xticklabels(platforms)
    ax.set_title('Risk Scores by Platform', fontsize=14, fontweight='bold')
    ax.set_ylabel('Risk Score (0-100)')
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, axis='y')
    return fig

def plot_risk_factors(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {'Low Risk': '#2ecc71', 'Medium Risk': '#f1c40f', 'High Risk': '#e67e22', 'Critical Risk': '#e74c3c'}
    for category, color in colors.items():
        mask = df['Risk Category'] == category
        if mask.any():
            ax.scatter(df.loc[mask, 'Volatility'], df.loc[mask, 'Liquidity'], c=color, label=category, s=100, alpha=0.7)
    ax.set_xlabel('Volatility')
    ax.set_ylabel('Liquidity')
    ax.set_title('Risk Factors: Volatility vs Liquidity', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig
