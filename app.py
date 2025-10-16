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

# Data validation function
def validate_data_format(df):
    """Validate that uploaded data has required columns and format"""
    required_columns = ['Date', 'Company', 'Revenue', 'NetIncome', 'OperatingExpenses', 'MarketCap', 'StockPrice', 'PERatio']
    errors = []
    
    # Check if all required columns exist
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    if not errors:
        # Check data types and format
        try:
            # Try to convert Date column
            pd.to_datetime(df['Date'])
        except:
            errors.append("Date column must be in a valid date format (YYYY-MM-DD)")
        
        # Check numeric columns
        numeric_columns = ['Revenue', 'NetIncome', 'OperatingExpenses', 'MarketCap', 'StockPrice', 'PERatio']
        for col in numeric_columns:
            if col in df.columns:
                try:
                    pd.to_numeric(df[col], errors='raise')
                except:
                    errors.append(f"Column '{col}' must contain numeric values only")
    
    return errors

# Process uploaded file
def process_uploaded_file(uploaded_file):
    """Process uploaded CSV or Excel file"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            return None, ["File must be CSV or Excel format"]
        
        # Validate data format
        validation_errors = validate_data_format(df)
        if validation_errors:
            return None, validation_errors
        
        # Process the data
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year
        df['Quarter'] = df['Date'].dt.quarter
        
        return df, []
    except Exception as e:
        return None, [f"Error processing file: {str(e)}"]

# Save data function
def save_data_to_file(df, backup_original=True):
    """Save dataframe to CSV file with optional backup"""
    try:
        if backup_original and os.path.exists('data/financial_data.csv'):
            # Create backup of original file
            backup_filename = f"data/financial_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            original_df = pd.read_csv('data/financial_data.csv')
            original_df.to_csv(backup_filename, index=False)
        
        # Save new data
        df_to_save = df.copy()
        df_to_save = df_to_save.drop(['Year', 'Quarter'], axis=1, errors='ignore')
        df_to_save.to_csv('data/financial_data.csv', index=False)
        return True, "Data saved successfully!"
    except Exception as e:
        return False, f"Error saving data: {str(e)}"

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
    
    # Import Data Section
    st.sidebar.markdown("---")
    st.sidebar.header("📥 Import Data")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload Financial Data",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a CSV or Excel file with financial data. Required columns: Date, Company, Revenue, NetIncome, OperatingExpenses, MarketCap, StockPrice, PERatio"
    )
    
    if uploaded_file is not None:
        # Process the uploaded file
        new_df, errors = process_uploaded_file(uploaded_file)
        
        if errors:
            st.sidebar.error("❌ File validation errors:")
            for error in errors:
                st.sidebar.error(f"• {error}")
        else:
            st.sidebar.success("✅ File validation passed!")
            
            # Show preview
            with st.sidebar.expander("📋 Preview Data", expanded=False):
                st.dataframe(new_df.head(), use_container_width=True)
            
            # Import options
            st.sidebar.subheader("Import Options")
            import_mode = st.sidebar.radio(
                "Choose import mode:",
                ["Replace existing data", "Append to existing data"],
                help="Replace: Overwrites current data. Append: Adds to current data."
            )
            
            if st.sidebar.button("🚀 Import Data", type="primary"):
                if import_mode == "Replace existing data":
                    final_df = new_df
                else:
                    # Append mode - combine with existing data
                    original_df = load_data()
                    # Remove Year and Quarter columns for combining
                    original_clean = original_df.drop(['Year', 'Quarter'], axis=1, errors='ignore')
                    new_clean = new_df.drop(['Year', 'Quarter'], axis=1, errors='ignore')
                    final_df = pd.concat([original_clean, new_clean], ignore_index=True)
                    final_df = final_df.drop_duplicates()
                    # Re-add computed columns
                    final_df['Date'] = pd.to_datetime(final_df['Date'])
                    final_df['Year'] = final_df['Date'].dt.year
                    final_df['Quarter'] = final_df['Date'].dt.quarter
                
                # Save the data
                success, message = save_data_to_file(final_df)
                if success:
                    st.sidebar.success(f"✅ {message}")
                    st.sidebar.info("🔄 Refresh the page to see updated data")
                    st.sidebar.balloons()
                else:
                    st.sidebar.error(f"❌ {message}")
    
    # Data Management Section
    st.sidebar.markdown("---")
    st.sidebar.header("🔧 Data Management")
    
    # Show current data info
    current_df = load_data()
    st.sidebar.info(f"""
    **Current Dataset:**
    • Records: {len(current_df):,}
    • Companies: {current_df['Company'].nunique()}
    • Date Range: {current_df['Date'].min().strftime('%Y-%m-%d')} to {current_df['Date'].max().strftime('%Y-%m-%d')}
    """)
    
    # Download template
    template_df = pd.DataFrame({
        'Date': ['2024-12-31'],
        'Company': ['Example Corp'],
        'Revenue': [50000],
        'NetIncome': [10000],
        'OperatingExpenses': [30000],
        'MarketCap': [500000],
        'StockPrice': [150.00],
        'PERatio': [25.0]
    })
    
    csv_template = template_df.to_csv(index=False)
    st.sidebar.download_button(
        label="📄 Download Template CSV",
        data=csv_template,
        file_name="financial_data_template.csv",
        mime="text/csv",
        help="Download a template CSV file with the correct format for importing data"
    )
    
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
