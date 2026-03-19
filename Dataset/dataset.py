import yfinance as yf
import pandas as pd

symbols = ['RELIANCE.NS','TCS.NS','HDFCBANK.NS','INFY.NS','HINDUNILVR.NS','ICICIBANK.NS',
           'KOTAKBANK.NS','BHARTIARTL.NS','ITC.NS','SBIN.NS','LT.NS','ASIANPAINT.NS',
           'AXISBANK.NS','MARUTI.NS','ULTRACEMCO.NS','NESTLEIND.NS','SUNPHARMA.NS',
           'TITAN.NS','DMART.NS','BAJFINANCE.NS','WIPRO.NS','NTPC.NS','POWERGRID.NS',
           'TECHM.NS','HCLTECH.NS','HDFCLIFE.NS','DIVISLAB.NS','CIPLA.NS','JSWSTEEL.NS',
           'COALINDIA.NS','TATASTEEL.NS','GRASIM.NS','ONGC.NS','BPCL.NS','HEROMOTOCO.NS',
           'EICHERMOT.NS','DRREDDY.NS','APOLLOHOSP.NS','LTIM.NS','ADANIENT.NS',
           'ADANIPORTS.NS','BAJAJFINSV.NS','TRENT.NS','SHRIRAMFIN.NS','GODREJCP.NS',
           'PIDILITIND.NS','BRITANNIA.NS','INDUSINDBK.NS']

print("💾 SAVING RAW DATASET...")
data = []
for symbol in symbols:
    df = yf.download(symbol, period="5y", progress=False)
    df.reset_index(inplace=True)
    df['Symbol'] = symbol
    data.append(df)

df = pd.concat(data, ignore_index=True)
df.to_csv('chanakya_raw_data.csv', index=False)
print(f"✅ SAVED: chanakya_raw_data.csv ({len(df):,} rows)")