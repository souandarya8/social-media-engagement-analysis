import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 1. LOAD CLEAN DATA
# ============================================================

df = pd.read_csv(
    "../data/processed/social_media_clean.csv"
)

print("=" * 60)
print("SOCIAL MEDIA ENGAGEMENT - EDA")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())


# ============================================================
# 2. KEY BUSINESS METRICS
# ============================================================

print("\n" + "=" * 60)
print("KEY METRICS")
print("=" * 60)

print("Total Posts:", len(df))

print("Total Views:", f"{df['views'].sum():,.0f}")

print(
    "Average Views:",
    f"{df['views'].mean():,.2f}"
)

print(
    "Average Engagement Rate:",
    f"{df['engagement_rate'].mean() * 100:.2f}%"
)

print(
    "Total Engagement:",
    f"{df['total_engagement'].sum():,.0f}"
)

print(
    "Average Engagement:",
    f"{df['total_engagement'].mean():,.2f}"
)

print(
    "Viral Posts:",
    df["is_viral"].sum()
)

print(
    "Viral Rate:",
    f"{df['is_viral'].mean() * 100:.2f}%"
)


# ============================================================
# 3. PLATFORM ANALYSIS
# ============================================================

platform_analysis = (
    df.groupby("platform")
    .agg(
        posts=("post_id", "count"),
        avg_views=("views", "mean"),
        total_views=("views", "sum"),
        avg_engagement_rate=("engagement_rate", "mean"),
        avg_likes=("likes", "mean"),
        avg_comments=("comments", "mean"),
        avg_shares=("shares", "mean"),
        viral_rate=("is_viral", "mean")
    )
    .reset_index()
)

platform_analysis["avg_engagement_rate"] *= 100
platform_analysis["viral_rate"] *= 100

print("\n" + "=" * 60)
print("PLATFORM ANALYSIS")
print("=" * 60)

print(
    platform_analysis.sort_values(
        "avg_engagement_rate",
        ascending=False
    ).to_string(index=False)
)


# Platform chart

plt.figure(figsize=(10, 6))

sns.barplot(
    data=platform_analysis,
    x="platform",
    y="avg_engagement_rate"
)

plt.title("Average Engagement Rate by Platform")
plt.xlabel("Platform")
plt.ylabel("Average Engagement Rate (%)")

plt.tight_layout()
plt.show()


# ============================================================
# 4. CONTENT TYPE ANALYSIS
# ============================================================

content_analysis = (
    df.groupby("content_type")
    .agg(
        posts=("post_id", "count"),
        avg_views=("views", "mean"),
        avg_engagement_rate=("engagement_rate", "mean"),
        avg_shares=("shares", "mean"),
        viral_rate=("is_viral", "mean")
    )
    .reset_index()
)

content_analysis["avg_engagement_rate"] *= 100
content_analysis["viral_rate"] *= 100

print("\n" + "=" * 60)
print("CONTENT TYPE ANALYSIS")
print("=" * 60)

print(
    content_analysis.sort_values(
        "avg_engagement_rate",
        ascending=False
    ).to_string(index=False)
)


# ============================================================
# 5. TOPIC ANALYSIS
# ============================================================

topic_analysis = (
    df.groupby("topic")
    .agg(
        posts=("post_id", "count"),
        avg_views=("views", "mean"),
        avg_engagement_rate=("engagement_rate", "mean"),
        avg_shares=("shares", "mean"),
        viral_rate=("is_viral", "mean")
    )
    .reset_index()
)

topic_analysis["avg_engagement_rate"] *= 100
topic_analysis["viral_rate"] *= 100

print("\n" + "=" * 60)
print("TOPIC ANALYSIS")
print("=" * 60)

print(
    topic_analysis.sort_values(
        "avg_engagement_rate",
        ascending=False
    ).to_string(index=False)
)


# ============================================================
# 6. VIRAL VS NON-VIRAL ANALYSIS
# ============================================================

