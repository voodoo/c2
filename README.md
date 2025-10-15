# 📊 FAANG Financial Dashboard

A comprehensive Streamlit dashboard for visualizing financial data from major tech companies (Facebook/Meta, Apple, Amazon, Netflix, and Google/Alphabet).

## 🌟 Features

- **Interactive Visualizations**: Multiple chart types including line charts, bar charts, and pie charts
- **Dynamic Filtering**: Filter by company, date range, and financial metrics
- **Key Performance Indicators**: Real-time display of critical financial metrics
- **Year-over-Year Growth Analysis**: Compare revenue growth across companies and time periods
- **Data Export**: Download filtered data as CSV for further analysis
- **Responsive Design**: Works seamlessly on different screen sizes

## 📈 Visualizations Included

1. **Revenue Comparison** - Bar chart comparing latest quarterly revenue
2. **Stock Price Trends** - Historical stock price movements
3. **Net Income Trends** - Profitability analysis over time
4. **Market Cap Distribution** - Pie chart showing market capitalization breakdown
5. **Custom Metric Analysis** - Flexible analysis of selected financial metrics
6. **YoY Growth Rates** - Year-over-year revenue growth comparison

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/paul/dev/cline/c2
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Dashboard

1. **Start the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

2. **Access the dashboard:**
   - The dashboard will automatically open in your default web browser
   - If not, navigate to: `http://localhost:8501`

## 📁 Project Structure

```
.
├── app.py                    # Main Streamlit application
├── data/
│   └── financial_data.csv    # Sample FAANG financial data (2020-2024)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 💾 Data Overview

The dashboard uses sample financial data for FAANG companies covering:
- **Time Period**: Q1 2020 - Q3 2024 (quarterly data)
- **Companies**: Meta, Apple, Amazon, Netflix, Alphabet
- **Metrics**:
  - Revenue (in millions)
  - Net Income (in millions)
  - Operating Expenses (in millions)
  - Market Capitalization (in millions)
  - Stock Price (in dollars)
  - P/E Ratio

## 🎛️ Using the Dashboard

### Sidebar Controls

- **Select Companies**: Choose one or multiple companies to analyze
- **Select Date Range**: Filter data by specific time periods
- **Select Financial Metric**: Switch between different financial indicators for custom analysis

### Main Dashboard Sections

1. **Key Performance Indicators**: Quick overview of total revenue, net income, market cap, and average P/E ratio
2. **Visualization Panels**: Six interactive charts showing different aspects of financial performance
3. **Detailed Data Table**: Comprehensive view of all data points with formatting
4. **Export Function**: Download button to export filtered data as CSV

### Tips for Analysis

- Use the company filter to compare specific companies
- Adjust date ranges to focus on particular time periods
- Switch between metrics to analyze different financial aspects
- Hover over charts for detailed information
- Use the year-over-year growth chart to identify trends

## 📦 Dependencies

- **streamlit** (1.28.0): Web application framework
- **pandas** (2.1.1): Data manipulation and analysis
- **plotly** (5.17.0): Interactive visualizations
- **numpy** (1.26.0): Numerical computations

## 🔧 Customization

### Adding New Companies

1. Edit `data/financial_data.csv` to include new company data
2. Update the `COMPANY_COLORS` dictionary in `app.py` with color codes for new companies

### Modifying Visualizations

- Chart configurations can be adjusted in the respective sections of `app.py`
- Use Plotly's extensive customization options for styling and interactivity

### Adding New Metrics

1. Add new columns to `data/financial_data.csv`
2. Include the metric in the sidebar `metric_option` selectbox
3. Update the format function with appropriate labels

## 🎨 Color Scheme

Each company has a distinctive color for easy identification:
- **Meta**: Blue (#1877F2)
- **Apple**: Gray (#555555)
- **Amazon**: Orange (#FF9900)
- **Netflix**: Red (#E50914)
- **Alphabet**: Light Blue (#4285F4)

## 📝 Notes

- This dashboard uses sample/mock data for demonstration purposes
- Data reflects realistic quarterly financial patterns but is not actual company data
- The application uses Streamlit's caching mechanism for optimal performance

## 🤝 Support

For issues or questions about the dashboard:
- Check that all dependencies are correctly installed
- Ensure Python version is 3.8 or higher
- Verify that the data file exists in the `data/` directory

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

**Built with Streamlit** 🎈
