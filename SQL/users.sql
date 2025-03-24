INSERT INTO users (
    user_id, customer_name, first_review_date, last_review_date, user_lifetime_days,
    total_reviews, avg_rating, min_rating, max_rating, sentiment_avg_score,
    sentiment_volatility, highly_positive_reviews, highly_negative_reviews, balanced_reviews,
    has_response, avg_response_time, active_years, active_months, peak_activity_year,
    peak_activity_month, review_frequency, recent_activity_score
)
WITH limited_users AS (
    SELECT DISTINCT user_id, customer_name
    FROM reviews 
	where sentiment_confidence is not null
    LIMIT 500
),
user_data AS (
    SELECT 
        r.user_id,
        r.customer_name,
        MIN(r.time) AS first_review_date,
        MAX(r.time) AS last_review_date,
        COUNT(*) AS total_reviews,
        AVG(r.rating) AS avg_rating,
        MIN(r.rating) AS min_rating,
        MAX(r.rating) AS max_rating,
        STDDEV(r.sentiment_confidence) AS sentiment_volatility,
        AVG(r.sentiment_confidence) AS sentiment_avg_score,
        COUNT(CASE WHEN r.sentiment_confidence > 0.8 THEN 1 END) AS highly_positive_reviews,
        COUNT(CASE WHEN r.sentiment_confidence < 0.2 THEN 1 END) AS highly_negative_reviews,
        COUNT(CASE WHEN r.sentiment_confidence BETWEEN 0.4 AND 0.6 THEN 1 END) AS balanced_reviews,
        COUNT(CASE WHEN r.resp IS NOT NULL AND r.resp <> 'None' THEN 1 END) AS has_response,

        -- Extract response time only if 'resp' is valid JSON
        AVG(
            CASE 
                WHEN r.resp IS NOT NULL AND r.resp <> 'None' AND r.resp ~ '^{".+}' 
                THEN EXTRACT(EPOCH FROM (TO_TIMESTAMP((r.resp::json->>'time')::bigint / 1000))) - EXTRACT(EPOCH FROM r.time)
                ELSE NULL
            END
        ) AS avg_response_time,

        COUNT(DISTINCT EXTRACT(YEAR FROM r.time)) AS active_years,
        COUNT(DISTINCT EXTRACT(MONTH FROM r.time)) AS active_months,
        MODE() WITHIN GROUP (ORDER BY EXTRACT(YEAR FROM r.time)) AS peak_activity_year,
        MODE() WITHIN GROUP (ORDER BY EXTRACT(MONTH FROM r.time)) AS peak_activity_month
    FROM reviews r
    JOIN limited_users lu ON r.user_id = lu.user_id
    GROUP BY r.user_id, r.customer_name
)
SELECT 
    user_id,
    customer_name,
    first_review_date,
    last_review_date,
    EXTRACT(DAY FROM last_review_date - first_review_date) AS user_lifetime_days,
    total_reviews,
    avg_rating,
    min_rating,
    max_rating,
    sentiment_avg_score,
    sentiment_volatility,
    highly_positive_reviews,
    highly_negative_reviews,
    balanced_reviews,
    has_response,
    avg_response_time,
    active_years,
    active_months,
    peak_activity_year,
    peak_activity_month,
    ROUND(EXTRACT(DAY FROM last_review_date - first_review_date)::NUMERIC / NULLIF(total_reviews, 0), 2) AS review_frequency,
    ROUND((total_reviews / NULLIF(EXTRACT(DAY FROM NOW() - first_review_date), 0))::NUMERIC, 2) AS recent_activity_score
FROM user_data;
