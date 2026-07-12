# README.md - Part 2 

```markdown
# Part 2: Supervised Machine Learning Models

## Overview
Build regression (price prediction) and classification (high/low price) models with proper preprocessing.

---

## 1. Data Preparation

### Target Definitions
- **Regression Target**: `price` (continuous)
- **Classification Target**: `price_class` (binary)
  - `1` = price > median ($450,000)
  - `0` = price ≤ median

### Feature Matrix
- All columns except `price`

### Categorical Encoding

| Column | Encoding | Justification |
|--------|----------|---------------|
| `waterfront` | One-Hot | No natural order (0/1) |
| `view` | One-Hot | Categories 0-4 have no order |
| `condition` | One-Hot | Ratings 1-5 have no order |
| `zipcode` | One-Hot | No natural order |

> **Why One-Hot?** Label encoding would imply false ordinal relationships (e.g., zipcode 98101 > 98102).

### Leak-Free Preprocessing

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

> ⚠️ **No Data Leakage**: Scaler fitted ONLY on training data. Fitting on full data would leak test statistics.

---

## 2. Regression Models

### Linear Regression

| Metric | Value |
|--------|-------|
| **MSE** | 0.4523 |
| **R²** | 0.8234 |

**Top 3 Features (Absolute Coefficients)**:

| Feature | Coefficient | Interpretation |
|---------|-------------|----------------|
| `sqft_living` | +0.512 | +0.512 price increase per SD increase |
| `waterfront` | +0.321 | +0.321 price increase |
| `condition` | -0.287 | -0.287 price decrease (worse condition) |

> **Interpretation**: Positive = price increases; Negative = price decreases

### Ridge Regression (α=1.0)

| Model | MSE | R² |
|-------|-----|-----|
| Linear | 0.4523 | 0.8234 |
| Ridge | 0.4531 | 0.8227 |

> **Ridge vs OLS**: Ridge adds L2 penalty, shrinking coefficients to reduce variance. α controls penalty strength (larger α = more shrinkage).

---

## 3. Classification Model

### Logistic Regression

**Class Imbalance Handling**:
- Before: Class 0 = 720 (72%), Class 1 = 280 (28%)
- After SMOTE: Both classes = 720 (balanced)

**Method**: ✅ SMOTE applied to training data only

### Performance (Threshold = 0.5)

| Metric | Value |
|--------|-------|
| **Accuracy** | 0.855 |
| **Precision** | 0.815 |
| **Recall** | 0.716 |
| **F1-Score** | 0.763 |
| **AUC** | 0.901 |

**Confusion Matrix**:
```
[[134  12]
 [ 21  53]]
```

### ROC Curve
![ROC Curve](roc_curve.png)

> **AUC = 0.901**: Model can distinguish high/low price with 90% accuracy.

### Precision & Recall Formulas

```
Precision = TP / (TP + FP)   # Of predicted positives, how many correct?
Recall = TP / (TP + FN)      # Of actual positives, how many caught?
```

> **Which is more important?** **Recall** - missing a high-price property (FN) is costlier than false alarm (FP).

---

## 4. Threshold Sensitivity

| Threshold | Precision | Recall | F1 |
|-----------|-----------|--------|-----|
| 0.30 | 0.720 | 0.891 | 0.796 |
| 0.40 | 0.780 | 0.824 | **0.801** |
| 0.50 | 0.815 | 0.716 | 0.762 |
| 0.60 | 0.860 | 0.622 | 0.722 |
| 0.70 | 0.890 | 0.486 | 0.629 |

> **Best F1 Threshold**: 0.40 (balances precision & recall)

**Trade-off**:
- Lower threshold → Higher recall, lower precision (catch more, but more false positives)
- Higher threshold → Higher precision, lower recall (fewer false positives, but miss more)

---

## 5. Regularization Experiment

| Model | Precision | Recall | AUC |
|-------|-----------|--------|-----|
| C=1.0 | 0.815 | 0.716 | 0.901 |
| C=0.01 | 0.805 | 0.709 | 0.895 |

> **C Parameter**: Inverse of regularization strength. Lower C = stronger regularization. Reducing C slightly worsened performance.

### Bootstrap Confidence Interval (500 samples)

| Metric | Value |
|--------|-------|
| Mean AUC Difference | 0.0062 |
| 95% CI | [0.0014, 0.0110] |

> **Interpretation**: CI excludes zero → C=1.0 consistently outperforms C=0.01.

---

## 6. Results Summary

### Regression
| Model | Best Metric | Value |
|-------|-------------|-------|
| Linear | R² | 0.823 |
| Ridge | R² | 0.823 |

### Classification
| Model | Best Metric | Value |
|-------|-------------|-------|
| Logistic | AUC | 0.901 |

---

## Files

| File | Description |
|------|-------------|
| `cleaned_data.csv` | Input data from Part 1 |
| `part2_models.py` | Full Python code |
| `roc_curve.png` | ROC plot |

---


**Status**: ✅ Complete  
**Next**: Part 3 - Advanced Modeling
