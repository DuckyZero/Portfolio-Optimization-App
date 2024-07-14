import streamlit as st
import pandas as pd

# Set the page title and icon
st.set_page_config(
    page_title="Portfolio Optimization App",
    page_icon="📊"
)

# Header and introduction
st.title("Technologies Used")

# Define the technologies and APIs
technologies = [
    {
        "name": "Streamlit",
        "description": "Used for building and deploying the web application.",
        "link": "https://www.streamlit.io/",
    },
    {
        "name": "yfinance",
        "description": "API for fetching historical stock price data.",
        "link": "https://pypi.org/project/yfinance/",
    },
    {
        "name": "scipy.optimize",
        "description": "Library for numerical optimization.",
        "link": "https://docs.scipy.org/doc/scipy/reference/optimize.html",
    },
    {
        "name": "matplotlib",
        "description": "Library for plotting charts and graphs.",
        "link": "https://matplotlib.org/",
    },
    {
        "name": "fredapi",
        "description": "API for retrieving economic data, used here for the risk-free rate.",
        "link": "https://pypi.org/project/fredapi/",
    },
]

# Display technologies in a table format without index
st.header("Technologies and APIs Used:")
st.write("Below is a summary of the technologies and APIs integrated into the Portfolio Optimization App.")

# Convert technologies to a dataframe for display
tech_df = pd.DataFrame(technologies)

# Display the dataframe without index
st.table(tech_df.set_index('name'))

# Footer with additional information and links
st.write("""
### Additional Notes:
- **Streamlit**: [Streamlit](https://www.streamlit.io/) is a Python library for creating interactive web apps.
- **yfinance**: [yfinance](https://pypi.org/project/yfinance/) allows fetching historical market data from Yahoo Finance.
- **scipy.optimize**: [SciPy](https://docs.scipy.org/doc/scipy/reference/optimize.html) provides optimization algorithms for various mathematical problems.
- **matplotlib**: [matplotlib](https://matplotlib.org/) is a Python plotting library for creating static, animated, and interactive visualizations.
- **fredapi**: [fredapi](https://pypi.org/project/fredapi/) is a Python interface for the FRED (Federal Reserve Economic Data) API, used here to fetch the risk-free rate.
""")

