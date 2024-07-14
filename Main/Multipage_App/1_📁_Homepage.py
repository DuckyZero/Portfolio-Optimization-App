import streamlit as st

# Set the page title and icon
st.set_page_config(
    page_title="Portfolio Optimization App",
    page_icon="📈"
)

# Header and introduction
st.title("Welcome to the Portfolio Optimization App!")
st.write("""
Optimize your investment portfolio using Modern Portfolio Theory (MPT). This app allows you to select multiple stock tickers, choose a date range, and optimize your portfolio based on risk and return metrics.
""")

# Features and instructions
st.header("Features:")
st.markdown("""
- **Portfolio Optimizer:** Select from a range of stock tickers and specify your investment period.
- **Risk Management:** Adjust portfolio weights dynamically using a slider to suit your risk tolerance.
- **Performance Metrics:** Evaluate the expected return, volatility, and Sharpe Ratio of your optimized portfolio.
""")

st.header("Instructions:")
st.markdown("""
1. **Select Tickers:** Enter stock tickers separated by commas in the sidebar input field.
2. **Choose Dates:** Use the date picker to select your desired start date.
3. **Adjust Weight Constraint:** Slide the max weight constraint to set allocation limits for each asset.
4. **View Results:** Analyze optimal portfolio weights and performance metrics displayed below.
""")

# Example or demo section
st.header("Example:")
st.markdown("""
To get started, you can enter tickers like `AAPL, MSFT, GOOGL, AMZN, FB`, choose a start date, and adjust the max weight constraint to explore different portfolio compositions.
""")

# Footer or additional notes
st.header("Notes:")
st.markdown("""
- Ensure valid stock tickers are entered to retrieve data successfully.
- Historical data availability may vary for different tickers and date ranges.
- This app uses Modern Portfolio Theory (MPT) to optimize portfolio allocation.
""")


