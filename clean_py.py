import time
import torch
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from datasets import Dataset
from transformers import pipeline
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
# ---------------------------------------------------------------------------
# 1) PostgreSQL / Engine Setup
# ---------------------------------------------------------------------------
DB_HOST = "192.168.1.104"
DB_PORT = "5432"
DB_NAME = "Capstone"
DB_USER = "postgres"
DB_PASSWORD = "Google#13"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_size=20,
    max_overflow=40
)
Session = sessionmaker(bind=engine)
TABLE_NAME = "reviews"

# ---------------------------------------------------------------------------
# 2) GPU-Accelerated Sentiment Pipeline
# ---------------------------------------------------------------------------
device = 0 if torch.cuda.is_available() else -1
print(f"Detected device: {'GPU' if device >= 0 else 'CPU'}")

if device >= 0:
    print("Using GPU:", torch.cuda.get_device_name(device))
else:
    print("Using CPU for inference.")

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    device=device,
)

# ---------------------------------------------------------------------------
# 3) Utility: Fast Vectorized Text Cleaning
# ---------------------------------------------------------------------------
def clean_text_series(series: pd.Series) -> pd.Series:
    """Cleans a Pandas Series of text using vectorized regex operations."""
    return series.str.replace(r"\s+", " ", regex=True).str.strip()

# ---------------------------------------------------------------------------
# 4) Optimized Processing Function
# ---------------------------------------------------------------------------
def process_batch(df_chunk, max_length, batch_size):
    """Processes a batch using sentiment analysis and returns processed data."""
    start_time = time.time()

    # Clean text
    df_chunk["clean_text"] = clean_text_series(df_chunk["text"])

    # Convert to Hugging Face Dataset
    dataset = Dataset.from_pandas(df_chunk[["id", "clean_text"]])

    # Run Sentiment Analysis
    results = sentiment_pipeline(dataset["clean_text"], batch_size=batch_size, max_length=max_length)

    # Extract Sentiment Scores & Labels
    df_chunk["text_sentiment"] = [int(result["label"].split()[0]) for result in results]
    df_chunk["text_sentiment_score"] = [float(result["score"]) for result in results]

    print(f"✅ Processed {len(df_chunk)} rows in {time.time() - start_time:.2f} sec (Max Length {max_length}, Batch Size {batch_size}).")
    
    return df_chunk  # Return processed data instead of updating DB immediately

# ---------------------------------------------------------------------------
# 5) Asynchronous Database Update
# ---------------------------------------------------------------------------
def update_database(processed_chunks, max_len, batch_size):
    """Updates the database asynchronously."""
    session = Session()
    start_time = time.time()
    try:
        update_values = [
            {
                "id": row["id"],
                "clean_text": row["clean_text"],
                "text_sentiment": row["text_sentiment"],
                "text_score": row["text_sentiment_score"]
            }
            for _, row in processed_chunks.iterrows()
        ]

        update_query = text(f"""
            UPDATE {TABLE_NAME}
            SET clean_text = :clean_text,
                text_sentiment = :text_sentiment,
                sentiment_confidence = :text_score
            WHERE id = :id
        """)

        session.execute(update_query, update_values)
        session.commit()
        print(f"✅ Updated {len(processed_chunks)} rows in {time.time() - start_time:.2f} sec (Max Length {max_len}, Batch Size {batch_size}).rows in the database.")

        # print(f"✅ Updated {len(processed_chunks)} rows in the database.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error updating database: {e}")

    finally:
        session.close()

# ---------------------------------------------------------------------------
# 6) Main Execution Loop (Iterating Over Text Lengths)
# ---------------------------------------------------------------------------
def main():
    session = Session()
    
    # Define text length ranges and corresponding batch sizes
    length_ranges = [(0, 4),(4, 8), (8, 16), (16, 32), (32, 64), (64, 128), (128, 256), (256, 512), (512, 10000)]
    batch_sizes = [64000,32000, 16000, 8000, 4000, 2000, 1000, 512, 10]  # Scaled inversely

    with ThreadPoolExecutor(max_workers=4) as executor:  # Thread pool for async DB updates
        for (min_len, max_len), batch_size in zip(length_ranges, batch_sizes):
            # Count rows within the text length range
            count_query = f"""
                SELECT COUNT(*) FROM reviews
                WHERE sentiment_confidence IS NULL
                AND LENGTH(text) >= {min_len} ;
            """
            total_count = pd.read_sql(count_query, engine).iloc[0, 0]

            if total_count == 0:
                continue  # Skip if no data in this length range

            num_batches = (total_count + batch_size - 1) // batch_size
            
            # Query reviews within this length range
            query = f"""
                SELECT id, text FROM reviews
                WHERE sentiment_confidence IS NULL
                AND LENGTH(text) >= {min_len}  ORDER BY LENGTH(text) ASC;
            """
            
            chunk_iter = pd.read_sql(query, engine, chunksize=batch_size)
            
            for df_chunk in tqdm(chunk_iter, total=num_batches, desc=f"Processing {min_len}-{max_len} chars"):
                processed_chunk = process_batch(df_chunk, max_len, batch_size)
                executor.submit(update_database, processed_chunk, max_len, batch_size)  # Send to DB update thread

    session.close()
    print("✅ All rows updated successfully!")

# ---------------------------------------------------------------------------
# 7) Run Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
