
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go

#  function to scrape revenue 
def get_revenue_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    for table in tables:
        if "Revenue" in table.text:
            df = pd.read_html(str(table))[0]
            df.columns = ["Date", "Revenue"]
            df["Date"] = pd.to_datetime(df["Date"])
            df["Revenue"] = df["Revenue"].replace('[\$,]', '', regex=True).astype(float)
            return df
    return pd.DataFrame()

# Tesla Stock Data
tesla = yf.Ticker("TSLA")
tesla_stock = tesla.history(period="5y").reset_index()

#  Tesla Revenue Data
tesla_revenue = get_revenue_data("https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue")

#  GameStop Stock Data
gamestop = yf.Ticker("GME")
gamestop_stock = gamestop.history(period="5y").reset_index()

#  GameStop Revenue Data
gamestop_revenue = get_revenue_data("https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue")

fig_tesla = go.Figure()
fig_tesla.add_trace(go.Scatter(x=tesla_stock["Date"], y=tesla_stock["Close"], name="Tesla Stock Price"))
fig_tesla.add_trace(go.Bar(x=tesla_revenue["Date"], y=tesla_revenue["Revenue"], name="Tesla Revenue"))
fig_tesla.update_layout(title="Tesla: Stock Price vs Revenue", xaxis_title="Date", yaxis_title="USD")
fig_tesla.show()
 

fig_gme = go.Figure()
fig_gme.add_trace(go.Scatter(x=gamestop_stock["Date"], y=gamestop_stock["Close"], name="GameStop Stock Price"))
fig_gme.add_trace(go.Bar(x=gamestop_revenue["Date"], y=gamestop_revenue["Revenue"], name="GameStop Revenue"))
fig_gme.update_layout(title="GameStop: Stock Price vs Revenue", xaxis_title="Date", yaxis_title="USD")
fig_gme.show()


