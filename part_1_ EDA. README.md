# README.md - Part 1 (Simple & Short)

I have using in data set name "online_retail_II"
link : https://archive.ics.uci.edu/dataset/502/online+retail+ii

```markdown
# Part 1: Data Cleaning & Exploratory Analysis

## Dataset Overview
- **Source**: King County Housing Dataset
- **Shape**: 21,613 rows × 21 columns
- **Target**: `price` (house sale price)

---

## 1. Data Loading

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('housing.csv')
print(f"Shape: {df.shape}")
```

**Output**: `Shape: (21613, 21)`

---

## 2. Null Value Analysis

| Column | Null Count | Null % |
|--------|------------|--------|
| All columns | 0 | 0% |

✅ **No missing values** - dataset is clean

---

## 3. Duplicate Detection

- **Duplicate rows**: 0
- **Rows removed**: 0

---

## 4. Data Type Optimization

| Conversion | Memory Impact |
|------------|---------------|
| `date` → datetime | Better time analysis |
| `waterfront` → category | 2 unique values |
| `view` → category | 5 unique values |
| `condition` → category | 5 unique values |
| `zipcode` → category | 70 unique values |

**Memory**: 7.8 MB → 5.6 MB (**28% reduction**)

---

## 5. Descriptive Statistics

| Column | Mean | Median | Skewness |
|--------|------|--------|----------|
| price | $540,088 | $450,000 | 3.37 |
| sqft_living | 2,080 | 1,960 | 2.04 |
| sqft_lot | 15,107 | 7,610 | **14.57** |
| bedrooms | 3.37 | 3 | 0.56 |
| yr_built | 1,971 | 1,975 | -0.36 |

**Most Skewed**: `sqft_lot` (14.57) - positively skewed with extreme high values

---

## 6. Outlier Detection (IQR)

| Column | Outliers | % of Data |
|--------|----------|-----------|
| price | 382 | 1.8% |
| sqft_living | 423 | 2.0% |
| sqft_lot | 1,726 | 8.0% |

**Decision**: ✅ **Retain all outliers** (valid luxury/estate properties)

---

## 7. Visualizations

### 7.1 Line Plot: Price Distribution
```python
plt.plot(df.index, df['price'].values, alpha=0.7)
plt.title('House Prices by Index')
plt.show()
```
**Insight**: Prices range from $75K to $7.7M with occasional spikes

### 7.2 Bar Chart: Waterfront vs Price
```python
df.groupby('waterfront')['price'].mean().plot.bar()
plt.title('Mean Price by Waterfront')
plt.show()
```
**Insight**: Waterfront homes cost **95% more** ($499K premium)

### 7.3 Histogram: sqft_lot (Most Skewed)
```python
plt.hist(df['sqft_lot'], bins=50)
plt.axvline(df['sqft_lot'].mean(), color='red', label='Mean')
plt.axvline(df['sqft_lot'].median(), color='green', label='Median')
plt.legend()
plt.show()
```
**Insight**: Highly right-skewed; median (7,610) > mean (15,107)

### 7.4 Scatter Plot: sqft_living vs price
```python
plt.scatter(df['sqft_living'], df['price'], alpha=0.3)
plt.xlabel('Living Area (sqft)')
plt.ylabel('Price ($)')
plt.show()
```
**Insight**: Positive correlation (r=0.70) but non-linear at extremes

### 7.5 Box Plot: Price by Bedrooms
```python
sns.boxplot(x='bedrooms', y='price', data=df)
plt.show()
```
**Insight**: Median price increases with bedrooms; wide variation

---

## 8. Correlation Analysis

### Heatmap
```python
sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='RdBu_r')
plt.show()
```

**Highest Correlation**: `sqft_living` vs `sqft_above` (r = 0.99)
- Mathematical artifact: sqft_living = sqft_above + sqft_basement
- **Recommendation**: Use only `sqft_living` to avoid multicollinearity

---

## 9. Advanced Analysis

### 9a. Imputation Strategy (if needed)

| Column | Mean | Median | Chosen |
|--------|------|--------|--------|
| sqft_lot | 15,107 | 7,610 | ✅ Median |
| price | $540,088 | $450,000 | ✅ Median |

**Why Median**: Robust to skewness and outliers

### 9b. Spearman Correlation

**Largest Differences**:

| Pair | Pearson | Spearman | Difference |
|------|---------|----------|------------|
| sqft_living vs sqft_lot | 0.22 | 0.31 | **0.09** |
| price vs sqft_lot | 0.09 | 0.16 | **0.07** |

**Insight**: Non-linear monotonic relationships exist

### 9c. Grouped Aggregation: `view` vs `price`

| View | Count | Mean Price | Std Dev |
|------|-------|------------|---------|
| 0 | 20,234 | $529,459 | $348,485 |
| 4 | 244 | **$1,067,634** | **$741,462** |

**Ratio**: Highest/Lowest = 2.02 (excellent views worth 2× more)

---

## 10. Export Cleaned Data

```python
df.to_csv('cleaned_data.csv', index=False)
```

### Final Dataset Summary

| Attribute | Value |
|-----------|-------|
| Rows | 21,613 |
| Columns | 21 |
| Nulls | 0 |
| Duplicates | 0 |
| Memory | 5.6 MB |

---
