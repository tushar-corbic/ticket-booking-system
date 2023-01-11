import pandas as pd
import pyarrow

df = pd.read_csv("/home/tushar/Downloads/fno_ticks_11-01-2023.csv", nrows=10000)

df.to_parquet("/home/tushar/Downloads/output.parquet", engine="pyarrow")


print(df["isin"].unique())


