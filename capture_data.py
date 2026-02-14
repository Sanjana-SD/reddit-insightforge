import pandas as pd
from minio import Minio
from io import BytesIO
import random
from datetime import datetime, timedelta

# MinIO Config
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "gold"
OBJECT_NAME = "aggregated_data.parquet"

def generate_synthetic_data():
    print("⚠️ MinIO unavailable or empty. Generating synthetic data...")
    subreddits = ['tIFU', 'dataengineering', 'Python', 'MachineLearning', 'startups']
    data = []
    base_time = datetime.now()
    
    for _ in range(100):
        sub = random.choice(subreddits)
        data.append({
            'subreddit': sub,
            'title': f"Sample post about {sub} #{random.randint(1, 1000)}",
            'author': f"user_{random.randint(1, 50)}",
            'score': random.randint(0, 5000),
            'num_comments': random.randint(0, 500),
            'created_utc': base_time - timedelta(hours=random.randint(0, 48))
        })
    
    return pd.DataFrame(data)

def main():
    try:
        client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )
        
        response = client.get_object(BUCKET_NAME, OBJECT_NAME)
        data = BytesIO(response.read())
        df = pd.read_parquet(data)
        print("✅ Successfully loaded data from MinIO.")
        
    except Exception as e:
        print(f"❌ Could not load from MinIO: {e}")
        df = generate_synthetic_data()

    # Save to local
    output_path = "dashboard/data/sample_data.parquet"
    df.to_parquet(output_path, index=False)
    print(f"💾 Saved snapshot to {output_path}")
    print(df.head())

if __name__ == "__main__":
    main()
