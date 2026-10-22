import pandas as pd
import numpy as np

# ============================================================
# 1. LOAD RAW DATA
# ============================================================

file_path = "../data/raw/social_media_raw.csv"

df = pd.read_csv(file_path)

print("=" * 60)
print("INITIAL DATASET CHECK")
print("=" * 60)

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nCleaned Columns:")
print(df.columns.tolist())


# ============================================================
# 3. CHECK POST ID
# ============================================================

print("\nDuplicate Post IDs:")
print(df["post_id"].duplicated().sum())

# Remove duplicate post IDs
df = df.drop_duplicates(
    subset="post_id",
    keep="first"
)


# ============================================================
# 4. CONVERT DATE COLUMN
# ============================================================

df["post_datetime"] = pd.to_datetime(
    df["post_datetime"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

print("\nDate Conversion Check:")
print(df["post_datetime"].head())

print(
    "Invalid dates:",
    df["post_datetime"].isna().sum()
)


# ============================================================
# 5. NUMERIC COLUMN CONVERSION
# ============================================================

numeric_columns = [
    "sentiment_score",
    "views",
    "likes",
    "comments",
    "shares",
    "engagement_rate",
    "is_viral"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# 6. CHECK INVALID NUMERIC VALUES
# ============================================================

print("\nMissing Numeric Values:")

print(
    df[numeric_columns]
    .isnull()
    .sum()
)


# ============================================================
# 7. CHECK NEGATIVE VALUES
# ============================================================

count_columns = [
    "views",
    "likes",
    "comments",
    "shares"
]

print("\nNegative Values:")

for column in count_columns:
    print(
        column,
        ":",
        (df[column] < 0).sum()
    )


# ============================================================
# 8. CHECK ZERO VIEWS
# ============================================================

print(
    "\nRows with zero views:",
    (df["views"] == 0).sum()
)


# ============================================================
# 9. HANDLE ZERO VIEWS
# ============================================================

df["views"] = df["views"].replace(0, np.nan)


# ============================================================
# 10. FEATURE ENGINEERING
# ============================================================

df["total_engagement"] = (
    df["likes"]
    + df["comments"]
    + df["shares"]
)

df["engagement_per_1000_views"] = (
    df["total_engagement"]
    / df["views"]
) * 1000

df["like_rate"] = (
    df["likes"]
    / df["views"]
)

df["comment_rate"] = (
    df["comments"]
    / df["views"]
)

df["share_rate"] = (
    df["shares"]
    / df["views"]
)


# ============================================================
# 11. DATE FEATURES
# ============================================================

df["post_date"] = df["post_datetime"].dt.date

df["year"] = (
    df["post_datetime"]
    .dt.year
)

df["month"] = (
    df["post_datetime"]
    .dt.month
)

df["month_name"] = (
    df["post_datetime"]
    .dt.month_name()
)

df["day_of_week"] = (
    df["post_datetime"]
    .dt.day_name()
)

df["post_hour"] = (
    df["post_datetime"]
    .dt.hour
)


# ============================================================
# 12. CALCULATE ENGAGEMENT RATE
# ============================================================

df["calculated_engagement_rate"] = (
    df["likes"]
    + df["comments"]
    + df["shares"]
) / df["views"]


# ============================================================
# 13. COMPARE EXISTING VS CALCULATED ENGAGEMENT RATE
# ============================================================

df["engagement_rate_difference"] = (
    df["engagement_rate"]
    - df["calculated_engagement_rate"]
)

print("\nEngagement Rate Comparison:")

print(
    df[
        [
            "engagement_rate",
            "calculated_engagement_rate",
            "engagement_rate_difference"
        ]
    ].head(10)
)

print(
    "\nAverage ER difference:",
    df["engagement_rate_difference"]
    .abs()
    .mean()
)


# ============================================================
# 14. CHECK SENTIMENT SCORE
# ============================================================

print("\nSentiment Score Range:")

print(
    "Minimum:",
    df["sentiment_score"].min()
)

print(
    "Maximum:",
    df["sentiment_score"].max()
)


# ============================================================
# 15. CHECK ENGAGEMENT RATE RANGE
# ============================================================

print("\nEngagement Rate Range:")

print(
    "Minimum:",
    df["engagement_rate"].min()
)

print(
    "Maximum:",
    df["engagement_rate"].max()
)


# ============================================================
# 16. CHECK CATEGORICAL VALUES
# ============================================================

categorical_columns = [
    "platform",
    "content_type",
    "topic",
    "language",
    "region"
]

print("\nCategorical Value Counts:")

for column in categorical_columns:

    print("\n" + "-" * 40)

    print(column)

    print(
        df[column]
        .value_counts()
    )


# ============================================================
# 17. FINAL MISSING VALUE CHECK
# ============================================================

print("\n" + "=" * 60)
print("FINAL DATA QUALITY CHECK")
print("=" * 60)

print("\nFinal Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Post IDs:")
print(df["post_id"].duplicated().sum())


# ============================================================
# 18. SAVE CLEAN DATA
# ============================================================

output_path = "../data/processed/social_media_clean.csv"

df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 60)

print(
    "Clean dataset saved successfully:"
)

print(output_path)

print("=" * 60)