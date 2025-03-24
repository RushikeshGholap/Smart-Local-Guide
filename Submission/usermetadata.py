from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection settings.
DB_HOST = "192.168.1.103"
DB_PORT = "5432"
DB_NAME = "Capstone"
DB_USER = "postgres"
DB_PASSWORD = "Google#13"

# Create engine and session.
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_size=20,
    max_overflow=40
)
Session = sessionmaker(bind=engine)
session = Session()

TABLE_NAME = "reviews"  # Name of the reviews table.
import pandas as pd
try:
    # Retrieve distinct user_ids from reviews with non-null sentiment_confidence
    # that are not already in the users table.
    print("Starting retrieval of distinct user_ids not present in users table...")
    df = pd.read_sql_query("""select user_id from reviews 
                            where user_id  not in (select user_id from users)""",
                            con=engine)

    df.to_csv('./data/userid_unique.csv')
    # Load user IDs from CSV file
    user_ids = pd.read_csv('./data/userid_unique.csv')['user_id'].to_list()


    batch_size = 5000
    total_users = len(user_ids)
    print(f"Total users to process: {total_users}")

    for i in range(0, total_users, batch_size):
        batch_ids = user_ids[i:i + batch_size]
        print(f"Processing batch {(i // batch_size) + 1} with {len(batch_ids)} users.")

        insert_query = text("""
            WITH limited_users AS (
                SELECT DISTINCT user_id, customer_name
                FROM reviews 
                WHERE sentiment_confidence IS NOT NULL
                  AND user_id = ANY(:batch_ids)
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
                    AVG(
                        CASE 
                            WHEN r.resp IS NOT NULL 
                                 AND r.resp <> 'None' 
                                 AND r.resp ~ '^{".+}' 
                            THEN EXTRACT(EPOCH FROM TO_TIMESTAMP((r.resp::json->>'time')::bigint / 1000))
                                 - EXTRACT(EPOCH FROM r.time)
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
            INSERT INTO users (
                user_id, customer_name, first_review_date, last_review_date, user_lifetime_days,
                total_reviews, avg_rating, min_rating, max_rating, sentiment_avg_score,
                sentiment_volatility, highly_positive_reviews, highly_negative_reviews, balanced_reviews,
                has_response, avg_response_time, active_years, active_months, peak_activity_year,
                peak_activity_month, review_frequency, recent_activity_score
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
            FROM user_data
            WHERE user_id NOT IN (SELECT user_id FROM users)
            ON CONFLICT (user_id) DO NOTHING;
        """)

        session.execute(insert_query, {'batch_ids': batch_ids})
        session.commit()
        print(f"Done batch {(i // batch_size) + 1} with {len(batch_ids)} users.")

except Exception as e:
    session.rollback()
    print("Error occurred:", e)
finally:
    session.close()
