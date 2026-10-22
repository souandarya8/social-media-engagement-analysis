-- ============================================================
-- SOCIAL MEDIA ENGAGEMENT ANALYSIS
-- 01_create_database.sql
-- ============================================================

-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS social_media_analysis;

-- Select the database for the remaining project work
USE social_media_analysis;

-- Verify that the correct database is selected
SELECT DATABASE() AS current_database;