viral_analysis = (
    df.groupby("is_viral")
    .agg(
        posts=("post_id", "count"),
        avg_views=("views", "mean"),
        avg_likes=("likes", "mean"),
        avg_comments=("comments", "mean"),
        avg_shares=("shares", "mean"),
        avg_engagement_rate=("engagement_rate", "mean")
    )
    .reset_index()
)

viral_analysis["avg_engagement_rate"] *= 100

viral_analysis["viral_status"] = viral_analysis[
    "is_viral"
].map({
    0: "Non-Viral",
    1: "Viral"
})

print("\n" + "=" * 60)
print("VIRAL ANALYSIS")
print("=" * 60)

print(
    viral_analysis[
        [
            "viral_status",
            "posts",
            "avg_views",
            "avg_likes",
            "avg_comments",
            "avg_shares",
            "avg_engagement_rate"
        ]
    ].to_string(index=False)
)


# ============================================================
# 7. CORRELATION ANALYSIS
# ============================================================

correlation = df[
    [
        "sentiment_score",
        "engagement_rate",
        "views",
        "likes",
        "comments",
        "shares"
    ]
].corr()

print("\n" + "=" * 60)
print("CORRELATION ANALYSIS")
print("=" * 60)

print(correlation.round(3))


# Correlation heatmap

plt.figure(figsize=(9, 7))

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title("Correlation Between Social Media Metrics")

plt.tight_layout()
plt.show()


# ============================================================
# 8. SENTIMENT VS ENGAGEMENT
# ============================================================

plt.figure(figsize=(8, 6))

sns.scatterplot(
    data=df,
    x="sentiment_score",
    y="engagement_rate",
    alpha=0.4
)

plt.title(
    "Sentiment Score vs Engagement Rate"
)

plt.xlabel("Sentiment Score")

plt.ylabel("Engagement Rate")

plt.tight_layout()

plt.show()


# ============================================================
# 9. DAY OF WEEK ANALYSIS
# ============================================================

day_analysis = (
    df.groupby("day_of_week")
    .agg(
        posts=("post_id", "count"),
        avg_engagement_rate=("engagement_rate", "mean"),
        avg_views=("views", "mean")
    )
    .reset_index()
)

day_analysis["avg_engagement_rate"] *= 100

print("\n" + "=" * 60)
print("DAY OF WEEK ANALYSIS")
print("=" * 60)

print(
    day_analysis.sort_values(
        "avg_engagement_rate",
        ascending=False
    ).to_string(index=False)
)


# ============================================================
# 10. POSTING HOUR ANALYSIS
# ============================================================

hour_analysis = (
    df.groupby("post_hour")
    .agg(
        posts=("post_id", "count"),
        avg_engagement_rate=("engagement_rate", "mean"),
        avg_views=("views", "mean")
    )
    .reset_index()
)

hour_analysis["avg_engagement_rate"] *= 100

print("\n" + "=" * 60)
print("POSTING HOUR ANALYSIS")
print("=" * 60)

print(
    hour_analysis.sort_values(
        "avg_engagement_rate",
        ascending=False
    ).to_string(index=False)
)


# ============================================================
# 11. REGION ANALYSIS
# ============================================================

region_analysis = (
    df.groupby("region")
    .agg(
        posts=("post_id", "count"),
        avg_views=("views", "mean"),
        avg_engagement_rate=("engagement_rate", "mean"),
        viral_rate=("is_viral", "mean")
    )
    .reset_index()
)

region_analysis["avg_engagement_rate"] *= 100
region_analysis["viral_rate"] *= 100

print("\n" + "=" * 60)
print("REGION ANALYSIS")
print("=" * 60)

print(
    region_analysis.sort_values(
        "avg_engagement_rate",
        ascending=False
    ).to_string(index=False)
)


# ============================================================
# 12. LANGUAGE ANALYSIS
# ============================================================

