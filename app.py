import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Add root to path so imports work whether files are flat or in subfolders
sys.path.insert(0, os.path.dirname(__file__))

from data_aggregator import FinancialDataAggregator
from risk_model import RiskScoringModel
from risk_agent import RiskMonitorAgent
from visualizations import plot_risk_distribution, plot_risk_by_platform, plot_risk_factors

st.set_page_config(page_title="Risk Monitor", page_icon="📊", layout="wide")

st.title("📊 Cross-Platform Risk Monitor")
st.markdown("""
    **Risk assessment across Traditional Finance (TradFi), DeFi, and FinTech**
    *Integration: Project 2 (Stats) | Project 3 (ML) | Project 6 (Agent)*
""")

if 'results_df' not in st.session_state:
    st.session_state.results_df = None

@st.cache_resource
def init_system():
    aggregator = FinancialDataAggregator()
    model = RiskScoringModel()
    model.train()
    agent = RiskMonitorAgent(aggregator, model)
    return aggregator, model, agent

with st.spinner("Initializing..."):
    aggregator, model, agent = init_system()

with st.sidebar:
    st.header("Configuration")
    all_assets = ["Apple", "Microsoft", "JP Morgan", "Aave", "Uniswap", "Lido", "PayPal", "Block", "Stripe"]
    selected_assets = st.multiselect("Select assets", all_assets, default=["Apple", "Aave", "PayPal"])
    risk_threshold = st.slider("Alert Threshold", 0, 100, 70)
    run_button = st.button("Run Risk Assessment", type="primary")

col1, col2, col3 = st.columns(3)

if run_button and selected_assets:
    with st.spinner("Agent analyzing assets..."):
        results_df = agent.run(selected_assets[:5])
        st.session_state.results_df = results_df
    
    with col1:
        st.metric("Assets Analyzed", len(results_df))
    with col2:
        high_risk = len(results_df[results_df['Risk Score'] >= risk_threshold])
        st.metric("High Risk Assets", high_risk)
    with col3:
        st.metric("Avg Risk Score", f"{results_df['Risk Score'].mean():.0f}%")

if st.session_state.results_df is not None:
    df = st.session_state.results_df
    
    st.subheader("Risk Assessment Results")
    
    def color_risk(val):
        if val >= risk_threshold:
            return 'background-color: #ffcccc'
        elif val >= 50:
            return 'background-color: #ffffcc'
        return 'background-color: #ccffcc'
    
    styled_df = df.style.applymap(color_risk, subset=['Risk Score'])
    st.dataframe(styled_df, use_container_width=True)
    
    tab1, tab2, tab3 = st.tabs(["Risk Distribution", "Platform Comparison", "Risk Factors"])
    
    with tab1:
        fig = plot_risk_distribution(df)
        st.pyplot(fig)
    
    with tab2:
        fig = plot_risk_by_platform(df)
        st.pyplot(fig)
        st.dataframe(aggregator.compare_platforms())
    
    with tab3:
        fig = plot_risk_factors(df)
        st.pyplot(fig)
    
    high_risk_alerts = df[df['Risk Score'] >= risk_threshold]
    if len(high_risk_alerts) > 0:
        st.subheader("Alerts")
        for _, row in high_risk_alerts.iterrows():
            st.error(f"**{row['Asset']}** ({row['Platform']}) - Risk: {row['Risk Score']:.0f}%")
    
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, f"risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
else:
    st.info("Select assets and click 'Run Risk Assessment'")

st.caption("Built with: Project 2 | Project 3 | Project 6 | Scalable modular architecture")
