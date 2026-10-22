-- ============================================================
-- SOCIAL MEDIA ENGAGEMENT ANALYSIS
-- 03_data_cleaning.sql
-- ============================================================
-- Purpose:
-- Perform data-quality and validation checks before analysis.
--
-- IMPORTANT:
-- This file contains SELECT statements only.
-- It does NOT UPDATE, DELETE, ALTER, DROP or MODIFY data.
-- Therefore, it will not affect the Power BI dashboard.
-- ============================================================


USE social_media_analysis;


-- ============================================================
-- 1. CHECK TOTAL ROW COUNT
-- ============================================================

SELECT
    COUNT(*) AS total_posts
FROM fact_social_posts;


-- ============================================================
-- 2. CHECK FOR DUPLICATE POST IDs
-- ============================================================

SELECT
    post_id,
    COUNT(*) AS duplicate_count
FROM fact_social_posts
GROUP BY post_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 3. CHECK NULL VALUES IN IMPORTANT FACT TABLE COLUMNS
-- ============================================================

SELECT
    SUM(post_id IS NULL) AS null_post_id,
    SUM(platform_id IS NULL) AS null_platform_id,
    SUM(content_type_id IS NULL) AS null_content_type_id,
    SUM(region_id IS NULL) AS null_region_id,
    SUM(date_id IS NULL) AS null_date_id,
    SUM(views IS NULL) AS null_views,
    SUM(likes IS NULL) AS null_likes,
    SUM(comments IS NULL) AS null_comments,
    SUM(shares IS NULL) AS null_shares,
    SUM(engagement_rate IS NULL) AS null_engagement_rate,
    SUM(is_viral IS NULL) AS null_viral_status
FROM fact_social_posts;


-- ============================================================
-- 4. CHECK NEGATIVE VALUES
-- ============================================================

SELECT
    COUNT(*) AS negative_views
FROM fact_social_posts
WHERE views < 0;


SELECT
    COUNT(*) AS negative_likes
FROM fact_social_posts
WHERE likes < 0;


SELECT
    COUNT(*) AS negative_comments
FROM fact_social_posts
WHERE comments < 0;


SELECT
    COUNT(*) AS negative_shares
FROM fact_social_posts
WHERE shares < 0;


-- ============================================================
-- 5. CHECK ENGAGEMENT RATE RANGE
-- ============================================================

SELECT
    MIN(engagement_rate) AS minimum_engagement_rate,
    MAX(engagement_rate) AS maximum_engagement_rate,
    ROUND(AVG(engagement_rate) * 100, 2) AS average_engagement_rate_percent
FROM fact_social_posts;


-- ============================================================
-- 6. CHECK POSTING HOUR RANGE
-- ============================================================

SELECT
    MIN(post_hour) AS minimum_post_hour,
    MAX(post_hour) AS maximum_post_hour
FROM fact_social_posts;


-- ============================================================
-- 7. CHECK PLATFORM DIMENSION
-- ============================================================

SELECT
    platform_id,
    platform_name
FROM dim_platform
ORDER BY platform_id;


-- ============================================================
-- 8. CHECK CONTENT DIMENSION
-- ============================================================

SELECT
    content_type_id,
    content_type,
    topic
FROM dim_content
ORDER BY content_type_id;


-- ============================================================
-- 9. CHECK REGION DIMENSION
-- ============================================================

SELECT
    region_id,
    region_code
FROM dim_region
ORDER BY region_id;


-- ============================================================
-- 10. CHECK DATE DIMENSION
-- ============================================================

SELECT
    COUNT(*) AS total_dates,
    MIN(full_date) AS earliest_date,
    MAX(full_date) AS latest_date
FROM dim_date;


-- ============================================================
-- 11. CHECK FACT TABLE FOREIGN KEY MATCHES
-- ============================================================

SELECT COUNT(*) AS unmatched_platform_records
FROM fact_social_posts f
LEFT JOIN dim_platform p
    ON f.platform_id = p.platform_id
WHERE p.platform_id IS NULL;


SELECT COUNT(*) AS unmatched_content_records
FROM fact_social_posts f
LEFT JOIN dim_content c
    ON f.content_type_id = c.content_type_id
WHERE c.content_type_id IS NULL;


SELECT COUNT(*) AS unmatched_region_records
FROM fact_social_posts f
LEFT JOIN dim_region r
    ON f.region_id = r.region_id
WHERE r.region_id IS NULL;


SELECT COUNT(*) AS unmatched_date_records
FROM fact_social_posts f
LEFT JOIN dim_date d
    ON f.date_id = d.date_id
WHERE d.date_id IS NULL;


-- ============================================================
-- 12. CHECK VIRAL STATUS VALUES
-- ============================================================

SELECT
    is_viral,
    COUNT(*) AS total_posts
FROM fact_social_posts
GROUP BY is_viral;


-- ============================================================
-- END OF DATA QUALITY CHECKS
-- ============================================================