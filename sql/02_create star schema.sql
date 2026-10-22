-- ============================================================
-- SOCIAL MEDIA ENGAGEMENT ANALYSIS
-- 02_create_star_schema.sql
-- ============================================================
-- Purpose:
-- Create the dimensional model used for Power BI analysis.
--
-- Star Schema:
--
--                    dim_platform
--                         |
--                         |
-- dim_content ---- fact_social_posts ---- dim_region
--                         |
--                         |
--                      dim_date
--
-- Fact table:
--     fact_social_posts
--
-- Dimension tables:
--     dim_platform
--     dim_content
--     dim_region
--     dim_date
-- ============================================================


USE social_media_analysis;


-- ============================================================
-- 1. PLATFORM DIMENSION
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_platform (
    platform_id INT NOT NULL,
    platform_name VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (platform_id)
);


-- ============================================================
-- 2. CONTENT DIMENSION
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_content (
    content_type_id INT NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    topic VARCHAR(100),
    
    PRIMARY KEY (content_type_id)
);


-- ============================================================
-- 3. REGION DIMENSION
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_region (
    region_id INT NOT NULL,
    region_code VARCHAR(20) NOT NULL,
    
    PRIMARY KEY (region_id)
);


-- ============================================================
-- 4. DATE DIMENSION
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_id INT NOT NULL,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    day_number INT NOT NULL,
    
    PRIMARY KEY (date_id),
    UNIQUE (full_date)
);


-- ============================================================
-- 5. FACT TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_social_posts (
    post_id INT NOT NULL,
    
    platform_id INT NOT NULL,
    content_type_id INT NOT NULL,
    region_id INT NOT NULL,
    date_id INT NOT NULL,
    
    language VARCHAR(10),
    hashtags TEXT,
    sentiment_score DECIMAL(5,3),
    
    views BIGINT,
    likes BIGINT,
    comments BIGINT,
    shares BIGINT,
    
    engagement_rate DECIMAL(10,5),
    is_viral BOOLEAN,
    
    post_hour INT,
    
    PRIMARY KEY (post_id)
);


-- ============================================================
-- 6. FOREIGN KEY RELATIONSHIPS
-- ============================================================

ALTER TABLE fact_social_posts
ADD CONSTRAINT fk_fact_platform
FOREIGN KEY (platform_id)
REFERENCES dim_platform(platform_id);


ALTER TABLE fact_social_posts
ADD CONSTRAINT fk_fact_content
FOREIGN KEY (content_type_id)
REFERENCES dim_content(content_type_id);


ALTER TABLE fact_social_posts
ADD CONSTRAINT fk_fact_region
FOREIGN KEY (region_id)
REFERENCES dim_region(region_id);


ALTER TABLE fact_social_posts
ADD CONSTRAINT fk_fact_date
FOREIGN KEY (date_id)
REFERENCES dim_date(date_id);


-- ============================================================
-- 7. VERIFY STAR SCHEMA TABLES
-- ============================================================

SHOW TABLES;


-- ============================================================
-- 8. VERIFY TABLE STRUCTURES
-- ============================================================

DESCRIBE dim_platform;

DESCRIBE dim_content;

DESCRIBE dim_region;

DESCRIBE dim_date;

DESCRIBE fact_social_posts;