language_analysis = (
    df.groupby("language")
    .agg(
        posts=("post_id", "count"),
        avg_views=("views", "mean"),
        avg_engagement_rate=("engagement_rate", "mean"),
        viral_rate=("is_viral", "mean")
    )
    .reset_index()
)

language_analysis["avg_engagement_rate"] *= 100
language_analysis["viral_rate"] *= 100

print("\n" + "=" * 60)
print("LANGUAGE ANALYSIS")
print("=" * 60)

print(
    language_analysis.sort_values(
        "avg_engagement_rate",
        ascending=False
    ).to_string(index=False)
)


# ============================================================
# 13. HASHTAG ANALYSIS
# ============================================================

df["hashtag_count"] = (
    df["hashtags"]
    .fillna("")
    .str.count("#")
)

hashtag_analysis = (
    df.groupby("hashtag_count")
    .agg(
        posts=("post_id", "count"),
        avg_engagement_rate=("engagement_rate", "mean"),
        avg_views=("views", "mean"),
        viral_rate=("is_viral", "mean")
    )
    .reset_index()
)

hashtag_analysis["avg_engagement_rate"] *= 100
hashtag_analysis["viral_rate"] *= 100

print("\n" + "=" * 60)
print("HASHTAG ANALYSIS")
print("=" * 60)

print(
    hashtag_analysis.to_string(index=False)
)


# ============================================================
# 14. PLATFORM × CONTENT TYPE
# ============================================================

platform_content = pd.pivot_table(
    df,
    values="engagement_rate",
    index="platform",
    columns="content_type",
    aggfunc="mean"
)

platform_content *= 100

print("\n" + "=" * 60)
print("PLATFORM × CONTENT TYPE")
print("=" * 60)

print(
    platform_content.round(2)
)


# ============================================================
# 15. TOP 20 POSTS
# ============================================================

top_posts = (
    df.sort_values(
        "engagement_rate",
        ascending=False
    )
    .head(20)
)

print("\n" + "=" * 60)
print("TOP 20 POSTS")
print("=" * 60)

print(
    top_posts[
        [
            "post_id",
            "platform",
            "content_type",
            "topic",
            "views",
            "likes",
            "comments",
            "shares",
            "engagement_rate",
            "is_viral"
        ]
    ].to_string(index=False)
)


# ============================================================
# 16. SAVE EDA OUTPUTS
# ============================================================

platform_analysis.to_csv(
    "../data/processed/platform_analysis.csv",
    index=False
)

content_analysis.to_csv(
    "../data/processed/content_analysis.csv",
    index=False
)

topic_analysis.to_csv(
    "../data/processed/topic_analysis.csv",
    index=False
)

viral_analysis.to_csv(
    "../data/processed/viral_analysis.csv",
    index=False
)

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)
print("\n===== ENGAGEMENT RATE DISTRIBUTION =====")

print(
    df["engagement_rate"]
    .value_counts()
    .head(20)
)

print("\nNumber of posts with exactly 30% ER:")
print(
    (df["engagement_rate"] == 0.30).sum()
)

print("\nTop engagement rates:")
print(
    df["engagement_rate"]
    .nlargest(30)
    .unique()
)
print("\n===== IS_VIRAL vs ENGAGEMENT RATE =====")

print(
    df.groupby("is_viral")["engagement_rate"]
    .agg(["min", "max", "mean", "median"])
)
print("\n===== ENGAGEMENT RATE DISTRIBUTION =====")

print(
    df["engagement_rate"]
    .value_counts()
    .head(20)
)

print("\nPosts with exactly 30% engagement rate:")

print(
    (df["engagement_rate"] == 0.30).sum()
)

print("\nTop Engagement Rates:")

print(
    df["engagement_rate"]
    .nlargest(30)
    .unique()
)

print("\n===== VIRAL vs ENGAGEMENT RATE =====")

print(
    df.groupby("is_viral")["engagement_rate"]
    .agg(["min", "max", "mean", "median"])
)