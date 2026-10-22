-- ============================================================
-- SOCIAL MEDIA ENGAGEMENT ANALYSIS
-- 04_analysis_queries.sql
-- ============================================================
-- Purpose:
-- Business analysis queries used to generate insights
-- for the Power BI dashboard.
--
-- IMPORTANT:
-- This file contains SELECT statements only.
-- It does not modify any database tables.
-- ============================================================


USE social_media_analysis;


-- ============================================================
-- 1. OVERALL KPI SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS total_posts,
    ROUND(SUM(views) / 1000000000, 2) AS total_views_billions,
    ROUND(SUM(likes + comments + shares) / 1000000, 2) AS total_engagement_millions,
    SUM(CASE WHEN is_viral = 1 THEN 1 ELSE 0 END) AS viral_posts,
    ROUND(
        AVG(is_viral) * 100,
        2
    ) AS viral_rate_percent,
    ROUND(
        AVG(engagement_rate) * 100,
        2
    ) AS average_engagement_rate_percent
FROM fact_social_posts;


-- ============================================================
-- 2. PLATFORM PERFORMANCE
-- ============================================================

SELECT
    p.platform_name,
    COUNT(*) AS total_posts,
    ROUND(AVG(f.engagement_rate) * 100, 2) AS avg_engagement_rate,
    ROUND(AVG(f.views), 0) AS avg_views,
    ROUND(SUM(f.views), 0) AS total_views
FROM fact_social_posts f
JOIN dim_platform p
    ON f.platform_id = p.platform_id
GROUP BY p.platform_name
ORDER BY avg_engagement_rate DESC;


-- ============================================================
-- 3. VIRAL VS NON-VIRAL PERFORMANCE
-- ============================================================

SELECT
    CASE
        WHEN is_viral = 1 THEN 'Viral'
        ELSE 'Non-Viral'
    END AS viral_status,
    COUNT(*) AS total_posts,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM fact_social_posts),
        2
    ) AS percentage_of_posts,
    ROUND(AVG(engagement_rate) * 100, 2) AS avg_engagement_rate,
    ROUND(AVG(views), 0) AS avg_views
FROM fact_social_posts
GROUP BY is_viral
ORDER BY is_viral DESC;


-- ============================================================
-- 4. ENGAGEMENT BY POSTING HOUR
-- ============================================================

SELECT
    post_hour,
    COUNT(*) AS total_posts,
    ROUND(AVG(engagement_rate) * 100, 2) AS avg_engagement_rate,
    ROUND(AVG(views), 0) AS avg_views
FROM fact_social_posts
GROUP BY post_hour
ORDER BY post_hour;


-- ============================================================
-- 5. CONTENT TYPE PERFORMANCE
-- ============================================================

SELECT
    c.content_type,
    COUNT(*) AS total_posts,
    ROUND(AVG(f.engagement_rate) * 100, 2) AS avg_engagement_rate,
    ROUND(AVG(f.views), 0) AS avg_views,
    ROUND(SUM(f.views), 0) AS total_views
FROM fact_social_posts f
JOIN dim_content c
    ON f.content_type_id = c.content_type_id
GROUP BY c.content_type
ORDER BY avg_engagement_rate DESC;


-- ============================================================
-- 6. TOPICS PERFORMANCE
-- ============================================================

SELECT
    c.topic,
    COUNT(*) AS total_posts,
    ROUND(AVG(f.engagement_rate) * 100, 2) AS avg_engagement_rate,
    ROUND(AVG(f.views), 0) AS avg_views
FROM fact_social_posts f
JOIN dim_content c
    ON f.content_type_id = c.content_type_id
GROUP BY c.topic
ORDER BY avg_engagement_rate DESC;


-- ============================================================
-- 7. REGION PERFORMANCE
-- ============================================================

SELECT
    r.region_code,
    COUNT(*) AS total_posts,
    ROUND(AVG(f.engagement_rate) * 100, 2) AS avg_engagement_rate,
    ROUND(AVG(f.views), 0) AS avg_views
FROM fact_social_posts f
JOIN dim_region r
    ON f.region_id = r.region_id
GROUP BY r.region_code
ORDER BY avg_engagement_rate DESC;


-- ============================================================
-- 8. LANGUAGE PERFORMANCE
-- ============================================================

SELECT
    language,
    COUNT(*) AS total_posts,
    ROUND(AVG(engagement_rate) * 100, 2) AS avg_engagement_rate,
    ROUND(AVG(views), 0) AS avg_views
FROM fact_social_posts
GROUP BY language
ORDER BY avg_engagement_rate DESC;


-- ============================================================
-- 9. SENTIMENT PERFORMANCE
-- ============================================================

