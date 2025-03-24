SELECT 
    rating, 
    COUNT(*) AS count, 
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM main), 2) AS percentage
FROM main
GROUP BY rating
ORDER BY rating DESC;



SELECT 
   	business_name, 
    avg(rating) AS avg_rating, 
    COUNT(rating) AS total_reviews
FROM main
GROUP BY business_name
HAVING COUNT(rating) > 50  -- Exclude businesses with too few reviews
ORDER BY total_reviews DESC, avg_rating DESC
LIMIT 10;



SELECT word, COUNT(*) AS frequency
FROM (
    SELECT UNNEST(string_to_array(LOWER(text), ' ')) AS word
    FROM  main
) AS words
WHERE LENGTH(word) > 3
GROUP BY word
ORDER BY frequency DESC
LIMIT 20;




SELECT 
    user_id, 
    COUNT(*) AS total_reviews,  -- Total reviews by the user
    SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) AS total_1_star_reviews,  -- 1-star reviews by the user
    ROUND(100.0 * SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentage_1_star  -- % of 1-star reviews
FROM main
GROUP BY user_id
HAVING COUNT(*) > 50  -- Users who have written more than 50 reviews
ORDER BY percentage_1_star DESC;


SELECT 
    user_id, 
    COUNT(*) AS total_reviews,  -- Total reviews by the user
    SUM(CASE WHEN rating = 5 THEN 1 ELSE 0 END) AS total_5_star_reviews,  -- 1-star reviews by the user
    ROUND(100.0 * SUM(CASE WHEN rating = 5 THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentage_5_star  -- % of 1-star reviews
FROM main
GROUP BY user_id
HAVING COUNT(*) > 60  -- Users who have written more than 50 reviews
ORDER BY percentage_5_star DESC;



SELECT 
    business_name, 
    COUNT(*) AS total_reviews, 
   	AVG(rating) AS avg_rating,
    SUM(CASE WHEN rating = 5 THEN 1 ELSE 0 END) AS total_5_star_reviews,
    ROUND(100.0 * SUM(CASE WHEN rating = 5 THEN 1 ELSE 0 END) / COUNT(*), 2) AS five_star_percentage
FROM main
GROUP BY business_name
HAVING COUNT(*) < 100  -- Exclude businesses with too few reviews
ORDER BY total_5_star_reviews DESC


