import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data
@st.cache
def load_data():
    df = pd.read_csv('FINAL_CAPSTONE_DATA.csv')
    df['DATE'] = pd.to_datetime(df['DATE'],format='%d-%m-%Y')
    df.sort_values('DATE', inplace=True)
    return df

df = load_data()

# Sidebar for stock selection
st.sidebar.header('Stock and Industry Selector')
selected_symbol = st.sidebar.selectbox('Select a Stock Symbol:', df['Symbol'].unique())
selected_industry = st.sidebar.selectbox('Select an Industry:', df['Industry'].unique())

# Filter data based on selection
stock_data = df[df['Symbol'] == selected_symbol]
industry_data = df[df['Industry'] == selected_industry]

# Calculate 52-week high and low
def get_high_low(data):
    recent_data = data[data['DATE'] > pd.Timestamp.now() - pd.Timedelta(days=365)]
    return recent_data['Close'].max(), recent_data['Close'].min()

stock_high, stock_low = get_high_low(stock_data)
industry_high, industry_low = get_high_low(industry_data)

# Display Statistics
st.write(f"### Selected Stock: {selected_symbol}")
st.write(f"**52-Week High:** {stock_high}")
st.write(f"**52-Week Low:** {stock_low}")
st.write(f"**Current PE:** {stock_data.iloc[-1]['PE']}")
st.write(f"**Volume:** {stock_data.iloc[-1]['Volume']}")
st.write(f"**EPS:** {stock_data.iloc[-1]['Eps']}")

# Plotting closing price trend
st.write(f"### Closing Price Trend for {selected_symbol}")
fig, ax = plt.subplots()
ax.plot(stock_data['DATE'], stock_data['Close'])
ax.set_title('Closing Price Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Closing Price')
st.pyplot(fig)

# Repeat display for the selected industry
st.write(f"### Selected Industry: {selected_industry}")
st.write(f"**Industry 52-Week High:** {industry_high}")
st.write(f"**Industry 52-Week Low:** {industry_low}")

# Plotting closing price trend for the industry
st.write(f"### Closing Price Trend for {selected_industry}")
fig, ax = plt.subplots()
ax.plot(industry_data['DATE'], industry_data['Close'])
ax.set_title('Industry Closing Price Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Closing Price')
st.pyplot(fig)