SELECT
    CASE
        WHEN sentiment_score >= 0.50 THEN 'Positive'
        WHEN sentiment_score <= -0.50 THEN 'Negative'
        ELSE 'Neutral'
    END AS sentiment_category,
    COUNT(*) AS total_posts,
    ROUND(AVG(engagement_rate) * 100, 2) AS avg_engagement_rate,
    ROUND(AVG(views), 0) AS avg_views
FROM fact_social_posts
WHERE sentiment_score IS NOT NULL
GROUP BY sentiment_category
ORDER BY avg_engagement_rate DESC;


-- ============================================================
-- 10. VIRAL POSTS BY PLATFORM
-- ============================================================

SELECT
    p.platform_name,
    COUNT(*) AS viral_posts,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM fact_social_posts),
        2
    ) AS percentage_of_all_posts
FROM fact_social_posts f
JOIN dim_platform p
    ON f.platform_id = p.platform_id
WHERE f.is_viral = 1
GROUP BY p.platform_name
ORDER BY viral_posts DESC;


-- ============================================================
-- 11. CONTENT TYPE VS VIRAL PERFORMANCE
-- ============================================================

SELECT
    c.content_type,
    CASE
        WHEN f.is_viral = 1 THEN 'Viral'
        ELSE 'Non-Viral'
    END AS viral_status,
    COUNT(*) AS total_posts,
    ROUND(AVG(f.engagement_rate) * 100, 2) AS avg_engagement_rate
FROM fact_social_posts f
JOIN dim_content c
    ON f.content_type_id = c.content_type_id
GROUP BY
    c.content_type,
    f.is_viral
ORDER BY
    c.content_type,
    f.is_viral DESC;


-- ============================================================
-- 12. PLATFORM + CONTENT TYPE ANALYSIS
-- ============================================================

SELECT
    p.platform_name,
    c.content_type,
    COUNT(*) AS total_posts,
    ROUND(AVG(f.engagement_rate) * 100, 2) AS avg_engagement_rate
FROM fact_social_posts f
JOIN dim_platform p
    ON f.platform_id = p.platform_id
JOIN dim_content c
    ON f.content_type_id = c.content_type_id
GROUP BY
    p.platform_name,
    c.content_type
ORDER BY
    p.platform_name,
    avg_engagement_rate DESC;


-- ============================================================
-- 13. TOP 10 POSTS BY ENGAGEMENT RATE
-- ============================================================

SELECT
    post_id,
    engagement_rate,
    views,
    likes,
    comments,
    shares,
    is_viral
FROM fact_social_posts
ORDER BY engagement_rate DESC
LIMIT 10;


-- ============================================================
-- 14. TOP 10 POSTS BY VIEWS
-- ============================================================

SELECT
    post_id,
    views,
    engagement_rate,
    likes,
    comments,
    shares,
    is_viral
FROM fact_social_posts
ORDER BY views DESC
LIMIT 10;


-- ============================================================
-- 15. DAILY ENGAGEMENT TREND
-- ============================================================

SELECT
    d.full_date,
    COUNT(*) AS total_posts,
    ROUND(AVG(f.engagement_rate) * 100, 2) AS avg_engagement_rate,
    ROUND(AVG(f.views), 0) AS avg_views
FROM fact_social_posts f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY d.full_date
ORDER BY d.full_date;


-- ============================================================
-- 16. MONTHLY ENGAGEMENT TREND
-- ============================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(*) AS total_posts,
    ROUND(AVG(f.engagement_rate) * 100, 2) AS avg_engagement_rate
FROM fact_social_posts f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- ============================================================
-- 17. ENGAGEMENT BY DAY OF WEEK
-- ============================================================

SELECT
    d.day_of_week,
    COUNT(*) AS total_posts,
    ROUND(AVG(f.engagement_rate) * 100, 2) AS avg_engagement_rate
FROM fact_social_posts f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY d.day_of_week
ORDER BY avg_engagement_rate DESC;


-- ============================================================
-- 18. PLATFORM VIRAL RATE
-- ============================================================

SELECT
    p.platform_name,
    COUNT(*) AS total_posts,
    SUM(
        CASE
            WHEN f.is_viral = 1 THEN 1
            ELSE 0
        END
    ) AS viral_posts,
    ROUND(
        SUM(
            CASE
                WHEN f.is_viral = 1 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS viral_rate_percent
FROM fact_social_posts f
JOIN dim_platform p
    ON f.platform_id = p.platform_id
GROUP BY p.platform_name
ORDER BY viral_rate_percent DESC;


-- ============================================================
-- END OF ANALYSIS QUERIES
-- ============================================================