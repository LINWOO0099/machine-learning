import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ==============================
# 1. Load Dataset
# ==============================

df = pd.read_excel("online_retail_II.xlsx")

print("First 5 rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nShape:")
print(df.shape)
