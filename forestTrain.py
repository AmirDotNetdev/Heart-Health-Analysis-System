
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# --------------------------------
# 1. نام ستون‌های دیتاست
# --------------------------------

columns = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal", "num"
]

# --------------------------------
# 2. خواندن چهار فایل
# --------------------------------

files = [
    "processed.cleveland.data",
    "processed.hungarian.data",
    "processed.switzerland.data",
    "processed.va.data"
]

dataframes = []

for file in files:
    df_part = pd.read_csv(
        file,
        header=None,
        names=columns,
        na_values="?",
        skipinitialspace=True
    )

    dataframes.append(df_part)

# ترکیب چهار دیتاست
df = pd.concat(dataframes, ignore_index=True)

# تبدیل ستون‌ها به عدد
for col in columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# حذف ردیف‌هایی که تشخیص بیماری ندارند
df = df.dropna(subset=["num"]).copy()

# تبدیل تشخیص به دو کلاس:
# 0 = سالم
# 1 = دارای بیماری قلبی
df["target"] = (df["num"] > 0).astype(int)

# ذخیره دیتاست ترکیب‌شده
df.to_csv("heart_disease_uci.csv", index=False)

print("Dataset created successfully!")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))
print("\nClass distribution:")
print(df["target"].value_counts())

# --------------------------------
# 3. مشخص کردن ورودی و خروجی
# --------------------------------

X = df.drop(columns=["num", "target"])
y = df["target"]

# ستون‌های عددی و دسته‌ای
numeric_features = [
    "age", "trestbps", "chol", "thalach", "oldpeak"
]

categorical_features = [
    "sex", "cp", "fbs", "restecg",
    "exang", "slope", "ca", "thal"
]

# --------------------------------
# 4. آماده‌سازی داده‌ها
# --------------------------------

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

# --------------------------------
# 5. ساخت مدل Random Forest
# --------------------------------

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])

# --------------------------------
# 6. تقسیم داده‌ها
# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------------
# 7. آموزش مدل
# --------------------------------

model.fit(X_train, y_train)

# --------------------------------
# 8. ارزیابی مدل
# --------------------------------

y_pred = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# --------------------------------
# 9. ذخیره مدل
# --------------------------------

joblib.dump(model, "heart_model.joblib")

print("\nModel saved successfully: heart_model.joblib")
