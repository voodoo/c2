import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io
import os

# Page configuration
st.set_page_config(
    page_title="FAANG Financial Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
    }
    /* Make metric labels more prominent */
    .stMetric label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #1f1f1f !important;
    }
    /* Make metric values stand out significantly more */
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #0e4c92 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    /* Style metric delta (if present) */
    .stMetric [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/financial_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.quarter
    return df

# Company color mapping
COMPANY_COLORS = {
    'Meta': '#1877F2',
    'Apple': '#555555',
    'Amazon': '#FF9900',
    'Netflix': '#E50914',
    'Alphabet': '#4285F4'
}

# Main app
def main():
    # Title
    st.markdown('<h1 class="main-header">📊 FAANG Financial Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🎛️ Filters")
    
    # Company selection
    companies = st.sidebar.multiselect(
        "Select Companies",
        options=df['Company'].unique(),
        default=df['Company'].unique()
    )
    
    # Date range selection
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Metric selection
    metric_option = st.sidebar.selectbox(
        "Select Financial Metric",
        options=['Revenue', 'NetIncome', 'OperatingExpenses', 'MarketCap', 'StockPrice', 'PERatio'],
        format_func=lambda x: {
            'Revenue': 'Revenue (Millions)',
            'NetIncome': 'Net Income (Millions)',
            'OperatingExpenses': 'Operating Expenses (Millions)',
            'MarketCap': 'Market Cap (Millions)',
            'StockPrice': 'Stock Price ($)',
            'PERatio': 'P/E Ratio'
        }[x]
    )
    
    # Filter data
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = df[
            (df['Company'].isin(companies)) &
            (df['Date'].dt.date >= start_date) &
            (df['Date'].dt.date <= end_date)
        ]
    else:
        filtered_df = df[df['Company'].isin(companies)]
    
    # Sidebar company info
    st.sidebar.markdown("---")
    st.sidebar.header("ℹ️ About FAANG")
    st.sidebar.markdown("""
    **FAANG** represents five major tech companies:
    - **Meta** (Facebook)
    - **Apple**
    - **Amazon**
    - **Netflix**
    - **Alphabet** (Google)
    
    These companies dominate the tech industry and have significant market influence.
    """)
    
    # Main dashboard
    if filtered_df.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selections.")
        return
    
    # Key Metrics Row
    st.header("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        latest_revenue = filtered_df.groupby('Company')['Revenue'].last().sum()
        st.metric(
            label="Total Revenue",
            value=f"${latest_revenue:,.0f}M"
        )
    
    with col2:
        latest_income = filtered_df.groupby('Company')['NetIncome'].last().sum()
        st.metric(
            label="Total Net Income",
            value=f"${latest_income:,.0f}M"
        )
    
    with col3:
        latest_marketcap = filtered_df.groupby('Company')['MarketCap'].last().sum()
        st.metric(
            label="Combined Market Cap",
            value=f"${latest_marketcap:,.0f}M"
        )
    
    with col4:
        avg_pe = filtered_df.groupby('Company')['PERatio'].last().mean()
        st.metric(
            label="Average P/E Ratio",
            value=f"{avg_pe:.1f}"
        )
    
    st.markdown("---")
    
    # Row 1: Revenue Comparison and Stock Price Trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Revenue Comparison")
        latest_data = filtered_df.groupby('Company').tail(1)
        fig_revenue = px.bar(
            latest_data,
            x='Company',
            y='Revenue',
            color='Company',
            color_discrete_map=COMPANY_COLORS,
            title='Latest Quarterly Revenue by Company'
        )
        fig_revenue.update_layout(showlegend=False, height=400)
        fig_revenue.update_yaxes(title_text="Revenue (Millions $)")
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        st.subheader("📊 Stock Price Trends")
        fig_stock = px.line(
            filtered_df,
            x='Date',
            y='StockPrice',
            color='Company',
            color_discrete_map=COMPANY_COLORS,
            title='Historical Stock Prices'
        )
        fig_stock.update_layout(height=400)
        fig_stock.update_yaxes(title_text="Stock Price ($)")
        st.plotly_chart(fig_stock, use_container_width=True)
    
    # Row 2: Profitability and Market Cap Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💵 Net Income Trends")
        fig_income = px.line(
            filtered_df,
            x='Date',
            y='NetIncome',
            color='Company',
            color_discrete_map=COMPANY_COLORS,
            title='Net Income Over Time'
        )
        fig_income.update_layout(height=400)
        fig_income.update_yaxes(title_text="Net Income (Millions $)")
        st.plotly_chart(fig_income, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Market Cap Distribution")
        latest_marketcap_data = filtered_df.groupby('Company')['MarketCap'].last().reset_index()
        fig_pie = px.pie(
            latest_marketcap_data,
            values='MarketCap',
            names='Company',
            color='Company',
            color_discrete_map=COMPANY_COLORS,
            title='Current Market Cap Distribution'
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Row 3: Custom Metric Analysis and Growth
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📉 {metric_option} Analysis")
        fig_metric = px.line(
            filtered_df,
            x='Date',
            y=metric_option,
            color='Company',
            color_discrete_map=COMPANY_COLORS,
            title=f'{metric_option} Over Time'
        )
        fig_metric.update_layout(height=400)
        st.plotly_chart(fig_metric, use_container_width=True)
    
    with col2:
        st.subheader("📈 Year-over-Year Growth")
        
        # Calculate YoY growth for revenue
        growth_data = []
        for company in companies:
            company_data = filtered_df[filtered_df['Company'] == company].copy()
            company_data = company_data.sort_values('Date')
            
            for year in company_data['Year'].unique()[1:]:
                current_year = company_data[company_data['Year'] == year]['Revenue'].sum()
                previous_year = company_data[company_data['Year'] == year-1]['Revenue'].sum()
                
                if previous_year > 0:
                    growth = ((current_year - previous_year) / previous_year) * 100
                    growth_data.append({
                        'Company': company,
                        'Year': year,
                        'Growth': growth
                    })
        
        if growth_data:
            growth_df = pd.DataFrame(growth_data)
            fig_growth = px.bar(
                growth_df,
                x='Year',
                y='Growth',
                color='Company',
                color_discrete_map=COMPANY_COLORS,
                title='Revenue YoY Growth Rate (%)',
                barmode='group'
            )
            fig_growth.update_layout(height=400)
            fig_growth.update_yaxes(title_text="Growth Rate (%)")
            st.plotly_chart(fig_growth, use_container_width=True)
        else:
            st.info("Not enough data to calculate year-over-year growth.")
    
    # Detailed Data Table
    st.markdown("---")
    st.header("📋 Detailed Financial Data")
    
    # Format the dataframe for display
    display_df = filtered_df.copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:,.0f}M")
    display_df['NetIncome'] = display_df['NetIncome'].apply(lambda x: f"${x:,.0f}M")
    display_df['OperatingExpenses'] = display_df['OperatingExpenses'].apply(lambda x: f"${x:,.0f}M")
    display_df['MarketCap'] = display_df['MarketCap'].apply(lambda x: f"${x:,.0f}M")
    display_df['StockPrice'] = display_df['StockPrice'].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"faang_financial_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>💡 <strong>FAANG Financial Dashboard</strong> | Sample data for demonstration purposes</p>
            <p>Data reflects quarterly financial metrics from 2020-2024</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
