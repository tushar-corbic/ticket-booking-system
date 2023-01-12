import pandas as pd
import pyarrow

df = pd.read_csv("/home/tushar/Downloads/fno_ticks_11-01-2023.csv", nrows=10000)
print(df.head())
df.to_parquet("/home/tushar/Downloads/output2.parquet")

df = pd.read_parquet("/home/tushar/Downloads/output2.parquet")
df["time"] = df["time"].astype("datetime64[ns]")
df["time"] = df["time"] + pd.Timedelta(days=1,minutes=30, hours=5)
df["local_time"]= df["local_time"].astype("datetime64[ns]")
df["local_time"] =df["local_time"] +pd.Timedelta(days=1,minutes=30, hours=5)
df["expiry"]= df["expiry"].astype("datetime64[ns]")
df["expiry"] =df["expiry"] +pd.Timedelta(days=7,minutes=30, hours=5)
df["price"] = df["price"]+1.00
df["time"] = df["time"].astype("string")
df["local_time"] = df["local_time"].astype("string")
df["expiry"] = df["expiry"].astype("string")

df.to_parquet("/home/tushar/Downloads/output2.parquet")
df = pd.read_parquet("/home/tushar/Downloads/output2.parquet")
print(df.head())


